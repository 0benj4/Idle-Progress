"""What each class actually DOES. All effects are automatic (no player input).

Per class:
  stats  : start-stat bonus, like a race (added on top of the race bonus)
  grow   : extra per-level growth for a stat (base growth is +10% per level,
           so {"INT": 0.02} means INT grows +12% per level)
  mechanics (all optional, 1.0 = no change):
    mana        max mana multiplier        regen       mana regen speed
    spell_cost  mana cost of casts         spell_power +power on every cast
      (power is what really counts: fewer injuries and more XP in combat steps;
       mana only limits casting early on, the hero casts every combat step later)
    injury      chance to get wounded      xp          all XP gained
    gold        quest gold + loot sales    drops       chance a step drops loot
    carry       carry capacity             discount    shop prices (gear, tomes, smith)
    events      chance of random events    luck_events extra chance events are good
Tune a class by editing its line here; the class screen text is generated from it.
"""

FX = {
    "Mage":        dict(stats={"INT": 3, "STR": -1}, grow={"INT": 0.02}, spell_power=2, mana=1.4),
    "Monk":        dict(stats={"DEX": 2, "VIT": 1}, grow={"DEX": 0.015}, regen=1.5, injury=0.85),
    "Paladin":     dict(stats={"STR": 1, "VIT": 2}, grow={"VIT": 0.015}, injury=0.85, regen=1.25),
    "Warrior":     dict(stats={"STR": 2, "VIT": 2, "INT": -1}, grow={"STR": 0.015}, injury=0.75),
    "Barbarian":   dict(stats={"STR": 3, "VIT": 1, "INT": -2}, grow={"STR": 0.02}, carry=1.3),
    "Druid":       dict(stats={"VIT": 2, "INT": 1}, grow={"VIT": 0.015}, xp=1.05, luck_events=0.1),
    "Priest":      dict(stats={"INT": 2, "VIT": 1}, spell_power=1, regen=1.4),
    "Cleric":      dict(stats={"VIT": 2, "INT": 1, "DEX": -1}, injury=0.85, mana=1.15),
    "Voodoo King": dict(stats={"INT": 2, "LCK": 1}, grow={"INT": 0.015}, spell_power=1, mana=1.1),
    "Engineer":    dict(stats={"INT": 2, "DEX": 1, "STR": -1}, discount=0.85),
    "Tunneler":    dict(stats={"STR": 1, "VIT": 2}, carry=1.25, gold=1.1),
    "Batrider":    dict(stats={"DEX": 2, "LCK": 1}, injury=0.85, drops=1.1),
    "Hunter":      dict(stats={"DEX": 2, "LCK": 1}, grow={"DEX": 0.015}, drops=1.25),
    "Runemaster":  dict(stats={"INT": 2, "STR": 1, "LCK": -1}, spell_power=1, spell_cost=0.9),
    "Bard":        dict(stats={"LCK": 2, "DEX": 1}, discount=0.9, events=1.5),
    "Shouter":     dict(stats={"VIT": 2, "STR": 1}, xp=1.1, injury=0.9),
    "Necromancer": dict(stats={"INT": 3, "VIT": -1}, grow={"INT": 0.015}, mana=1.2, spell_power=1, injury=1.1),
    "Rogue":       dict(stats={"DEX": 3, "LCK": 1, "VIT": -1}, gold=1.15, drops=1.15),
    "Alchemist":   dict(stats={"INT": 2, "LCK": 1}, discount=0.85, gold=1.05),
    "Pirate":      dict(stats={"STR": 1, "LCK": 2}, gold=1.2, events=1.3),
    "Ninja":       dict(stats={"DEX": 3, "VIT": -1}, grow={"DEX": 0.015}, injury=0.7, carry=0.9),
    "Chef":        dict(stats={"VIT": 2, "LCK": 1}, regen=1.3, carry=1.1, xp=1.05),
    "Beastmaster": dict(stats={"STR": 1, "VIT": 1, "LCK": 1}, carry=1.15, drops=1.1, injury=0.9),
    "Jester":      dict(stats={"LCK": 3, "STR": -1}, events=2.0, luck_events=0.15),
    "Gambler":     dict(stats={"LCK": 3, "VIT": -1}, events=1.6, luck_events=0.1, drops=1.1),
    "Samurai":     dict(stats={"STR": 2, "DEX": 2, "INT": -1}, grow={"STR": 0.01, "DEX": 0.01}, injury=0.8),
}


def fx(cls, key, default=1.0):
    return FX.get(cls, {}).get(key, default)


def stat_bonus(cls):
    return FX.get(cls, {}).get("stats", {})


def _pct(mult):
    return f"{abs(round((mult - 1) * 100))}%"


def describe(cls):
    """Short readable perk lines, generated from the numbers above."""
    d, out = FX.get(cls, {}), []
    if "grow" in d:
        out.append(" and ".join(d["grow"]) + " grows faster each level")
    if "mana" in d:
        out.append(f"+{_pct(d['mana'])} max mana")
    if "regen" in d:
        out.append(f"+{_pct(d['regen'])} mana regeneration")
    if "spell_cost" in d:
        out.append(f"spells cost {_pct(d['spell_cost'])} less mana")
    if "spell_power" in d:
        out.append(f"spells hit harder (+{d['spell_power']} power)")
    if "injury" in d:
        out.append(f"{_pct(d['injury'])} {'fewer' if d['injury'] < 1 else 'more'} injuries")
    if "xp" in d:
        out.append(f"+{_pct(d['xp'])} XP")
    if "gold" in d:
        out.append(f"+{_pct(d['gold'])} gold from quests and sales")
    if "drops" in d:
        out.append(f"+{_pct(d['drops'])} loot drops")
    if "carry" in d:
        out.append(f"{'+' if d['carry'] > 1 else '-'}{_pct(d['carry'])} carry capacity")
    if "discount" in d:
        out.append(f"{_pct(d['discount'])} cheaper shops, tomes and smith")
    if "events" in d:
        out.append(f"+{_pct(d['events'])} random events")
    if "luck_events" in d:
        out.append("luckier random events")
    return out
