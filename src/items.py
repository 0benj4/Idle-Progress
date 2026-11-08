"""Item definitions: tiers and each item's tier.
To add an item, put  "Item name": "Tier"  in ITEMS (unlisted items count as Basic)."""

# (name, 256-color number, 8-color fallback)  -- weakest to strongest
TIERS = [
    ("Basic",    250, 7),   # grey/white
    ("Common",    71, 2),   # green
    ("Uncommon",  39, 6),   # blue/cyan
    ("Rare",     135, 5),   # purple
    ("Mythic",   208, 3),   # orange/gold
]
TIER_NAMES = [t[0] for t in TIERS]

ITEMS = {
    "Pebble": "Basic",
    "Bone": "Basic",
    "Torn Cloth": "Common",
    "Rusty Key": "Uncommon",
}


def tier_of(item):
    return ITEMS.get(item, "Basic")


def tier_index(item):
    return TIER_NAMES.index(tier_of(item))


# Sell value (gold). The shop sells an item for BUY_MULT times this.
VALUE = {
    "Pebble": 1,
    "Bone": 3,
    "Torn Cloth": 8,
    "Rusty Key": 25,
    "Torch": 4,
    "Rope": 6,
    "Lockpick": 15,
    "Healing Potion": 20,
}
BUY_MULT = 3

# Shop supplies. Price is computed from VALUE.
STOCK = ["Torch", "Rope", "Lockpick", "Healing Potion"]
ITEMS.update({"Torch": "Basic", "Rope": "Basic", "Lockpick": "Common", "Healing Potion": "Common"})


def sell_price(item):
    return VALUE.get(item, 1)


GEAR_CATEGORIES = ("Head", "Chest", "Legs", "Feet", "Weapon", "Shield")
GEAR_BUY_MULT = 6      # gear costs 6x its value in the shop (supplies: BUY_MULT)


def buy_price(item):
    info = ITEM_INFO.get(item)
    mult = GEAR_BUY_MULT if info and info["category"] in GEAR_CATEGORIES else BUY_MULT
    return VALUE.get(item, 1) * mult


# Weight of one item (unlisted items weigh 1).
WEIGHT = {
    "Pebble": 2,
    "Bone": 1,
    "Torn Cloth": 1,
    "Rusty Key": 1,
    "Torch": 1,
    "Rope": 2,
    "Lockpick": 1,
    "Healing Potion": 1,
}


def item_weight(item):
    return WEIGHT.get(item, 1)


# ---- the 300-item database (items_data.py) --------------------------------
# Hand-set values above win; everything else is filled in from the database.
from items_data import DB  # noqa: E402

ITEM_INFO = {e["name"]: e for e in DB}   # full info: category, tags, slot, bonus, level...
for _e in DB:
    ITEMS.setdefault(_e["name"], _e["tier"])
    VALUE.setdefault(_e["name"], _e["value"])
    WEIGHT.setdefault(_e["name"], _e["weight"])


# ---- tag-based drops --------------------------------------------------------
import random as _random  # noqa: E402

TIER_BASE_WEIGHT = [60, 30, 12, 4, 1]   # chance weights Basic .. Mythic
LEVEL_BOOST = 0.03                      # higher quest level -> better tiers
_pools = {}


def _pool(tags):
    key = tuple(sorted(tags))
    if key not in _pools:
        tagset = set(tags)
        by_tier = {}
        for e in DB:
            if e["name"] not in STOCK and tagset & set(e["tags"]):
                by_tier.setdefault(TIER_NAMES_LIST.index(e["tier"]), []).append(e["name"])
        _pools[key] = by_tier
    return _pools[key]


TIER_NAMES_LIST = [t[0] for t in TIERS]


def roll_drop(tags, level):
    """Pick an item matching any of the tags; tier odds improve with quest level."""
    by_tier = _pool(tags)
    if not by_tier:
        return None
    tiers = list(by_tier)
    weights = [TIER_BASE_WEIGHT[i] * (1 + LEVEL_BOOST * level) ** i for i in tiers]
    tier = _random.choices(tiers, weights)[0]
    return _random.choice(by_tier[tier])
