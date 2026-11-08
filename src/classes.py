"""Class selection screen."""
import curses

from character import STATS, final_stats, put, wrap
from classfx import describe, stat_bonus

CLASSES = {
    "Mage": ([
        "   /\\   ",
        "  /__\\  ",
        "  (oo)* ",
        "  /||\\| ",
    ], "Spellbook in hand, brows furrowed. Fire, ice, lightning: all one word away."),
    "Monk": ([
        "   O    ",
        "  \\|/   ",
        "  /|\\   ",
        "  _/ \\_ ",
    ], "Body and mind as one. Hands and feet are weapons, patience is armor."),
    "Paladin": ([
        "  _O_   ",
        " [+|+]  ",
        "  /|\\ ] ",
        "  d b   ",
    ], "Sword of the holy light. The shield never drops against evil."),
    "Warrior": ([
        "   O  / ",
        "  /|]/  ",
        "  / \\   ",
        "  d b   ",
    ], "Sword, shield, stubbornness. Goes in first, comes back last."),
    "Barbarian": ([
        "  \\O/   ",
        "  /|\\ T ",
        "  / \\   ",
        " ~~~~   ",
    ], "Armor? Who needs it. The bigger the rage, the faster the axe."),
    "Druid": ([
        "  \\|/   ",
        "  (^o^) ",
        "  /|\\ Y ",
        "  / \\   ",
    ], "The voice of nature. Turns into a wolf, a bear, sometimes a tree."),
    "Priest": ([
        "   +    ",
        "  (o)   ",
        "  /|\\   ",
        "  /_\\   ",
    ], "Heals and prays. When angry, the prayers get a little harsh."),
    "Cleric": ([
        "   ,+,  ",
        "  (o_o) ",
        "  /|#|\\ ",
        "  d b   ",
    ], "Armored priest. Bandages wounds and breaks heads."),
    "Voodoo King": ([
        "  \\W/   ",
        "  (x x) ",
        "  /|*|\\ ",
        "  ! ! ! ",
    ], "Dolls, bones, curses. Don't worry, he's only acting friendly."),
    "Engineer": ([
        "  [==]  ",
        "  (oo)  ",
        "  /|\\@  ",
        " *-/ \\  ",
    ], "Gears, bolts, steam. Every problem needs a machine, every machine is a problem."),
    "Tunneler": ([
        "  _^_   ",
        "  (o_o) ",
        " T/|\\   ",
        "  d b   ",
    ], "Digs paths underground. Gets richer as he digs, gets lost as he digs."),
    "Batrider": ([
        " ^v^ O  ",
        "  \\/|\\  ",
        "  /\\ /  ",
        "   ~~   ",
    ], "Rides a giant bat. The night sky belongs to him."),
    "Hunter": ([
        "   O )  ",
        "  /|>-> ",
        "  / \\ ) ",
        "  d b   ",
    ], "Arrows, traps, patience. Tracks the prey, then strikes once."),
    "Runemaster": ([
        "  ᚱ ᚦ   ",
        "  (o)   ",
        "  /|\\ᚠ  ",
        "  / \\   ",
    ], "Carves runes into stones, swords and walls. Ancient script obeys him."),
    "Bard": ([
        "  ♪ O   ",
        "  \\|/ ♫ ",
        "  /|\\=  ",
        "  / \\   ",
    ], "Pays debts with stories, gives courage with songs."),
    "Shouter": ([
        "  \\O/   ",
        "  (O)   ",
        " ))/|\\(( ",
        "  / \\   ",
    ], "Shouts. The louder the shout, the more enemies stagger and friends rejoice. The neighbors complain."),
    "Necromancer": ([
        "  _/\\_   ",
        "  (x_x) ",
        "  /|*|\\ ",
        "  ~ ~ ~ ",
    ], "Talks to the dead. They talk back, and they are rude about it."),
    "Rogue": ([
        "  ,--,  ",
        "  (-_-) ",
        "  /|\\-- ",
        "  d b   ",
    ], "Your pockets are lighter before he says hello. Nothing personal."),
    "Alchemist": ([
        "   O  ! ",
        "  /|\\o  ",
        "  / \\u  ",
        " ~~~~~  ",
    ], "Turns lead into gold. Turns gold into smoke. Turns eyebrows into history."),
    "Pirate": ([
        "  _/^\\_ ",
        "  (o-o) ",
        "  /|\\J  ",
        "  d b   ",
    ], "Arr. Loves the sea, rum and maps with an X. Hates stairs."),
    "Ninja": ([
        "  ___   ",
        " (-_-)  ",
        " /|\\*   ",
        "  /\\    ",
    ], "You did not see him. You will not see him. Something is missing from your pocket."),
    "Chef": ([
        "  _O_   ",
        "  (^o^) ",
        "  /|\\ ] ",
        "  d b   ",
    ], "Fights with a ladle and wins with seasoning. Nobody leaves the table hungry."),
    "Beastmaster": ([
        "   O  ^ ",
        "  /|\\(o) ",
        "  / \\ /\\ ",
        "  d b   ",
    ], "Never walks alone. The wolf is loyal, the goose is in charge."),
    "Jester": ([
        " \\^v^/  ",
        "  (^_^) ",
        "  /|\\o  ",
        "  d b   ",
    ], "Jokes at the worst possible moment. Somehow it always works."),
    "Gambler": ([
        "   _    ",
        "  (^_~) ",
        "  /|\\[]  ",
        "  d b   ",
    ], "Never plays the odds. The odds play him. Today is his lucky day, as always."),
    "Samurai": ([
        "   O  / ",
        "  /|\\/  ",
        "  / \\   ",
        "  d b   ",
    ], "Bows before a duel, bows after. In between, there is mostly sword."),
}

NAMES = list(CLASSES)


def choose_class(stdscr, char):
    """Returns the class name, or None on Esc."""
    curses.curs_set(0)
    green = curses.color_pair(1)
    sel_attr = curses.color_pair(2) | curses.A_BOLD
    sel, top = 0, 0

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        put(stdscr, 1, 3, "CHOOSE CLASS", green | curses.A_BOLD)
        put(stdscr, 3, 3, f"{char['name']}  -  {char['race']}", curses.A_BOLD)
        stats = final_stats(char["race"], NAMES[sel])    # race + the highlighted class
        put(stdscr, 4, 3, "  ".join(f"{k} {v}" for k, v in stats.items()), curses.A_DIM)

        rows = max(3, h - 11)
        if sel < top:
            top = sel
        elif sel >= top + rows:
            top = sel - rows + 1
        for i in range(top, min(len(NAMES), top + rows)):
            y = 6 + i - top
            if i == sel:
                put(stdscr, y, 3, f"> {NAMES[i]:<13}", sel_attr)
            else:
                put(stdscr, y, 3, f"  {NAMES[i]}")
        if top > 0:
            put(stdscr, 5, 20, "▲", curses.A_DIM)
        if top + rows < len(NAMES):
            put(stdscr, 6 + rows, 20, "▼", curses.A_DIM)

        art, desc = CLASSES[NAMES[sel]]
        px = 28
        put(stdscr, 5, px, NAMES[sel].upper(), green | curses.A_BOLD)
        for j, line in enumerate(art):
            put(stdscr, 7 + j, px + 2, line, green)
        dlines = wrap(desc, max(20, min(44, w - px - 3)))
        for j, line in enumerate(dlines):
            put(stdscr, 8 + len(art) + j, px, line)
        by = 9 + len(art) + len(dlines)
        bonus = stat_bonus(NAMES[sel])
        put(stdscr, by, px, "Class bonus:", curses.A_DIM)
        put(stdscr, by + 1, px, "  ".join(f"{v:+d} {k}" for k, v in bonus.items()), curses.A_BOLD)
        put(stdscr, by + 3, px, "Perks:", curses.A_DIM)
        for j, line in enumerate(describe(NAMES[sel])):
            put(stdscr, by + 4 + j, px, "- " + line)

        put(stdscr, h - 2, 3, "Up/Down: class   Enter: start   Esc: back", curses.A_DIM)
        stdscr.refresh()

        try:
            key = stdscr.get_wch()
        except curses.error:
            continue
        if key == "\x1b":
            return None
        if key == curses.KEY_UP:
            sel = (sel - 1) % len(NAMES)
        elif key == curses.KEY_DOWN:
            sel = (sel + 1) % len(NAMES)
        elif key in ("\n", "\r", curses.KEY_ENTER):
            return NAMES[sel]
