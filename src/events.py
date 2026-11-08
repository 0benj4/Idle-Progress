"""Random events that can happen after any quest step.

Each event is (kind, text). The game applies the effect and appends it to the text:
  gold+   find gold          gold-  lose a little gold
  xp      gain experience    mana+  mana refills partly      mana-  mana drains
  item    find an item       flavor nothing happens (just a story)
"""

GOOD = [
    ("gold+", "You find a purse in the grass"),
    ("gold+", "A grateful traveler tips you"),
    ("gold+", "A coin glints at the bottom of a puddle"),
    ("gold+", "You win a bet with a suspicious goat"),
    ("gold+", "A dying merchant leaves you his lunch money"),
    ("gold+", "You sell a pretty rock to a collector"),
    ("xp", "A hermit shares an old fighting trick"),
    ("xp", "You study an odd carving on the wall"),
    ("xp", "A wandering bard sings of your deeds"),
    ("xp", "You spot a better way to hold your weapon"),
    ("xp", "A stray dog shows you a shortcut"),
    ("mana+", "A glowing spring refreshes you"),
    ("mana+", "You nap in a patch of moonlight"),
    ("mana+", "A friendly sprite shares its snack"),
    ("item", "You trip over something shiny"),
    ("item", "A crow drops a gift at your feet"),
    ("item", "You find a half-buried chest"),
    ("item", "A wounded stranger rewards your help"),
]

FLAVOR = [
    ("flavor", "A cloud shaped like a sword drifts by"),
    ("flavor", "You hear distant singing and decide not to look"),
    ("flavor", "A squirrel stares at you. You stare back"),
    ("flavor", "You find a signpost with every arrow pointing up"),
    ("flavor", "Somebody left a very nice chair here"),
    ("flavor", "A frog croaks something that sounds like your name"),
    ("flavor", "You meet a knight who is looking for his horse"),
    ("flavor", "A peddler offers you a map. It is of a different place"),
    ("flavor", "The wind smells like toast"),
    ("flavor", "You pass a tavern called The Last Tavern"),
]

BAD = [
    ("gold-", "A pickpocket bumps into you"),
    ("gold-", "You drop your purse in a river"),
    ("gold-", "A toll troll demands a fee"),
    ("gold-", "You pay too much for a 'magic' bean"),
    ("gold-", "A seagull steals a coin. Nobody knows why"),
    ("mana-", "A cursed breeze saps your focus"),
    ("mana-", "A ghost sneezes on you"),
    ("mana-", "You step on a mana-eating mushroom"),
]
