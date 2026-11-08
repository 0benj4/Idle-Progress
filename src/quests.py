"""Quest list used by the game.

The first quest is hand-written with explicit loot. All the others live as plain
text in quests_data.py and quests_pack1..4.py (add a quest by copying a block) and drop items by TAG:
a step drops an item whose tags match the step's tags (or the quest's tags).
Quests are played in order of their level; the list repeats when it ends.

Fields: name, level, tags, steps, step_tags, quest_loot, optional explicit "loot".
  "quest_loot": {"Step": "Quest item"}  given on that step, removed when the quest ends
  "loot": {"Step": ("Item", chance)}    fixed drop (instead of tag drops)
"""
from quests_data import QUESTS_NEW, parse
from quests_pack1 import TEXT as PACK1
from quests_pack2 import TEXT as PACK2
from quests_pack3 import TEXT as PACK3
from quests_pack4 import TEXT as PACK4

PACK_QUESTS = parse(PACK1) + parse(PACK2) + parse(PACK3) + parse(PACK4)

FOUND_THE_RELIC = {
    "name": "Found the Relic",
    "level": 1,
    "steps": [
        "Entering the Dungeon",
        "Fighting skeletons",
        "Pushing stones",
        "Picking the Lock",
        "Stealing the Relic",
        "Running from traps",
        "Walking back to Quest giver",
        "Completing the Quest",
    ],
    "quest_loot": {"Stealing the Relic": "Ancient Relic"},
    "loot": {
        "Fighting skeletons": ("Bone", 0.8),
        "Pushing stones": ("Pebble", 0.5),
        "Picking the Lock": ("Rusty Key", 0.3),
        "Running from traps": ("Torn Cloth", 0.4),
    },
}

# sorted() is stable: equal levels keep their order
QUESTS = sorted([FOUND_THE_RELIC] + QUESTS_NEW + PACK_QUESTS, key=lambda q: q["level"])
