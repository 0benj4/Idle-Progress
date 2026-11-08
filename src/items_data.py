"""300-item database for Idle Progress.

Line format inside the text blocks:
    Name | tags | extra
  - gear (Weapon, Shield, Head, Chest, Legs, Feet): extra = main stat letter
        S=STR  D=DEX  I=INT  V=VIT  L=LCK
  - Loot / Supply: extra = weight (optional, default 1)

Tags say WHERE / WHAT KIND of quest an item may drop in:
    places : dungeon cave mine forest swamp castle sea desert snow city volcano sky
    kinds  : undead beast magic holy demon thief tech absurd

Numbers (bonus, weight, value, level) are computed from tier + slot by build(),
so balance can be changed in one place (the tables below).
"""

TIER_NAMES = ["Basic", "Common", "Uncommon", "Rare", "Mythic"]

# ---- balance tables -------------------------------------------------------
POWER = [2, 4, 7, 11, 17]            # main-stat bonus per tier (before slot factor)
SLOT_FACTOR = {"Weapon": 1.0, "Shield": 0.8, "Chest": 0.9, "Legs": 0.7, "Head": 0.6, "Feet": 0.5}
LEVEL_REQ = [1, 5, 12, 22, 35]       # level needed to equip, per tier
GEAR_WEIGHT = {"Weapon": 3, "Shield": 4, "Head": 2, "Chest": 6, "Legs": 4, "Feet": 2}
TIER_VALUE = [3, 10, 35, 120, 500]   # base gold value per tier
VALUE_FACTOR = {"gear": 1.5, "loot": 1.0, "supply": 0.7}
STAT = {"S": "STR", "D": "DEX", "I": "INT", "V": "VIT", "L": "LCK"}
SECOND = {"STR": "VIT", "DEX": "LCK", "INT": "LCK", "VIT": "STR", "LCK": "DEX"}
EQUIP_SLOT = {"Weapon": "Weapon", "Shield": "Weapon / Shield", "Head": "Head",
              "Chest": "Chest", "Legs": "Legs", "Feet": "Feet"}

# ---- the items ------------------------------------------------------------
DATA = {
"Weapon": {
"Basic": """
Wooden Stick | forest | S
Rusty Dagger | dungeon thief | D
Chipped Club | cave | S
Kitchen Knife | city | D
Bent Spoon | absurd | L
Cracked Wand | magic | I
Frying Pan | city absurd | V
Garden Hoe | forest | S
Sharpened Bone | undead | D
Slingshot | forest | D
""",
"Common": """
Iron Sword | castle | S
Hunting Bow | forest beast | D
Oak Staff | forest magic | I
Miner's Pickaxe | mine | S
Spiked Mace | dungeon | S
Throwing Knives | thief | D
Apprentice Wand | magic | I
Fishing Spear | sea swamp | D
Baguette of Justice | city absurd | S
Squeaky Hammer | absurd | L
""",
"Uncommon": """
Steel Longsword | castle | S
Elven Shortbow | forest | D
Bone Scythe | undead | S
Crystal Wand | cave magic | I
Frost Axe | snow | S
Venom Dirk | swamp thief | D
Rubber Chicken of Doom | absurd | L
Holy Mace | holy | V
""",
"Rare": """
Stormcaller Staff | sky magic | I
Dwarven Warhammer | mine | S
Shadow Blade | thief demon | D
Sunforged Blade | holy desert | S
Lich's Thighbone | undead | I
Giant Trout | sea absurd | S
Runed Longbow | forest magic | D
""",
"Mythic": """
Sword of a Thousand Regrets | demon | S
Staff of the Infinite Library | magic | I
The Last Spoon | absurd | L
Dragonbone Greatsword | volcano | S
Whisper, Bow of Moons | sky forest | D
""",
},
"Shield": {
"Basic": """
Pot Lid | city | V
Wooden Plank | forest | V
Dented Tray | city | V
Cracked Barrel Lid | cave | V
Cardboard Shield | absurd | L
""",
"Common": """
Round Shield | castle | V
Iron Buckler | dungeon | D
Oak Kite Shield | forest | V
Turtle Shell | swamp beast | V
Umbrella | city absurd | L
""",
"Uncommon": """
Tower Shield | castle | V
Bone Wall | undead | V
Mirror Shield | magic | I
Giant Pancake | absurd | V
""",
"Rare": """
Dwarven Bulwark | mine | V
Aegis of Dawn | holy | V
Door of a Haunted House | undead absurd | V
""",
"Mythic": """
Shield of the Last Stand | castle | V
Sunmirror Aegis | sky holy | V
Wall of Infinite Cheese | absurd | V
""",
},
"Head": {
"Basic": """
Cloth Cap | city | V
Leather Hood | forest | D
Bucket Helmet | absurd | V
Straw Hat | forest | L
Rusty Pot Helm | dungeon | V
Wool Beanie | snow | V
Bandana | thief | D
Cracked Skull Cap | undead | V
""",
"Common": """
Iron Helm | castle | V
Chainmail Coif | castle | V
Hunter's Hood | forest beast | D
Miner's Lamp Helmet | mine | V
Wizard Hat | magic | I
Traffic Cone | city absurd | L
Fur Hat | snow | V
Plague Mask | swamp | V
""",
"Uncommon": """
Knight's Great Helm | castle | V
Horned Viking Helm | snow sea | S
Assassin's Cowl | thief | D
Crown of Twigs | forest | L
Skeleton King's Skull | undead | S
Cheese Wheel Hat | absurd | L
""",
"Rare": """
Dwarven Warhelm | mine | V
Archmage's Circlet | magic | I
Halo of Dawn | holy | V
Demon Horns | demon | S
Pirate Captain's Hat | sea | L
""",
"Mythic": """
Crown of the Forgotten King | castle undead | I
Dragonscale Helm | volcano | V
The Hat That Knows | absurd magic | L
""",
},
"Chest": {
"Basic": """
Burlap Sack | city | V
Ragged Tunic | city | V
Leather Vest | forest | D
Barrel (Wearable) | absurd | V
Old Robe | magic | I
Fur Scraps | snow | V
Padded Jerkin | castle | V
Bone Ribcage Vest | undead | S
""",
"Common": """
Chainmail Shirt | castle | V
Hardened Leather | beast | V
Apprentice Robe | magic | I
Miner's Overalls | mine | V
Lumberjack Flannel | forest | S
Clown Suit | absurd | L
Scale Hauberk | swamp | V
Thief's Vest | thief | D
""",
"Uncommon": """
Steel Breastplate | castle | V
Bearskin Coat | snow beast | S
Shadow Cloak | thief | D
Monk's Habit | holy | V
Wizard's Pajamas | magic absurd | I
Ogre-Hide Plate | cave | S
""",
"Rare": """
Dwarven Plate | mine | V
Robes of the Archmage | magic | I
Sunforged Cuirass | holy desert | V
Lich's Burial Shroud | undead | I
Giant Crab Shell | sea | V
""",
"Mythic": """
Dragonscale Mail | volcano | V
Armor of a Thousand Pockets | absurd | L
Vestments of the Void | demon magic | I
""",
},
"Legs": {
"Basic": """
Cloth Pants | city | V
Tattered Shorts | absurd | L
Leather Leggings | forest | D
Wool Trousers | snow | V
Rope Belt Skirt | forest | V
Patched Breeches | city | V
Bone Greaves | undead | S
Loincloth | cave | S
""",
"Common": """
Chain Leggings | castle | V
Hunter's Pants | forest | D
Miner's Trousers | mine | V
Mage Skirt | magic | I
Iron Greaves | dungeon | V
Pajama Bottoms | absurd | L
Swamp Waders | swamp | V
""",
"Uncommon": """
Steel Legplates | castle | V
Shadow Leggings | thief | D
Kilt of Valor | snow | S
Troll-Hide Pants | cave | S
Cursed Pantaloons | demon absurd | L
Fisherman's Waders | sea | V
Skirt of Focus | magic | I
""",
"Rare": """
Dwarven Legguards | mine | V
Archmage Leggings | magic | I
Sunforged Greaves | holy | V
Skeleton Legs | undead | D
Lava-Proof Trousers | volcano | V
""",
"Mythic": """
Dragonbone Greaves | volcano | S
Pants of Infinite Pockets | absurd | L
Legguards of the Eternal March | castle | V
""",
},
"Feet": {
"Basic": """
Bare Foot Wraps | cave | D
Cloth Shoes | city | V
Wooden Clogs | forest | V
Leather Sandals | desert | D
Single Sock | absurd | L
Torn Boots | dungeon | V
Straw Slippers | city | D
Bone Sandals | undead | S
""",
"Common": """
Leather Boots | forest | D
Iron Boots | castle | V
Hunter's Moccasins | beast | D
Miner's Boots | mine | V
Wizard Slippers | magic | I
Rubber Duck Shoes | absurd | L
Snowshoes | snow | V
""",
"Uncommon": """
Steel Sabatons | castle | V
Shadow Boots | thief | D
Swamp Strider Boots | swamp | D
Fur-Lined Boots | snow | V
Sneaky Socks | thief absurd | D
Pilgrim's Sandals | holy desert | V
Pirate Boots | sea | S
""",
"Rare": """
Dwarven Stompers | mine | S
Boots of Swiftness | sky | D
Sunforged Sabatons | holy | V
Lich Slippers | undead | I
Boots of the Ocean Walker | sea magic | D
""",
"Mythic": """
Dragonhide Treads | volcano | V
Boots of 1000 Steps | sky | D
Slippers of the Absolute Couch | absurd | L
""",
},
"Loot": {
"Basic": """
Pebble | cave | 2
Bone | undead
Dirty Rag | city
Bent Nail | dungeon
Cracked Tooth | undead
Dead Beetle | cave
Moldy Bread | dungeon
Broken Arrow | forest
Chicken Feather | forest
Snail Shell | swamp
Burnt Match | city
Rat Tail | dungeon beast
Mud Clump | swamp | 2
Pinecone | forest
Old Button | city
Stale Crumbs | city
Frayed Rope End | sea
Seashell | sea
Cactus Spine | desert
Ice Chip | snow
Soot Flake | volcano
Dull Marble | absurd
Lint Ball | absurd
Broken Quill | castle
Candle Stub | castle
Cobweb | dungeon
Dried Leaf | forest
Rusty Horseshoe | city | 2
Lost Sock | absurd
Wet Newspaper | city absurd
Empty Bottle | city
""",
"Common": """
Torn Cloth | city
Wolf Pelt | forest beast
Spider Silk | dungeon
Goblin Ear | cave
Iron Scrap | mine | 2
Copper Nugget | mine | 2
Bat Wing | cave
Frog Leg | swamp
Snake Skin | desert swamp
Boar Tusk | forest beast
Zombie Finger | undead
Glowing Mushroom | cave
Honeycomb | forest
Fish Scales | sea
Crab Claw | sea
Wolf Fang | forest beast
Dusty Tome Page | castle magic
Silver Spoon | castle
Bone Dice | thief
Lucky Coin (Fake) | thief absurd
Cursed Sock | demon absurd
Candle of Mild Evil | demon
Troll Toenail | cave
Soggy Map | sea
Cracked Lens | tech
""",
"Uncommon": """
Rusty Key | dungeon thief
Silver Ingot | mine | 2
Ghost Dust | undead
Vampire Fang | undead
Imp Horn | demon
Dragon Scale (Small) | volcano
Enchanted Feather | sky magic
Pearl | sea
Ruby Chip | mine
Amber Sap | forest
Spellbook Cover | magic
Treasure Map Piece | thief sea
Golem Core | cave tech | 2
Haunted Doll | undead absurd
Goblin King's Tooth | cave
Fire Salt | volcano
Frost Crystal | snow
Cursed Ring (Slightly) | demon
Mimic Tongue | dungeon
Tiny Clockwork Gear | tech
Singing Rock | cave absurd | 2
""",
"Rare": """
Gold Ingot | mine | 3
Sapphire | mine
Phoenix Feather | volcano sky
Dragon Heart Scale | volcano
Lich's Phylactery Shard | undead
Angel Tear | holy
Demon's Contract (Unsigned) | demon
Cheese of Immense Age | absurd | 2
""",
"Mythic": """
Diamond the Size of a Fist | mine | 3
Dragon's Heart | volcano | 2
Star Fragment | sky
Philosopher's Lunchbox | absurd magic
Crown Jewel of Nowhere | castle
""",
},
"Supply": {
"Basic": """
Torch | dungeon
Rope | dungeon | 2
Water Flask | desert
Bandage | city
Chalk | dungeon
Dry Rations | city
Flint and Steel | forest
Oil Lamp | cave
Candle | castle
Bedroll | forest | 2
Whistle | city absurd
Sack of Nails | mine | 2
""",
"Common": """
Lockpick | thief
Healing Potion | city
Antidote | swamp
Mana Tonic | magic
Smoke Bomb | thief
Grappling Hook | mine | 2
Warm Soup | snow
Whetstone | castle
Net | sea
Squeaky Toy | absurd
""",
"Uncommon": """
Greater Healing Potion | city
Elixir of Vigor | magic
Fire Bomb | volcano
Holy Water | holy
Invisibility Dust | thief
Pocket Sandwich (Eternal) | absurd
""",
"Rare": """
Phoenix Tonic | volcano
Scroll of Teleport | magic
""",
},
}


def build():
    """Turn DATA into a list of item dicts."""
    out = []
    for cat, tiers in DATA.items():
        gear = cat in EQUIP_SLOT
        kind = "gear" if gear else cat.lower()
        for tier, block in tiers.items():
            ti = TIER_NAMES.index(tier)
            for line in block.strip().splitlines():
                parts = [p.strip() for p in line.split("|")]
                name, tags = parts[0], parts[1].split()
                extra = parts[2] if len(parts) > 2 else ""
                e = {"name": name, "tier": tier, "category": cat, "tags": tags}
                if gear:
                    main = STAT[extra]
                    p = max(1, round(POWER[ti] * SLOT_FACTOR[cat]))
                    bonus = {main: p}
                    if ti >= 3:
                        bonus[SECOND[main]] = max(1, p // 2)
                    e.update(slot=EQUIP_SLOT[cat], bonus=bonus, level=LEVEL_REQ[ti],
                             weight=max(1, round(GEAR_WEIGHT[cat] * (1 + 0.15 * ti))))
                else:
                    e["weight"] = int(extra) if extra else 1
                e["value"] = max(1, round(TIER_VALUE[ti] * VALUE_FACTOR["gear" if gear else kind]))
                out.append(e)
    return out


DB = build()
