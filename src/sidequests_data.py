"""35 side quests: short, safe (no injury), lower rewards.
Same text format as quests_data.py. Quest items are optional here."""
from quests_data import parse

SIDE_TEXT = """
Feed the Stray Cats | 1 | city beast
Filling a bucket with fish scraps
Walking the back alleys | city
Calling "here, kitty"
Feeding a very fat cat | beast
Getting looked down upon

Polish the Statue | 1 | city
Fetching a bucket and rag
Climbing the stone pedestal
Scrubbing pigeon marks | city
Polishing the hero's nose
Admiring your work | @Statue Polishing Rag

Water the Town Flowers | 2 | city forest
Filling the big watering can
Watering the market flowers | city
Chasing a rabbit from the tulips | beast
Watering the town hall bed
Watering your own boots

Deliver the Baker's Pies | 3 | city
Loading a tray of warm pies
Dodging an excited dog | beast
Delivering the first pie
Delivering the second pie | city
Accepting a pie as a tip | @Baker's Apple Pie

Sweep the Chapel Steps | 4 | holy city
Borrowing a long broom
Sweeping the front steps | holy
Chasing away sparrow nests
Polishing the brass candlesticks
Receiving a quiet blessing

Count the Village Chickens | 5 | forest beast
Walking into the henhouse | forest
Counting twenty-one chickens
Counting twenty-two chickens
Counting them again | beast
Reporting "about twenty"

Carry Water for the Smith | 6 | city tech
Collecting two heavy buckets
Hauling water to the forge | tech
Pouring it over the anvil
Dodging a shower of sparks
Drinking the leftover water | @Smith's Water Ladle

Mend the Fisherman's Nets | 7 | sea
Spreading out tangled nets
Finding twenty-seven holes | sea
Stitching with a big needle
Catching your own sleeve
Hanging the nets to dry | beast

Help the Old Lady Cross the Road | 8 | city absurd
Spotting the old lady
Offering your arm | city
Stopping a runaway cart
Walking very, very slowly
Reaching the other side | absurd
Hearing her life story | @Old Lady's Hard Candy

Sort the Library Returns | 9 | magic city
Opening the return slot
Pulling out a huge stack
Sorting spellbooks by color | magic
Finding a book that bites
Shelving it very carefully

Stack Firewood for Winter | 10 | forest snow
Splitting the first log | forest
Splitting a hundred more
Stacking them in rows
Moving the stack twice
Rubbing your sore back | snow

Walk the Blind Witch's Cat | 11 | magic beast
Meeting a very opinionated cat
Clipping on a tiny leash
Walking in circles | beast
Chasing it up a tree
Returning with scratches | @Witch's Cat Whisker

Paint the Tavern Sign | 12 | city absurd
Choosing a color
Climbing a shaky ladder | city
Painting a smiling mug
Smudging the lettering
Repainting "Tavren" to "Tavern" | absurd
Getting a free drink

Polish the Knights' Armor | 13 | castle
Entering the armory | castle
Scrubbing a helmet
Scrubbing a chestplate
Finding a nest in a boot | beast
Hanging the armor back up

Brew a Batch of Mild Tea | 14 | forest magic
Picking leaves in the garden | forest
Boiling a big kettle
Adding a pinch of magic | magic
Stirring in honey
Pouring a cup for the alchemist | @Mild Tea Leaves

Wash the Dragon's Dishes | 15 | volcano absurd
Entering the dragon's kitchen | volcano
Looking at a mountain of plates
Scrubbing a golden bowl
Fighting a grease monster | absurd
Drying every claw-sized fork
Hearing a tiny burp

Rake the Haunted Garden | 16 | undead forest
Entering the misty garden | forest
Raking dead leaves
Raking more dead leaves
Raking a ghost by accident | undead
Apologizing very sincerely | @Ghostly Garden Rake

Deliver Mail to the Hermit | 17 | forest
Packing a sack of letters
Hiking up a steep trail | forest
Knocking on the hermit's door
Handing over a tax notice
Running before he opens it | beast

Tune the Cathedral Bells | 18 | holy
Climbing the bell tower | holy
Plucking each bell rope
Adjusting a rusty bolt
Hitting the wrong note twice
Ringing perfectly | @Cathedral Bell Rope

Oil the Dwarven Pulleys | 19 | mine tech
Taking a barrel of oil
Entering the lift shaft | mine
Oiling the first pulley | tech
Oiling twenty more
Slipping off a greasy plank
Receiving a gruff nod

Water the Cactus Garden | 20 | desert
Hauling two heavy buckets
Crossing the hot sand | desert
Pouring a single cup
Watching it vanish
Pouring one more cup
Getting poked by a spine | @Cactus Garden Flower

Count the Treasury's Pennies | 21 | castle thief
Sitting in the royal counting room | castle
Counting stacks of coins
Losing count at ninety-nine
Starting over from zero | thief
Finding a missing penny
Signing the ledger

Shine the Lighthouse Lens | 22 | sea
Climbing the spiral stairs
Reaching the glass room | sea
Polishing the giant lens
Wiping seagull droppings | beast
Seeing a ship's lantern at sea

Feed the Gargoyles | 23 | castle beast
Carrying a bucket of gravel
Climbing the castle roof | castle
Offering gravel to a gargoyle
Getting a stone-cold stare | beast
Feeding the last one | @Gargoyle's Chewed Gravel

Knit Scarves for Snowmen | 24 | snow absurd
Collecting wool and needles
Knitting a long red scarf | snow
Knitting a longer blue scarf
Dressing the first snowman | absurd
Dressing the last snowman
Hearing them thank you

Re-shelve the Wizard's Potions | 25 | magic
Opening the potion cabinet | magic
Sorting by color
Sorting by smell
Dodging a bubbling flask
Putting a screaming vial in the back

Pet the Three-Headed Puppy | 27 | beast demon
Approaching a giant puppy | demon
Scratching the left head
Scratching the middle head
Scratching the right head | beast
Throwing a burning ball | @Three-Headed Puppy's Collar

Scrub the Sky Bridge | 29 | sky
Tying a safety rope
Climbing onto the bridge | sky
Scrubbing a cloud stain
Chasing a stubborn raincloud
Rinsing with rainwater

Sing to the Grumpy Plants | 31 | forest magic
Entering the glass greenhouse | forest
Singing a soft lullaby
Switching to a rock song | magic
Singing to a grumpy fern
Hearing a grateful rustle | @Greenhouse Seedling

Dust the Sleeping Golems | 33 | cave tech
Entering the statue cave | cave
Dusting the first golem
Dusting its nose | tech
Sneezing loudly
Tiptoeing away from a creaky sound

Fold the Giant's Laundry | 35 | cave absurd
Climbing into a basket the size of a house | cave
Folding a giant sock
Folding a giant sheet | absurd
Matching a giant pair
Getting stuck inside a pillowcase

Wind the Cuckoo Clock of Fate | 37 | tech magic
Climbing up to the great clock | tech
Turning the huge key
Greasing the sacred gears
Chasing a runaway bird | magic
Hearing it cuckoo once | @Cuckoo of Fate Feather

Brush the Cloud Sheep | 39 | sky beast
Climbing onto a fluffy cloud | sky
Brushing the first sheep
Brushing a very shy lamb | beast
Collecting loose wool
Watching them drift away

Straighten the Stars | 41 | sky holy
Floating to the night sky | sky
Nudging a crooked star
Nudging another star
Straightening the Big Dipper | holy
Dusting the North Star | @Straightened Star

Tuck in the Sleeping Titan | 45 | cave absurd
Climbing up a mountainous blanket | cave
Pulling the cover up
Plumping a giant pillow
Singing a rumbling lullaby | absurd
Tiptoeing out on a giant toe | @Titan's Nightcap
"""

SIDE_QUESTS = parse(SIDE_TEXT)
