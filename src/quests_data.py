"""Quest text. One block per quest, blocks separated by a blank line.

First line of a block:   Quest name | recommended level | tags
Every other line = one step:   Step text | tags (optional) | @Quest item (optional)
  - step tags narrow the drop pool for that step (otherwise the quest tags are used)
  - @Quest item is handed to the character on that step and taken away when the quest ends

Tags: dungeon cave mine forest swamp castle sea desert snow city volcano sky
      undead beast magic holy demon thief tech absurd
"""

QUEST_TEXT = """
Rescue the Mayor's Cat | 1 | city dungeon
Accepting the Mayor's request
Searching the back alleys | city
Climbing into the sewers | dungeon
Fighting giant sewer rats | dungeon beast
Negotiating with the cat | absurd | @Angry Cat
Carrying the angry cat home
Collecting the reward

Fetch the Baker's Sourdough Starter | 2 | city forest
Taking the baker's order
Walking to the old mill | forest
Fighting angry geese | beast
Crossing the creaky bridge
Sniffing out the starter | @Sourdough Starter
Escaping the bread mold
Hurrying back before it rises | city
Receiving a loaf as payment

Clear the Rat King's Cellar | 3 | dungeon beast
Reading the wanted poster
Descending the cellar stairs | dungeon
Lighting a damp torch
Fighting a hundred rats | beast
Squeezing through a tiny tunnel
Challenging the Rat King | @Rat King's Crown
Surviving the Rat King's speech
Carrying out the crown

Escort the Nervous Merchant | 3 | city forest thief
Meeting the shaking merchant
Loading too many crates | city
Walking the forest road | forest
Ambushed by bandits | thief
Negotiating a cheaper robbery
Calming the merchant down | @Merchant's Lucky Charm
Receiving a modest tip

Find the Lost Wedding Ring | 4 | swamp
Consoling the weeping groom
Boarding a leaky boat | swamp
Poking the mud with a stick
Fighting a ring-stealing frog | beast
Asking the heron politely
Digging through the reeds | @Wedding Ring
Washing the ring clean
Arriving just in time for the vows

Banish the Poltergeist Landlord | 4 | undead city
Reading the haunted lease
Climbing to the attic | undead
Dodging flying furniture
Hiding under the bed from ghost hands
Arguing about the rent | absurd
Finding his unpaid tombstone | undead
Burying the overdue rent | @Landlord's Ledger
Signing the exorcism papers | holy
Moving out immediately

Harvest Moonberries | 5 | forest magic
Packing a very large basket
Waiting for the moon to rise
Sneaking into the glowing grove | forest magic
Shooing sleepy fairies
Napping inside a mushroom ring
Picking the silver berries | @Basket of Moonberries
Fighting a jealous owl | beast
Resisting a taste
Delivering the berries to the alchemist

Defend the Scarecrow | 5 | forest absurd
Meeting the very proud scarecrow
Building a fence nobody asked for
Hiding in the cornfield | forest
Teaching the scarecrow to wave
Fighting a murder of crows | beast
Mending the scarecrow's hat | @Scarecrow's Hat
Out-staring a giant crow | absurd
Winning the harvest festival
Accepting a handshake of straw

Mine the Singing Crystal | 6 | mine cave
Hiring a grumpy dwarf
Entering the old mine | mine
Following the humming sound | cave
Pushing a runaway cart
Fighting cave spiders | beast
Crossing a wobbly plank
Arguing with the dwarf about snacks
Chipping out the crystal | @Singing Crystal
Escaping the cave-in | mine
Selling it as music

Steal the Duke's Wig | 6 | castle thief absurd
Studying the Duke's schedule
Disguising yourself as a servant | thief
Walking into the castle | castle
Bluffing past the guards
Carrying a tray of tiny sandwiches | absurd
Sneaking into the bedroom | thief
Lifting the powdered wig | @Duke's Wig
Dodging the Duke's poodles | beast
Hiding inside a suit of armor
Leaving through the laundry chute

Cure the Sneezing Plague | 7 | city swamp
Handing out tiny handkerchiefs
Visiting the sneezing quarter | city
Interviewing a sniffling doctor
Collecting swamp pollen samples | swamp
Fighting angry pollen clouds | swamp
Brewing a bitter cure | magic
Testing it on a brave rat | @Sneeze Cure
Spreading the cure through town
Sneezing once for good luck

Hunt the Giant Boar | 7 | forest beast
Following giant hoofprints
Setting a pit trap | forest
Waiting in a bush for hours
Fighting a startled badger | beast
Spotting the giant boar
Falling into your own trap
Wrestling the boar | @Boar's Golden Tusk
Being chased up a tree
Climbing down very slowly
Carrying home the tusk

Cleanse the Haunted Swamp | 8 | swamp undead
Buying overpriced mud boots | city
Wading into the swamp
Fighting zombie frogs | swamp undead beast
Avoiding the quicksand
Losing a boot to the mud
Finding the witch's hut | swamp magic
Fighting the witch's cat | beast
Arguing with the witch | magic demon absurd
Breaking the curse | holy magic | @Sealed Curse Jar
Cleaning the muck off
Wading back out

Escort the Grumpy Ghost Home | 8 | undead
Finding the lost ghost
Listening to his many complaints | absurd
Floating through the graveyard | undead
Fighting grave robbers | thief
Crossing a haunted crossroads
Finding his old house
Opening the rusty door | @Ghost's Door Key
Tucking him in his coffin | undead
Receiving a ghostly thank-you

Chart the Lost Cave | 9 | cave dungeon
Buying a very big roll of paper
Entering the narrow mouth | cave
Counting the stalagmites
Fighting giant bats | beast
Crossing an underground lake
Getting lost in a side tunnel
Meeting a blind cave troll
Befriending the troll with fish
Finding the sparkling chamber | @Finished Cave Map
Ducking under a falling stalactite
Drawing your way out | dungeon

Retrieve the Pirate's Treasure Map | 10 | sea thief
Boarding a suspicious ship | sea
Learning pirate vocabulary
Scrubbing the deck for cover
Fighting seagulls on deck | beast
Picking the captain's lock | thief
Hiding in a rum barrel
Swiping the map | @Pirate's Treasure Map
Being chased through the rigging | sea
Fencing the first mate
Jumping off the plank | sea
Swimming to the shore

Guard the Caravan Across the Dunes | 10 | desert
Loading the grumpy camels
Crossing the burning sand | desert
Getting lost for a day
Arguing with a spitting camel | beast
Fighting scorpion raiders | beast
Finding a hidden oasis
Haggling with an oasis merchant
Dodging a sandstorm
Delivering the spices | @Caravan Seal
Counting the missing camels
Spitting out the sand

Free the Imprisoned Bard | 11 | castle dungeon
Hearing a sad song at the tavern
Sneaking into the dungeon | dungeon
Dodging jailer patrols | castle
Stealing the cell keys | thief
Fighting the jailer's dog | beast
Unlocking the wrong cell
Unlocking the Bard's cell | @Bard's Lute
Escaping with terrible singing
Fleeing over the castle wall | castle
Getting a song written about you

Defeat the Troll Under the Bridge | 11 | cave beast
Reading the toll notice
Paying three copper coins
Arguing over the toll price | absurd
Fighting the troll's goats | beast
Solving the troll's riddle
Failing the troll's second riddle
Knocking the troll into the river | @Troll's Toll Chest
Collecting back the toll
Crossing the bridge for free

Brew the Potion of Mild Heroism | 12 | magic forest
Reading a smudged recipe
Picking fresh moss | forest
Hunting for rare newt eyes | swamp
Boiling a mysterious cauldron | magic
Stirring clockwise only
Adding a pinch of cheese | absurd
Surviving the small explosion
Scraping the ceiling clean
Bottling the potion | @Potion of Mild Heroism
Feeling slightly braver
Feeling slightly sick

Win the Great Cheese Rolling Race | 12 | absurd forest
Practicing downhill falling
Greasing your boots | forest
Chasing the cheese wheel
Tripping on a rival | absurd
Dodging a runaway goat | beast
Tumbling past the finish line | @Golden Cheese Wheel
Arguing about the photo finish
Celebrating with a bandage
Eating the trophy

Sabotage the Goblin War Machine | 13 | tech cave
Spying on the goblin workshop | cave
Sneaking past noisy gears | tech
Fighting oil-soaked goblins | beast
Hiding in a crate of bolts
Climbing the tin tower
Sliding through a steam pipe | tech
Removing the main bolt | @Goblin Master Bolt
Fighting the goblin foreman | beast
Pulling the emergency lever
Escaping the exploding steam | tech
Watching the machine fold

Rescue the Frozen Explorer | 13 | snow
Bundling up in three coats
Trudging through the snow | snow
Fighting an angry yeti | beast
Finding frozen footprints
Sliding down an ice slope | snow
Digging out a snow cave
Chipping the explorer from ice | @Frozen Explorer's Journal
Warming him with soup
Carrying him through the blizzard | snow
Sliding back down the slope | snow
Receiving his strange diary

Return the Stolen Church Bell | 14 | holy city thief
Hearing the silent morning
Questioning the shifty altar boy | city
Following the muffled ringing | thief
Breaking into the old warehouse
Dodging warehouse guard dogs | beast
Confronting the bell thieves | thief
Winning a bell-tug contest
Lugging the huge bell home | @Church Bell
Dragging it up the church steps | holy
Hanging it back up | holy
Ringing it twice for luck

Duel the Skeleton Knight | 14 | undead castle
Receiving a glove to the face
Practicing against a scarecrow
Riding to the haunted keep | castle
Dodging cursed arrows | undead
Fighting the bone squires | undead
Accepting the duel
Losing the first round
Breaking his ribs, politely | @Skeleton Knight's Gauntlet
Helping him put himself back together
Receiving a respectful bow

Tame the Wild Chicken | 15 | absurd beast
Studying the chicken's habits
Preparing delicious corn | absurd
Chasing it across the farm
Fighting a rival rooster | beast
Climbing the barn roof
Falling off the barn roof
Winning its trust | @Tamed Chicken's Egg
Riding it home
Learning it lays golden eggs

Seal the Demon Portal | 15 | demon holy
Reading the dusty ritual book
Gathering holy water | holy
Walking into the cursed ruins | demon
Fighting minor imps | demon
Climbing a crumbling altar
Drawing the sealing circle | magic
Holding off a pit fiend | demon
Reciting the closing words | @Portal Keystone
Pushing the portal shut
Waving goodbye to the screaming
Cleaning the scorch marks

Dive for the Sunken Crown | 16 | sea
Holding a very deep breath
Diving beneath the waves | sea
Meeting a polite octopus
Fighting hungry sharks | beast
Slipping into the shipwreck
Opening a squeaky hatch
Fighting a grumpy crab king | beast
Prying open the old chest | @Sunken Crown
Dodging an annoyed eel
Racing a rising bubble
Surfacing with dignity

Crack the Wizard's Locked Tower | 16 | magic castle
Staring at the endless stairs
Answering the talking door | magic
Climbing one thousand steps | castle
Resting on step 412
Fighting enchanted brooms
Solving a mirror puzzle
Defeating a cranky gargoyle | magic
Climbing nine hundred more steps
Opening the final lock | @Wizard's Master Key
Waking the sleeping wizard
Dodging a surprise spell
Apologizing for the dust
Taking the lift down

Fix the Dwarves' Broken Elevator | 17 | mine tech
Listening to the dwarves argue
Descending by rope instead | mine
Inspecting the rusty gears | tech
Fighting cave rats | beast
Replacing the cracked pulley
Pulling a stuck dwarf from a duct
Fighting a rock worm | beast
Oiling every creaky part | @Elevator Control Lever
Testing it with a goat
Testing it with a dwarf
Riding up in style

Survive the Vampire's Dinner Party | 17 | undead castle absurd
Dressing very formally
Arriving at the dark manor | castle
Hiding the garlic
Making polite small talk | absurd
Refusing the "special" soup
Sitting next to the creepy cousin
Dancing a very slow waltz
Fighting the butler bats | undead
Escaping through the dessert table | @Vampire's Invitation
Dodging a flying candelabra
Running from the host
Leaving before sunrise

Climb the Giant Beanstalk | 18 | sky forest
Planting one suspicious bean
Watching it grow overnight | forest
Climbing past the clouds | sky
Fighting sky crows | beast
Resting on a fluffy cloud
Dodging a rain of acorns
Crossing a bridge of vines
Sneaking into the giant's kitchen | @Giant's Golden Bean
Hiding in a teapot
Dodging a giant spoon
Fighting a hungry goose | beast
Chopping the stalk down
Landing in a haystack

Smuggle Cheese Past the Border | 18 | thief absurd
Packing cheese in your coat
Wearing a fake mustache | absurd
Approaching the border post
Bribing a sleepy guard | thief
Hiding in a hay cart
Switching to a hollow barrel
Sweating through the inspection | @Contraband Cheese
Distracting a sniffer dog | beast
Selling it at triple price
Hiding from the cheese police

Awaken the Sleeping Golem | 19 | cave tech
Finding the dusty cave
Cleaning ancient dust | cave
Reading runes on its head | magic
Pushing it with all your might
Fighting its stone guardians
Climbing the golem's arm
Replacing a missing rune | magic
Inserting the missing core | @Golem Core Key
Dodging its first big step | tech
Calming the golem down
Befriending a giant rock
Taking it for a walk

Deliver the Dragon's Pizza | 20 | volcano absurd
Receiving the hot pizza box | city | @Hot Pizza Box
Riding a rattling cart
Climbing the volcano
Dodging lava geysers
Crossing a bridge of cooling rock
Fighting fire imps | volcano demon
Keeping the pizza level
Bribing the dragon's doorman | thief absurd
Delivering the pizza
Arguing about the tip | absurd
Running from the dragon | volcano sky
Checking you still have eyebrows
Writing a one-star review

Cross the Frozen Wastes | 21 | snow beast
Packing too much firewood
Marching into the blizzard | snow
Losing a boot in the drift
Fighting ice wolves | beast
Sheltering in a frozen cave
Sharing a cave with a bear | beast
Chasing runaway snow goats
Crossing a cracking ice sheet | snow
Finding the lost signal fire | @Frozen Beacon
Fighting a frost giant | beast
Lighting the beacon
Digging out of an avalanche | snow
Arriving, slightly frozen

Rob the Floating Bank | 22 | sky thief
Booking a cloud-top flight | sky
Disguising yourself as a coin
Sneaking past flying guards | thief
Hiding in a deposit box
Cracking the sky vault
Fighting the vault golems | tech
Filling your bag with gold | @Sky Vault Key
Setting off the alarm
Escaping through the ventilation
Fighting a flying clerk | beast
Parachuting out with an umbrella | sky
Landing in a haystack

Pacify the Angry Volcano | 23 | volcano
Wearing fireproof pants
Climbing the smoking slopes | volcano
Fighting lava slimes | beast
Throwing offerings into the crater
Crossing a river of lava
Befriending a fire spirit | magic
Singing it a lullaby | absurd
Dodging falling boulders
Fighting a magma elemental | volcano
Placing the cooling stone | @Cooling Stone
Running as it grumbles
Watching it go back to sleep

Host the Goblin Tea Party | 24 | cave absurd
Sending polite invitations
Preparing tiny sandwiches | absurd
Decorating a muddy cave | cave
Greeting goblin nobles
Refereeing the biscuit fight
Stopping a cup-juggling duel
Calming the goblin chef
Serving the king his tea | @Goblin King's Teacup
Surviving the toasts
Escaping the group hug
Cleaning up a lot of crumbs

Slay the Lich of the Library | 25 | undead magic
Entering the dusty library | magic
Whispering to avoid shushing
Fighting animated books | undead
Climbing the tallest shelf
Dodging cursed bookmarks
Crossing the Forbidden Section | magic
Fighting the skeleton librarians | undead
Solving the lich's riddle
Fighting the Lich of the Library | undead magic
Breaking the phylactery | @Lich's Phylactery
Fleeing the collapsing shelves
Returning the overdue books
Paying the lich's late fee

Negotiate with the Demon Lawyer | 26 | demon absurd
Entering a brimstone office | demon
Waiting in the endless lobby
Reading the endless contract
Spotting the tricky clause | absurd
Hiding behind a stack of papers
Offering a counter-proposal
Fighting the paper imps | demon
Objecting to everything
Signing in invisible ink | @Demon's Fine Print
Escaping the lawsuit
Fighting a hellhound bailiff | beast
Framing the loophole

Retrieve the Angel's Lost Harp | 27 | holy sky
Hearing a sad celestial hum
Ascending the golden stairs | holy
Politely entering the heavens | sky
Fighting grumpy cherubs
Crossing the cloud bridge
Getting lectured by a saint
Following a trail of feathers
Finding the harp in a tree | @Angel's Harp
Fighting a jealous seraph | holy
Plucking one string by mistake
Falling through a cloud
Returning it with an apology

Plunder the Kraken's Pantry | 28 | sea beast
Sailing into the dark storm | sea
Convincing the crew to continue
Bailing out the leaking ship
Throwing rope at a giant tentacle | beast
Boarding the Kraken's lair
Hiding from the Kraken's cook
Fighting the cook's sea rats | beast
Opening the giant fridge
Snatching a barrel of calamari | @Kraken's Pantry Key
Fighting the Kraken | sea beast
Escaping on a stolen sail
Crossing a whirlpool | sea
Reaching shore with a big feast

Defend the Castle From Pigeons | 29 | castle absurd beast
Studying the pigeon menace
Manning the castle walls | castle
Loading the bread cannon | absurd
Repelling the first wave | beast
Patching the leaky roof
Fighting the pigeon general
Surviving a dropping barrage
Cleaning the battlements
Fighting the second wave | beast
Raising the white flag of corn | @Pigeon General's Feather
Signing the peace treaty
Hosting a victory feast
Regretting the bread cannon

Investigate the Missing Socks | 30 | absurd city
Interviewing a one-socked victim
Searching the laundry district | city
Following a trail of lint
Questioning a suspicious drawer
Fighting a sock-eating washing machine | absurd
Dodging runaway buttons
Discovering the sock dimension
Fighting a giant hairball | beast
Rescuing every lonely sock | @Bag of Lost Socks
Matching them all in pairs
Fighting the Left Sock Gang | thief
Returning them one by one
Closing the case forever

Race the Storm Giants | 31 | sky
Strapping on enchanted boots
Leaping from the cliff | sky
Riding the thunder clouds
Overtaking a lightning bolt
Dodging giant thrown boulders
Fighting a stray thunderbird | beast
Slipping on a wet cloud
Cutting through a hailstorm
Trading shoves with a giant
Crossing the rainbow finish | @Storm Giant's Medal
Tumbling into the mountain
Accepting a rumbling handshake

Raid the Dragon's Dentist | 32 | volcano absurd
Booking an emergency appointment
Reading old dental magazines
Entering the cavern clinic | volcano
Fighting terrified assistants
Climbing a very large tooth | absurd
Sneaking past the drill
Dodging a flying toothbrush
Hiding behind a giant dental chair
Fighting the dentist's dragon guard | volcano beast
Stealing the golden dental tools | @Dragon's Dental Mirror
Running from the roar
Brushing off the ashes
Flossing in victory

Steal the Moon's Reflection | 34 | sky magic thief
Building a ridiculously tall ladder
Climbing toward the night sky | sky
Resting on a passing cloud
Wading in the lunar lake
Fighting moonlight sprites | magic
Dodging the Man in the Moon
Hiding behind a crater
Fighting a lunar wolf | beast
Racing across the dusty plains | sky
Bottling the reflection | @Moon's Reflection
Slipping down a moonbeam | thief
Falling for a very long time
Landing on a soft cloud
Hiding it under the bed

Unseal the Ancient Tomb | 35 | desert undead
Digging in the hot sand | desert
Finding a crooked doorway
Dodging arrow traps | undead
Solving the hieroglyph puzzle
Fighting mummy guards | undead
Crossing a pit of scarabs
Fighting a sand golem | tech
Crawling through a tight tunnel
Solving the second puzzle
Cursing under your breath
Opening the golden sarcophagus | @Pharaoh's Golden Scarab
Waking a very annoyed pharaoh | undead
Outrunning the rolling boulder
Sliding down a sand ramp | desert
Apologizing to the pharaoh

Dethrone the Cheese King | 36 | absurd castle
Marching on the Cheddar Castle | castle
Scaling the wall of brie
Fighting cracker guards | absurd
Crossing the fondue moat
Slicing through a gouda gate
Fighting mold knights | beast
Climbing the spiral staircase
Reaching the throne room
Dodging the court jester
Toppling the Cheese King | @Cheese King's Crown
Surviving his smelly final words
Taking the crown (it smells)
Escaping a stampede of mice | beast
Rolling down the castle hill
Washing away the smell

Banish the Void Beyond the Couch | 38 | demon absurd
Moving the heavy couch | absurd
Staring into the dark gap
Fighting lost coins and crumbs
Fishing out an old remote
Entering the Void Below | demon
Crossing a bridge of dust bunnies
Fighting the Dust Wraiths | demon
Meeting the Lord of Dust
Bargaining for a lost sock
Offering a vacuum cleaner | @Lord of Dust's Vacuum
Surviving the first roar
Banishing him with a sneeze
Climbing back out of the gap
Replacing the couch carefully
Vacuuming everything

Slay the Dragon of Tuesday | 40 | volcano absurd
Waking up on the wrong day
Missing the early train
Climbing the slopes of Tuesday | volcano
Dodging "meeting" fireballs
Fighting the dragon's minions
Surviving a surprise deadline
Crossing a lake of cold coffee
Fighting the Monday Remnants | beast
Reading the dragon's schedule | absurd
Hiding in the breakroom
Fighting the Dragon of Tuesday | volcano beast
Cancelling Tuesday | @Dragon of Tuesday's Calendar
Surviving a final roar
Slipping out unnoticed
Skipping the afternoon
Flying home on a spreadsheet
Enjoying a very early Wednesday

Reassemble the Shattered Star | 42 | sky holy magic
Gathering falling star fragments | sky
Following the glowing trail
Fighting meteor imps | holy
Climbing the highest peak
Crossing a field of falling stars
Pulling a shard from a crater
Fighting a comet serpent | beast
Resting on a quiet moon
Meeting a very old constellation
Fitting the fragments together | magic
Holding it with burning hands
Fighting the Shadow of Night | demon
Mending the final crack | @Whole Star
Lifting it back to the sky
Dodging a tumbling asteroid
Falling back to the world
Watching the night shine again
"""


def parse(text):
    quests = []
    for block in text.strip().split("\n\n"):
        lines = [l.strip() for l in block.strip().splitlines() if l.strip()]
        name, level, tags = [p.strip() for p in lines[0].split("|")]
        q = {"name": name, "level": int(level), "tags": tags.split(),
             "steps": [], "step_tags": {}, "quest_loot": {}}
        for line in lines[1:]:
            parts = [p.strip() for p in line.split("|")]
            step = parts[0]
            q["steps"].append(step)
            for extra in parts[1:]:
                if extra.startswith("@"):
                    q["quest_loot"][step] = extra[1:]
                elif extra:
                    q["step_tags"][step] = extra.split()
        quests.append(q)
    return quests


QUESTS_NEW = parse(QUEST_TEXT)
