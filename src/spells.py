"""Spells: the names are our own; level / cost / power are tuned here.

level : character level needed to know the spell
cost  : mana spent per cast
power : 1-9 -> how much a cast lowers injury risk and boosts XP in a combat step
"""
from collections import namedtuple

Spell = namedtuple("Spell", "name level cost power")

SPELLS = [
    Spell("Static Zap", 1, 4, 1),
    Spell("Chill Poke", 1, 4, 1),
    Spell("Yawn Cloud", 2, 5, 1),
    Spell("Tiring Glare", 3, 6, 2),
    Spell("Thunder Snap", 4, 8, 2),
    Spell("Cinder Burst", 5, 10, 3),
    Spell("Lullaby Palm", 6, 9, 2),
    Spell("Weakening Whisper", 7, 10, 2),
    Spell("Icicle Dart", 8, 12, 3),
    Spell("Mana Nibble", 9, 10, 2),
    Spell("Hungry Fingers", 10, 14, 3),
    Spell("Runaway Blaze", 11, 14, 3),
    Spell("Swamp Sneeze", 12, 16, 4),
    Spell("Gust Punch", 14, 18, 4),
    Spell("Hex Sponge", 15, 16, 3),
    Spell("Blizzard Tantrum", 17, 22, 5),
    Spell("Robe Ripper", 19, 22, 4),
    Spell("Inferno Parade", 21, 28, 6),
    Spell("Archmage's Bonfire", 23, 30, 6),
    Spell("Sunrise Wrath", 26, 36, 7),
    Spell("Grasp of Rot", 30, 45, 8),
    Spell("Void Bubble", 34, 55, 9),
]


SPELL_BY_NAME = {s.name: s for s in SPELLS}


def known(level):
    """Every spell a character of this level COULD learn (old saves start with all)."""
    return [s for s in SPELLS if s.level <= level]


def price(spell):
    """Gold the spell trainer asks for a tome (Lv 5: 449, Lv 10: 1577, Lv 34: 14k)."""
    return int(25 * spell.level ** 1.8)


def learned_spells(names):
    return [SPELL_BY_NAME[n] for n in names if n in SPELL_BY_NAME]


def best_affordable(spells, mana, cost_mult=1.0):
    """Strongest of the learned spells the character can pay for right now (or None).
    cost_mult is the class discount on mana cost."""
    ok = [s for s in spells if max(1, round(s.cost * cost_mult)) <= mana]
    return max(ok, key=lambda s: (s.power, -s.cost)) if ok else None
