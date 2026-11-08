"""Main game screen: progress bars, inventory, equipment."""
import curses
import json
import random
import time

from items import (ITEM_INFO, STOCK, TIERS, buy_price, item_weight, roll_drop, sell_price,
                   tier_index)
from quests import QUESTS
from sidequests_data import SIDE_QUESTS
from character import put
from classfx import fx
from events import BAD, FLAVOR, GOOD
from spells import SPELLS, best_affordable, known, learned_spells, price as spell_price

STEP_SECONDS = 3.0   # seconds for a step bar to fill
LOG_LINES = 4
INV_W = 34            # inventory column width (long item names fit)
SLOTS = ["Head", "Chest", "Legs", "Feet", "Weapon", "Weapon / Shield"]
XP_STEP = 10         # XP per step
XP_QUEST = 25
QUEST_LEVEL_XP = 0.15   # +15% XP per quest level
QUEST_LEVEL_GOLD = 0.20 # +20% gold per quest level
TOWN_QUEST = {
    "name": "Town Trip",
    "steps": ["Walking to the market", "Selling loot", "Buying supplies",
              "Studying at the spell school", "Visiting the blacksmith",
              "Walking back to the dungeon"],
}
FLEE_QUEST = {
    "name": "Wounded!",
    "steps": ["Running for my life", "Hiding in a ditch", "Bandaging the wounds",
              "Limping back to town"],
}
BASE_MANA = 10         # max mana = BASE_MANA + MANA_PER_INT * INT
MANA_PER_INT = 3
MANA_REGEN_SECONDS = 60  # time to refill an empty mana pool
SPELL_XP_BONUS = 0.10  # +10% step XP per spell power point
COMBAT_WORDS = ("Fight", "Dodg", "Duel", "Ambush", "Wrestl", "Defeat", "Slay", "Repel")
DROP_CHANCE = 0.5      # chance a step drops a tag-matched item
GOLD_QUEST = 15      # gold for completing a quest
STAT_GROWTH = 1.10   # stats grow 10% per level (proportional)
INT_XP = 0.002       # each INT point: +0.2% XP
LCK_DROPS = 0.004    # each LCK point: +0.4% loot drop chance


def cfx(prog, key, default=1.0):
    """The character's class effect for this key (see classfx.py)."""
    return fx(prog.get("class", ""), key, default)


def shop_price(prog, name):
    return max(1, round(buy_price(name) * cfx(prog, "discount")))


def bar(frac, width):
    frac = max(0.0, min(1.0, frac))
    filled = int(frac * width)
    return "[" + "█" * filled + "░" * (width - filled) + f"] {int(frac * 100):3d}%"


def xp_needed(level):
    """XP needed per level. No level cap, but it gets steeply harder:
    40 * L^2 * 1.05^L  (Lv 10: 6.5k, Lv 20: 42k, Lv 50: 1.1M)."""
    return int(40 * level ** 2 * 1.05 ** level)


PLUS_STEP = 0.15       # each blacksmith + adds 15% of the item's bonus
PLUS_MAX = 10


def plus_of(prog, slot):
    """Blacksmith upgrade level of what is worn in this slot (0 if the item changed)."""
    p = prog.get("plus", {}).get(slot)
    item = prog["equipped"].get(slot)
    return p["lvl"] if p and item and p["item"] == item else 0


def gear_bonus(prog):
    """Total stat bonus from everything worn (blacksmith upgrades included)."""
    total = {}
    for slot, item in prog["equipped"].items():
        mult = 1 + PLUS_STEP * plus_of(prog, slot)
        for stat, v in (ITEM_INFO.get(item, {}).get("bonus", {}) if item else {}).items():
            total[stat] = total.get(stat, 0) + v * mult
    return total


def stats_now(prog):
    """Base stats (they grow with level) + worn gear."""
    bonus = gear_bonus(prog)
    return {k: v + bonus.get(k, 0) for k, v in prog["stats_f"].items()}


def gear_score(name):
    return sum(ITEM_INFO[name]["bonus"].values())


def auto_equip(prog, log):
    """Wear the best usable gear for every slot; the rest stays in the pack."""
    eq = prog["equipped"]
    pool = dict(prog["inventory"])
    for item in eq.values():
        if item:
            pool[item] = pool.get(item, 0) + 1
    lvl = prog["level"]

    def pick(slot, cats):
        cands = [n for n, k in pool.items()
                 if k > 0 and ITEM_INFO.get(n, {}).get("category") in cats
                 and ITEM_INFO[n]["level"] <= lvl]
        if not cands:
            return None
        def worth(n):   # an upgraded piece counts for more than its plain twin
            worn = n == eq.get(slot)
            return (gear_score(n) * (1 + PLUS_STEP * plus_of(prog, slot) * worn), worn)
        best = max(cands, key=worth)
        pool[best] -= 1
        return best

    new = {}
    for slot in ("Head", "Chest", "Legs", "Feet"):
        new[slot] = pick(slot, (slot,))
    new["Weapon"] = pick("Weapon", ("Weapon",))
    new["Weapon / Shield"] = pick("Weapon / Shield", ("Weapon", "Shield"))
    for slot, item in new.items():
        if item and item != eq.get(slot):
            log.append(f"Equipped {item}")
    prog["equipped"] = new
    prog["inventory"] = {n: k for n, k in pool.items() if k > 0}


def gain_xp(prog, amount, log):
    amount = max(1, round(amount * cfx(prog, "xp") * (1 + INT_XP * stats_now(prog)["INT"])))
    prog["xp"] += amount
    leveled = False
    while prog["xp"] >= xp_needed(prog["level"]):
        prog["xp"] -= xp_needed(prog["level"])
        prog["level"] += 1
        for k in prog["stats_f"]:
            prog["stats_f"][k] *= STAT_GROWTH + cfx(prog, "grow", {}).get(k, 0)
        log.append(f"** Level up! Lv {prog['level']} **")
        leveled = True
    if leveled:
        auto_equip(prog, log)   # new level may unlock better gear


def capacity(prog):
    """Carry limit from the character's current stats."""
    st = stats_now(prog)
    return int((20 + 3 * st["STR"] + 2 * st["VIT"]) * cfx(prog, "carry"))


def carried(prog):
    return sum(item_weight(n) * c for n, c in prog["inventory"].items())


FUTURE_GEAR_WINDOW = 12   # only keep gear that is at most this many levels away


def future_gear(prog):
    """Gear the hero can't wear YET but would wear once the level allows: it is kept,
    not sold. Per slot group: the piece wearable soonest and the strongest one (often the
    same), and only if it beats what is worn."""
    lvl, eq = prog["level"], prog["equipped"]

    def score(slot):
        return gear_score(eq[slot]) if eq.get(slot) else 0

    groups = [(("Head",), score("Head")), (("Chest",), score("Chest")),
              (("Legs",), score("Legs")), (("Feet",), score("Feet")),
              (("Weapon",), min(score("Weapon"), score("Weapon / Shield"))),
              (("Shield",), score("Weapon / Shield"))]
    keep = set()
    for cats, cur in groups:
        cands = [n for n in prog["inventory"]
                 if ITEM_INFO.get(n, {}).get("category") in cats
                 and lvl < ITEM_INFO[n]["level"] <= lvl + FUTURE_GEAR_WINDOW
                 and gear_score(n) > cur]
        if cands:   # the one wearable soonest, and the strongest of all
            keep.add(min(cands, key=lambda n: (ITEM_INFO[n]["level"], -gear_score(n))))
            keep.add(max(cands, key=gear_score))
    return keep


def sellable_count(prog, keep=None):
    """How many of each item the shop would take (supplies and kept gear stay)."""
    keep = future_gear(prog) if keep is None else keep
    return {n: c - (1 if n in keep else 0) for n, c in prog["inventory"].items()
            if n not in STOCK and c - (1 if n in keep else 0) > 0}


def needs_town(prog):
    """Full pack AND something to sell (supplies and kept gear are never sold)."""
    return bool(sellable_count(prog)) and carried(prog) >= capacity(prog)


QUEST_BELOW = 6        # quests up to this many levels below the character...
QUEST_ABOVE = 3        # ...and this many above are candidates for the next one
RECENT_QUESTS = 12     # don't repeat a quest played in the last N
SIDE_CHANCE = 0.25     # chance of a side quest after each main quest
SIDE_XP_MULT = 0.5     # side quests pay half XP / gold...
SIDE_DROP_CHANCE = 0.25  # ...and drop items less often. They never injure.
SIDE_BELOW, SIDE_ABOVE = 10, 2
SIDE_BY_NAME = {q["name"]: q for q in SIDE_QUESTS}


def choose_side_quest(prog):
    """Start a side quest near the character's level (not one of the last few)."""
    lvl = prog["level"]
    recent = prog.setdefault("recent_side", [])
    fresh = lambda i: SIDE_QUESTS[i]["name"] not in recent
    near = [i for i, q in enumerate(SIDE_QUESTS)
            if lvl - SIDE_BELOW <= q["level"] <= lvl + SIDE_ABOVE and fresh(i)]
    if not near:
        by_dist = sorted(range(len(SIDE_QUESTS)), key=lambda i: abs(SIDE_QUESTS[i]["level"] - lvl))
        near = [i for i in by_dist[:6] if fresh(i)] or by_dist[:2]
    q = SIDE_QUESTS[random.choice(near)]
    recent.append(q["name"])
    del recent[:-5]
    prog["side"], prog["side_step"] = q["name"], 0


def choose_next_quest(prog):
    """Next quest = a random one near the character's level, not played recently."""
    lvl = prog["level"]
    recent = prog.setdefault("recent", [])
    fresh = lambda i: QUESTS[i]["name"] not in recent
    near = [i for i, q in enumerate(QUESTS)
            if lvl - QUEST_BELOW <= q["level"] <= lvl + QUEST_ABOVE and fresh(i)]
    if len(near) < 3:   # level beyond the list: take the closest quests instead
        by_dist = sorted(range(len(QUESTS)), key=lambda i: abs(QUESTS[i]["level"] - lvl))
        near = [i for i in by_dist[:10] if fresh(i)] or by_dist[:3]
    i = random.choice(near)
    recent.append(QUESTS[i]["name"])
    del recent[:-RECENT_QUESTS]
    prog["quest"], prog["quest_name"], prog["step"] = i, QUESTS[i]["name"], 0
    return i


def max_mana(prog):
    return int((BASE_MANA + MANA_PER_INT * stats_now(prog)["INT"]) * cfx(prog, "mana"))


def is_combat(step):
    return any(w in step for w in COMBAT_WORDS)


def injury_chance(prog, quest, step, power=0):
    """Chance per step to get wounded and flee. Higher when the quest is above the
    character's level and in combat steps; tougher (VIT) characters get hurt less."""
    gap = quest.get("level", 1) - prog["level"]
    chance = 0.004 + 0.004 * max(0, gap + 2)
    if is_combat(step):
        chance *= 2
    chance *= max(0.3, 1 - 0.07 * power)   # a spell cast lowers the risk
    st = stats_now(prog)
    chance *= 8 / (4 + (st["VIT"] + st["DEX"]) / 2)   # tough (VIT) and nimble (DEX)
    chance *= cfx(prog, "injury")
    return min(chance, 0.30)


GEAR_MAX_TIER = 3        # shop sells Basic..Rare; Mythic gear only drops
GEAR_STOCK_SIZE = 4      # random pieces the shop offers per slot, per trip
GEAR_PER_TRIP = 2        # at most this many upgrades bought per town trip
TRADE_STEPS = ("Selling loot", "Buying supplies")
TRADE_MAX_FILL = 0.25      # seconds for the trade bar to fill once (one item)
TRADE_MAX_TOTAL = 8.0      # a whole sale never takes longer than this


def plan_gear(prog, gold):
    """Pick this trip's gear upgrades: a random shop stock per slot, the best
    piece of it only if it beats what is worn, biggest upgrades first."""
    lvl, offers = prog["level"], []
    for slot in SLOTS:
        cats = ("Weapon", "Shield") if slot == "Weapon / Shield" else (slot,)
        worn = prog["equipped"].get(slot)
        cur = gear_score(worn) if worn else 0
        pool = [n for n, e in ITEM_INFO.items()
                if e["category"] in cats and e["level"] <= lvl
                and tier_index(n) <= GEAR_MAX_TIER]
        if not pool:
            continue
        best = max(random.sample(pool, min(GEAR_STOCK_SIZE, len(pool))), key=gear_score)
        if gear_score(best) > cur:
            offers.append((gear_score(best) - cur, best))
    queue = []
    for _, name in sorted(offers, reverse=True):
        if len(queue) < GEAR_PER_TRIP and name not in queue and gold >= shop_price(prog, name):
            queue.append(name)
            gold -= shop_price(prog, name)
    return queue


def plan_trade(prog, step, log):
    """Build the list of single-item transactions for this town step."""
    inv = prog["inventory"]
    if step == "Selling loot":
        auto_equip(prog, log)          # keep the best gear first, sell the rest
        inv = prog["inventory"]
        sellable = sellable_count(prog)
        queue = [n for n in sorted(sellable) for _ in range(sellable[n])]
        return {"kind": "sell", "queue": queue, "total": len(queue), "frac": 0.0,
                "gold": 0, "done": []}
    queue, gold, weight = [], prog["gold"], carried(prog)   # buying supplies
    for name in STOCK:   # buy if missing; never spend more than half the gold
        price = shop_price(prog, name)
        if (inv.get(name, 0) == 0 and gold >= price * 2
                and weight + item_weight(name) <= capacity(prog)):
            queue.append(name)
            gold -= price
            weight += item_weight(name)
    queue += plan_gear(prog, gold)       # supplies are paid first, gear gets the rest
    return {"kind": "buy", "queue": queue, "total": len(queue), "frac": 0.0,
            "gold": 0, "done": []}


def run_trade(prog, step, dt, log):
    """Do the town trade one item at a time; the small bar fills once per item."""
    tr = prog.get("trade")
    if tr is None:
        tr = prog["trade"] = plan_trade(prog, step, log)
    inv = prog["inventory"]
    if tr["queue"]:
        tr["frac"] += dt / min(TRADE_MAX_FILL, TRADE_MAX_TOTAL / tr["total"])
        while tr["frac"] >= 1.0 and tr["queue"]:
            tr["frac"] -= 1.0
            name = tr["queue"].pop(0)
            if tr["kind"] == "sell":
                if inv.get(name, 0) > 0:
                    inv[name] -= 1
                    if inv[name] == 0:
                        del inv[name]
                    got = round(sell_price(name) * cfx(prog, "gold"))
                    prog["gold"] += got
                    tr["gold"] += got
                    tr["done"].append(name)
            else:
                prog["gold"] -= shop_price(prog, name)
                inv[name] = inv.get(name, 0) + 1
                tr["done"].append(name)
    if tr["queue"]:
        prog["frac"] = (tr["total"] - len(tr["queue"])) / tr["total"]   # main bar = whole trade
        return
    if tr["kind"] == "sell":
        n = len(tr["done"])
        log.append(f"Sold {n} items  +{tr['gold']} gold" if n else "Nothing to sell")
    else:
        log.append("Bought " + ", ".join(tr["done"]) if tr["done"] else "Bought nothing")
        auto_equip(prog, log)            # wear what was just bought
    prog["trade"] = None
    prog["trade_done"] = True      # the step itself can now complete
    prog["frac"] = 1.0


SHOP_RESERVE = 100     # trainer and smith never spend the last 100 gold


def run_trainer(prog, log):
    """Buy tomes for every spell the character is able to learn, strongest first."""
    todo = [sp for sp in SPELLS if sp.level <= prog["level"] and sp.name not in prog["spells"]]
    for sp in sorted(todo, key=lambda sp: (-sp.power, sp.level)):
        cost = max(1, round(spell_price(sp) * cfx(prog, "discount")))
        if prog["gold"] - cost >= SHOP_RESERVE:
            prog["gold"] -= cost
            prog["spells"].append(sp.name)
            log.append(f"Bought Tome of {sp.name} (-{cost} gold)")
            log.append(f"Learned {sp.name}!")


SMITH_PER_TRIP = 4     # upgrade attempts per town trip


def plus_cap(prog):
    return min(PLUS_MAX, prog["level"] // 4)


def upgrade_cost(item, lvl):
    return int((50 + 4 * ITEM_INFO[item]["value"]) * 2 ** lvl)


def upgrade_odds(lvl):
    """+1..+3 always work; after that the hammer may slip (gold is lost, gear is safe)."""
    return 1.0 if lvl < 3 else max(0.4, 1 - 0.1 * (lvl - 2))


def run_smith(prog, log):
    """Pay the blacksmith to upgrade worn gear, cheapest upgrade first."""
    for _ in range(SMITH_PER_TRIP):
        options = []
        for slot, item in prog["equipped"].items():
            lvl = plus_of(prog, slot)
            if item and lvl < plus_cap(prog):
                cost = max(1, round(upgrade_cost(item, lvl) * cfx(prog, "discount")))
                if prog["gold"] - cost >= SHOP_RESERVE:
                    options.append((cost, slot, item, lvl))
        if not options:
            return
        cost, slot, item, lvl = min(options)
        prog["gold"] -= cost
        if random.random() < upgrade_odds(lvl):
            prog["plus"][slot] = {"item": item, "lvl": lvl + 1}
            log.append(f"Smith upgraded {item} to +{lvl + 1} (-{cost} gold)")
        else:
            log.append(f"The hammer slipped on {item} (-{cost} gold)")


EVENT_CHANCE = 0.04    # chance per quest step that something happens


def random_event(prog, quest, log):
    """One small surprise: mostly nice, sometimes a bit unlucky. Never hurts badly."""
    ql = quest.get("level", 1)
    good = min(0.85, 0.45 + 0.02 * prog["stats_f"].get("LCK", 5) + cfx(prog, "luck_events", 0))
    r = random.random()
    kind, text = random.choice(GOOD if r < good else FLAVOR if r < good + 0.25 else BAD)
    base = GOLD_QUEST * (1 + QUEST_LEVEL_GOLD * ql)
    if kind == "item" and not quest.get("tags"):
        kind = "xp"
    if kind == "gold+":
        gold = round(base * random.uniform(1, 3))
        prog["gold"] += gold
        text += f" (+{gold} gold)"
    elif kind == "gold-":
        gold = min(prog["gold"], max(round(base * random.uniform(1, 2)), prog["gold"] // 50))
        prog["gold"] -= gold
        text += f" (-{gold} gold)"
    elif kind == "xp":
        xp = max(1, round(XP_QUEST * (1 + QUEST_LEVEL_XP * ql) * random.uniform(1, 2)))
        log.append(f"~ {text} (+{xp} XP)")
        gain_xp(prog, xp, log)
        return
    elif kind == "mana+":
        prog["mana"] = min(max_mana(prog), prog["mana"] + max_mana(prog) * 0.5)
        text += " (+mana)"
    elif kind == "mana-":
        prog["mana"] = max(0.0, prog["mana"] - max_mana(prog) * 0.3)
        text += " (-mana)"
    elif kind == "item":
        got = roll_drop(quest["tags"], ql)
        if got:
            prog["inventory"][got] = prog["inventory"].get(got, 0) + 1
            text += f" (+{got})"
            if "bonus" in ITEM_INFO.get(got, {}):
                auto_equip(prog, log)
    log.append("~ " + text)


def save_game(path, data):
    with open(path, "w") as f:
        json.dump(data, f, ensure_ascii=False)


def tick(prog, char, dt, log):
    """Advance the game by dt seconds (no drawing). Returns what the screen needs:
    (mode, quest, steps, idx, max_mana, stepped) - stepped is True when a step finished."""
    stepped = False
    town, flee = prog.get("town"), prog.get("flee")   # trip step indexes or None
    if isinstance(town, bool):       # very old saves
        town = prog["town"] = None
    if prog.get("side") not in SIDE_BY_NAME:
        prog["side"] = None
    side = prog.get("side")          # name of the running side quest or None

    def pick_mode():
        return ("flee" if prog.get("flee") is not None
                else "town" if prog.get("town") is not None
                else "side" if prog.get("side") else "quest")

    def quest_for(m):
        if m == "flee":
            return FLEE_QUEST
        if m == "town":
            return TOWN_QUEST
        if m == "side":
            return SIDE_BY_NAME[prog["side"]]
        return QUESTS[prog["quest"] % len(QUESTS)]

    def index_for(m):
        return {"flee": prog.get("flee"), "town": prog.get("town"),
                "side": prog["side_step"], "quest": prog["step"]}[m]

    mode = pick_mode()
    quest = quest_for(mode)
    steps = quest["steps"]
    idx = index_for(mode)
    if idx >= len(steps):            # quest list changed since the save
        idx = 0
        if mode == "side":
            prog["side_step"] = 0
        else:
            prog["step"] = 0

    # Bar 1: step
    mx = max_mana(prog)
    prog["mana"] = min(mx, prog["mana"] + mx * dt * cfx(prog, "regen") / MANA_REGEN_SECONDS)
    trade_active = mode == "town" and steps[idx] in TRADE_STEPS
    if not trade_active:
        prog["trade"] = None
    if trade_active and not prog.get("trade_done"):
        run_trade(prog, steps[idx], dt, log)
    elif not trade_active:
        prog["frac"] += dt / STEP_SECONDS
    while prog["frac"] >= 1.0:
        prog["frac"] -= 1.0
        name = steps[idx]
        ql = quest.get("level", 1)
        cast = None
        if mode == "quest" and is_combat(name):
            cost_mult = cfx(prog, "spell_cost")
            cast = best_affordable(learned_spells(prog["spells"]), prog["mana"], cost_mult)
            if cast:
                cast_cost = max(1, round(cast.cost * cost_mult))
                prog["mana"] -= cast_cost
                log.append(f"Cast {cast.name} (-{cast_cost} MP)")
        power = cast.power + int(cfx(prog, "spell_power", 0)) if cast else 0
        if mode == "quest" and random.random() < injury_chance(prog, quest, name, power):
            # wounded: abandon the quest and run (side quests are safe)
            log.append(f"Ouch! Wounded during: {name}")
            log.append(f"== Quest failed: {quest['name']} ==")
            if prog["quest_items"]:
                log.append("Lost: " + ", ".join(prog["quest_items"]))
                prog["quest_items"] = []
            prog["fled"] += 1
            choose_next_quest(prog)
            prog["flee"] = 0
            mode, idx = "flee", 0
            quest = FLEE_QUEST
            steps = quest["steps"]
            continue
        log.append(name + " ✔")
        if mode == "town":
            prog["trade_done"] = False   # the trade already happened
            if name == "Studying at the spell school":
                run_trainer(prog, log)
            elif name == "Visiting the blacksmith":
                run_smith(prog, log)
        elif mode in ("quest", "side"):
            mult = SIDE_XP_MULT if mode == "side" else 1.0
            step_xp = (XP_STEP * (1 + QUEST_LEVEL_XP * ql) * (1 + SPELL_XP_BONUS * power)
                       * mult)
            gain_xp(prog, max(1, round(step_xp)), log)
            qitem = quest.get("quest_loot", {}).get(name)
            if qitem and qitem not in prog["quest_items"]:
                prog["quest_items"].append(qitem)
                log.append(f"+ {qitem} (quest item)")
            drop = quest.get("loot", {}).get(name)
            got = None
            chance = min(1.0, (SIDE_DROP_CHANCE if mode == "side" else DROP_CHANCE) * cfx(prog, "drops") * (1 + LCK_DROPS * stats_now(prog)["LCK"]))
            if drop:                                   # fixed drop
                got = drop[0] if random.random() < drop[1] else None
            elif quest.get("tags") and random.random() < chance:
                tags = quest.get("step_tags", {}).get(name) or quest["tags"]
                got = roll_drop(tags, ql)
            if got:
                inv = prog["inventory"]
                inv[got] = inv.get(got, 0) + 1
                log.append(f"+ {got}")
                if "bonus" in ITEM_INFO.get(got, {}):
                    auto_equip(prog, log)
            if random.random() < EVENT_CHANCE * cfx(prog, "events"):
                random_event(prog, quest, log)
        idx += 1
        if idx >= len(steps):
            if mode == "flee":     # safe again: go to town to sell and rest
                prog["flee"] = None
                prog["town"] = 0
                prog["after_flee"] = True
                mode, idx = "town", 0
            elif mode == "town":   # back to work
                prog["town"] = None
                if prog.pop("after_flee", False) and not prog.get("side"):
                    choose_side_quest(prog)   # rest from the wounds with a safe job
                mode = pick_mode()
                idx = index_for(mode)
            elif mode == "side":   # side quest done (half rewards)
                gold = max(1, round(GOLD_QUEST * (1 + QUEST_LEVEL_GOLD * ql) * SIDE_XP_MULT * cfx(prog, "gold")))
                log.append(f"== Side quest complete: {quest['name']} ==")
                if prog["quest_items"]:
                    log.append("Handed in: " + ", ".join(prog["quest_items"]))
                    prog["quest_items"] = []
                prog["side_done"] += 1
                gain_xp(prog, max(1, round(XP_QUEST * (1 + QUEST_LEVEL_XP * ql) * SIDE_XP_MULT)), log)
                prog["gold"] += gold
                log.append(f"+ {gold} gold")
                prog["side"], prog["side_step"] = None, 0
                mode = "quest"
                idx = prog["step"]
            else:                  # quest done: rewards, next quest
                gold = round(GOLD_QUEST * (1 + QUEST_LEVEL_GOLD * ql) * cfx(prog, "gold"))
                log.append(f"== Quest complete: {quest['name']} ==")
                if prog["quest_items"]:
                    log.append("Handed in: " + ", ".join(prog["quest_items"]))
                    prog["quest_items"] = []
                prog["done"] += 1
                gain_xp(prog, round(XP_QUEST * (1 + QUEST_LEVEL_XP * ql)), log)
                prog["gold"] += gold
                log.append(f"+ {gold} gold")
                choose_next_quest(prog)
                idx = 0
                if random.random() < SIDE_CHANCE:
                    choose_side_quest(prog)
                    mode = "side"
        elif mode == "flee":
            prog["flee"] = idx
        elif mode == "town":
            prog["town"] = idx
        elif mode == "side":
            prog["side_step"] = idx
        else:
            prog["step"] = idx
        if mode in ("quest", "side") and needs_town(prog):   # pack is full: go sell
            log.append("Pack is full! Heading to town")
            prog["town"] = 0
            mode = "town"
            idx = 0
        quest = quest_for(mode)
        steps = quest["steps"]
        char["stats"] = {k: round(v) for k, v in prog["stats_f"].items()}
        stepped = True
    return mode, quest, steps, idx, mx, stepped


def run_game(stdscr, data, save_path):
    """data: save dict. Q/Esc returns to the menu."""
    green = curses.color_pair(1)
    tier_attr = []
    for i, (_, c256, c8) in enumerate(TIERS):
        try:
            curses.init_pair(10 + i, c256 if curses.COLORS >= 256 else c8, -1)
            tier_attr.append(curses.color_pair(10 + i))
        except curses.error:
            tier_attr.append(0)
    char = data["character"]
    old = {"GÜÇ": "STR", "ÇEV": "DEX", "ZEK": "INT", "DAY": "VIT", "ŞNS": "LCK"}   # old saves
    char["stats"] = {old.get(k, k): v for k, v in char.get("stats", {}).items()}
    if "stats_f" in data.get("progress", {}):
        data["progress"]["stats_f"] = {old.get(k, k): v for k, v in data["progress"]["stats_f"].items()}
    prog = data.setdefault("progress", {"quest": 0, "step": 0, "frac": 0.0, "done": 0})
    prog.setdefault("inventory", {})
    prog.setdefault("gold", 0)
    prog.setdefault("fled", 0)
    prog.setdefault("side_done", 0)
    prog.setdefault("side_step", 0)
    prog.setdefault("mana", None)
    prog.setdefault("quest_items", [])
    prog.setdefault("equipped", {slot: None for slot in SLOTS})
    prog.setdefault("level", 1)
    prog.setdefault("xp", 0)
    prog.setdefault("plus", {})
    prog["class"] = char.get("class", "")
    if "spells" not in prog:   # spells are bought now; old saves keep what they had
        prog["spells"] = [sp.name for sp in known(prog["level"])]
    prog.setdefault("stats_f", {k: float(v) for k, v in char.get("stats", {}).items()})
    for slot in SLOTS:
        prog["equipped"].setdefault(slot, None)
    auto_equip(prog, [])
    if prog["mana"] is None:
        prog["mana"] = float(max_mana(prog))
    names = [q["name"] for q in QUESTS]
    if prog.get("quest_name") in names:
        prog["quest"] = names.index(prog["quest_name"])
    elif prog["done"] == 0 and prog["step"] == 0:   # brand-new character: start with the intro quest
        prog["quest"], prog["quest_name"] = 0, QUESTS[0]["name"]
        prog.setdefault("recent", []).append(QUESTS[0]["name"])
    else:                                           # old save: pick a quest that fits the level
        choose_next_quest(prog)
    save_game(save_path, data)   # a brand-new character is saved right away
    log = []

    stdscr.timeout(100)
    last = time.monotonic()
    try:
        while True:
            now = time.monotonic()
            dt, last = min(now - last, 1.0), now  # tek karede en fazla 1 sn
            mode, quest, steps, idx, mx, stepped = tick(prog, char, dt, log)
            if stepped:
                save_game(save_path, data)
            log = log[-LOG_LINES:]

            # Drawing
            stdscr.erase()
            h, w = stdscr.getmaxyx()
            bw = max(10, min(36, w - 14 - INV_W - 26))
            px = 3 + bw + 7 + 4  # envanter paneli x konumu
            put(stdscr, 1, 3, f"Lv {prog['level']}", curses.color_pair(2) | curses.A_BOLD)
            put(stdscr, 1, 10, f"{char['name']}  -  {char['race']} {char.get('class', '')}",
                green | curses.A_BOLD)
            gb = gear_bonus(prog)
            put(stdscr, 2, 3, "  ".join(
                f"{k} {round(v)}" + (f" (+{round(gb[k])})" if gb.get(k) else "")
                for k, v in stats_now(prog).items()), curses.A_DIM)

            put(stdscr, 4, 3, f"Quest: {quest['name']}" + (" (Side)" if mode == "side" else ""), curses.A_BOLD)
            dots = "." * (int(now * 3) % 4)
            put(stdscr, 6, 3, f"{steps[idx]}{dots}")
            put(stdscr, 7, 3, bar(prog["frac"], bw), green)

            put(stdscr, 9, 3, f"Quest progress: {idx}/{len(steps)}", curses.A_DIM)
            put(stdscr, 10, 3, bar(idx / len(steps), bw), green)

            put(stdscr, 12, 3, f"Quests completed: {prog['done']}   Side: {prog['side_done']}   Fled: {prog['fled']}", curses.A_BOLD)
            for i, line in enumerate(log):
                put(stdscr, 14 + i, 3, line, curses.A_DIM)

            # Right side: XP (small) + Inventory + Equipped
            if px + 20 <= w:
                need = xp_needed(prog["level"])
                put(stdscr, 4, px, f"XP {prog['xp']}/{need}", curses.A_DIM)
                put(stdscr, 5, px, bar(prog["xp"] / need, 14), green)
                put(stdscr, 5, px + 24, f"Gold: {prog['gold']}", tier_attr[4] | curses.A_BOLD)
                put(stdscr, 6, px, f"MP {int(prog['mana'])}/{mx}", curses.A_DIM)

                for y in range(4, h - 3):
                    put(stdscr, y, px - 2, "│", curses.A_DIM)
                put(stdscr, 7, px, "INVENTORY", green | curses.A_BOLD)
                cap, load = capacity(prog), carried(prog)
                put(stdscr, 7, px + 10, f"{load}/{cap}",
                    tier_attr[4] | curses.A_BOLD if load >= cap else curses.A_DIM)
                qi = prog["quest_items"]
                lines = [(f"* {q}", curses.A_BOLD) for q in qi]   # quest items on top, no tier color
                groups = [("Weapons", ("Weapon",)), ("Armor", ("Head", "Chest", "Legs", "Feet")),
                          ("Shields", ("Shield",)), ("Other", None)]
                inv = prog["inventory"]
                placed = set()
                for gname, cats in groups:
                    names = [n for n in inv
                             if n not in placed and (
                                 cats is None or ITEM_INFO.get(n, {}).get("category") in cats)]
                    if not names:
                        continue
                    placed.update(names)
                    if lines:
                        lines.append(("", 0))
                    lines.append((f"-- {gname} --", curses.A_DIM))
                    for n in sorted(names, key=lambda n: (-tier_index(n), n)):
                        lines.append((f"{n} x{inv[n]}", tier_attr[tier_index(n)]))
                if not lines:
                    lines.append(("(empty)", curses.A_DIM))
                tr = prog.get("trade")
                if tr:   # small fast bar: one fill = one item bought/sold
                    put(stdscr, 8, px, bar(tr["frac"], 14), tier_attr[4])
                room = max(1, h - 3 - 10)
                for i, (text, attr) in enumerate(lines[:room]):
                    if i == room - 1 and len(lines) > room:
                        text, attr = "...", curses.A_DIM
                    put(stdscr, 10 + i, px, text, attr)

                ex = px + INV_W + 2
                if ex + 24 <= w:
                    for y in range(7, h - 3):
                        put(stdscr, y, ex - 2, "│", curses.A_DIM)
                    put(stdscr, 7, ex, "EQUIPPED", green | curses.A_BOLD)
                    for i, slot in enumerate(SLOTS):
                        item = prog["equipped"].get(slot)
                        put(stdscr, 9 + i * 2, ex, slot, curses.A_BOLD)
                        if item:
                            plus = plus_of(prog, slot)
                            label = f"{item} +{plus}" if plus else item   # blacksmith upgrade
                            put(stdscr, 10 + i * 2, ex + 2, label, tier_attr[tier_index(item)])
                        else:
                            put(stdscr, 10 + i * 2, ex + 2, "-", curses.A_DIM)
                    sy = 9 + len(SLOTS) * 2 + 1
                    spells = learned_spells(prog["spells"])
                    put(stdscr, sy, ex, f"SPELLS ({len(spells)})", green | curses.A_BOLD)
                    room = max(1, h - 3 - (sy + 2))
                    for i, sp in enumerate(reversed(spells)):   # newest first
                        if i == room - 1 and len(spells) > room:
                            put(stdscr, sy + 2 + i, ex, "...", curses.A_DIM)
                            break
                        put(stdscr, sy + 2 + i, ex, f"{sp.name} ({sp.cost})", curses.A_DIM)

            put(stdscr, h - 2, 3, "Q / Esc: back to menu (game is saved)", curses.A_DIM)
            stdscr.refresh()

            key = stdscr.getch()
            if key in (ord("q"), ord("Q"), 27):
                break
    finally:
        stdscr.timeout(-1)
        save_game(save_path, data)
