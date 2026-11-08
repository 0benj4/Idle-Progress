"""Character creation screen."""
import curses
import sys

# name: (art lines, short description)
RACES = {
    "Wisp": ([
        "    .   ",
        "   ( )  ",
        "  (. .) ",
        "   \\ /  ",
        "    ~   ",
    ], "A scrap of light from the shadowed forests. No body, plenty of curiosity."),
    "Treant": ([
        "  \\|/  ",
        " -(@@)-",
        "   ||  ",
        "  /||\\ ",
        " /_||_\\",
    ], "A thousand-year-old tree. Walks slowly, but is never in a hurry."),
    "Rat": ([
        " ()_()  ",
        " (o.o)  ",
        " (> <)~ ",
        "  m m   ",
    ], "King of the sewers. Sees an opportunity in every pile of trash."),
    "Slime": ([
        "   ___  ",
        "  /o o\\ ",
        " (  ~  )",
        " '-----'",
    ], "Sticky and bouncy. Has no idea what it just ate."),
    "Plague": ([
        "  .-.   ",
        " (x_x)  ",
        " /|~|\\  ",
        " ~ ' ~  ",
    ], "Disease given form. Nobody dares come near."),
    "Human": ([
        "   O    ",
        "  /|\\   ",
        "  / \\   ",
    ], "Ordinary but stubborn. Lives anywhere, tries everything."),
    "Orc": ([
        "  ,___, ",
        " (>_<)  ",
        " /|W|\\  ",
        " d   b  ",
    ], "Strong, loud and proud. Solves problems with fists."),
    "Wood Elf": ([
        "   /\\   ",
        "  (^.^)>",
        "  /|\\   ",
        "  / \\   ",
    ], "Born among the branches. Silent steps, sharp eyes."),
    "Dark Elf": ([
        "   /\\   ",
        "  (-.-) ",
        "  /|\\ ' ",
        "  / \\   ",
    ], "Graceful shadow of the underground. Forgets nothing, forgives nothing."),
    "Gnome": ([
        "   /\\   ",
        "  /__\\  ",
        "  (oo)  ",
        "  /||\\  ",
    ], "Tiny inventor. Always has a gear in one pocket and explosives in the other."),
    "Dwarf": ([
        "  _^_   ",
        " (o_o)  ",
        " /|=|\\  ",
        "  d b   ",
    ], "Stubborn as rock, greedy as gold. Never leaves the mine."),
    "Shadow": ([
        "  .--.  ",
        " (    ) ",
        " ( .. ) ",
        "  '~~'  ",
        "   ::   ",
    ], "The shadow of a shadow. Vanishes when the light comes on."),
    "Puddle": ([
        "        ",
        "  ~~~~  ",
        " ( o o )",
        "  ~~~~~ ",
    ], "Just a puddle. Its thoughts are always rainy."),
    "Demon": ([
        "  )\\_/( ",
        "  (>_<) ",
        "  /|v|\\ ",
        "   / \\~ ",
    ], "Banished from hell and not very sorry about it."),
    "Panda": ([
        "  (@.@) ",
        "  (  -) ",
        "  /|#|\\ ",
        "  (_ _) ",
    ], "Bamboo, sleep, bamboo. But once angry, nothing can stop it."),
    "Halfling": ([
        "   _    ",
        "  (^_^) ",
        "  /|\\   ",
        "  d b   ",
    ], "Cozy home, warm meal. Adventure? Maybe after dinner."),
    "Bear": ([
        " (\\_/)  ",
        " (O.O)  ",
        " /| |\\  ",
        " d   b  ",
    ], "Big paws, big heart. Absolutely hates hibernating."),
    "Worms": ([
        "  ~~~~~ ",
        " (o)~(o)",
        "  ~~~~  ",
        " ~~  ~~ ",
    ], "Not one worm, a whole bunch! The underground is theirs."),
    "Goblin": ([
        " /\\ /\\ ",
        " (o v o)",
        "  /|$|\\ ",
        "  d   b ",
    ], "Small, green and always scheming. Everything shiny is technically his."),
    "Kobold": ([
        "  ,^,   ",
        " (o.o)  ",
        " /|=|\\~ ",
        "  d b   ",
    ], "A scaly little digger who worships dragons and sets traps for everyone else."),
    "Ghost": ([
        "  .--.  ",
        " ( oo ) ",
        " (    ) ",
        " ^^^^^^ ",
    ], "Died long ago and never got around to leaving. Walks through walls, not through doors."),
    "Mushroom": ([
        "  .--.  ",
        " (o  o) ",
        "  '||'  ",
        "   ||   ",
    ], "A walking mushroom. Smells like rain, spreads like rumor."),
    "Golem": ([
        " [====] ",
        " [o__o] ",
        " /[##]\\ ",
        "  []  [] ",
    ], "Clay and rune. Slow to learn, impossible to break."),
    "Vampire": ([
        "  \\v/   ",
        " (-.-)  ",
        " /|W|\\  ",
        "  / \\   ",
    ], "Elegant, pale, thirsty. Hates garlic, mirrors and early mornings."),
    "Pixie": ([
        " \\ . /  ",
        "  (^.^) ",
        " ~/|\\~  ",
        "   '    ",
    ], "Thumb-sized troublemaker with wings. Sparkle first, apologize never."),
    "Minotaur": ([
        " Y   Y  ",
        " (O_O)  ",
        " /|#|\\  ",
        " d   b  ",
    ], "Half bull, half man, fully lost in every labyrinth he did not build."),
    "Catfolk": ([
        " /\\_/\\  ",
        " (o.o)  ",
        " />^<\\~ ",
        "  d b   ",
    ], "Lands on its feet. Knocks things off tables. Both are on purpose."),
    "Mimic": ([
        " ______ ",
        "|[o  o]|",
        "|\\vvvv/|",
        "|______|",
    ], "Looks like a treasure chest. Is not. Is also a bit sad about that."),
}

STATS = ["STR", "DEX", "INT", "VIT", "LCK"]  # strength, dexterity, intelligence, vitality, luck
BASE_STAT = 5

# race bonuses / penalties
RACE_BONUS = {
    "Wisp":     {"INT": 3, "DEX": 2, "VIT": -2},
    "Treant":   {"VIT": 3, "STR": 2, "DEX": -2},
    "Rat":      {"LCK": 3, "DEX": 2, "STR": -2},
    "Slime":    {"VIT": 3, "LCK": 1, "INT": -2},
    "Plague":   {"VIT": 2, "INT": 2, "LCK": -2},
    "Human":    {"STR": 1, "DEX": 1, "INT": 1, "VIT": 1, "LCK": 1},
    "Orc":      {"STR": 3, "VIT": 1, "INT": -2},
    "Wood Elf": {"DEX": 3, "LCK": 1, "VIT": -1},
    "Dark Elf": {"INT": 2, "DEX": 2, "VIT": -2},
    "Gnome":    {"INT": 3, "LCK": 1, "STR": -2},
    "Dwarf":    {"VIT": 2, "STR": 2, "DEX": -2},
    "Shadow":   {"DEX": 3, "INT": 1, "VIT": -2},
    "Puddle":   {"LCK": 3, "STR": -2},
    "Demon":    {"STR": 2, "INT": 2, "LCK": -2},
    "Panda":    {"VIT": 3, "STR": 1, "DEX": -1},
    "Halfling": {"LCK": 3, "DEX": 1, "STR": -1},
    "Bear":     {"STR": 3, "VIT": 2, "DEX": -2, "INT": -1},
    "Worms":    {"VIT": 2, "LCK": 1, "DEX": 1, "STR": -2},
    "Goblin":   {"LCK": 3, "DEX": 2, "VIT": -2},
    "Kobold":   {"DEX": 2, "INT": 2, "STR": -2},
    "Ghost":    {"INT": 3, "DEX": 1, "VIT": -2, "STR": -1},
    "Mushroom": {"VIT": 3, "LCK": 1, "DEX": -2},
    "Golem":    {"VIT": 4, "STR": 2, "DEX": -3, "INT": -1},
    "Vampire":  {"STR": 2, "INT": 2, "DEX": 1, "VIT": -1, "LCK": -1},
    "Pixie":    {"DEX": 3, "LCK": 2, "INT": 1, "STR": -3},
    "Minotaur": {"STR": 4, "VIT": 1, "INT": -3},
    "Catfolk":  {"DEX": 3, "LCK": 2, "VIT": -2},
    "Mimic":    {"LCK": 3, "VIT": 2, "INT": -2},
}


def bonus_text(race):
    b = RACE_BONUS[race]
    return "  ".join(f"{v:+d} {k}" for k, v in b.items())


def final_stats(race, cls=None):
    """Base 5 + race bonus + class bonus."""
    from classfx import stat_bonus
    b, cb = RACE_BONUS[race], stat_bonus(cls)
    return {k: BASE_STAT + b.get(k, 0) + cb.get(k, 0) for k in STATS}


NAMES = list(RACES)
MAX_NAME = 16


# Rare symbols that some Windows fonts draw as empty boxes get plain look-alikes there.
WIN_GLYPHS = str.maketrans({"ᚱ": "R", "ᚦ": "P", "ᚠ": "F", "♪": "o", "♫": "o", "✔": "v"})


def put(win, y, x, text, attr=0):
    if sys.platform == "win32":
        text = text.translate(WIN_GLYPHS)
    h, w = win.getmaxyx()
    if 0 <= y < h and 0 <= x < w:
        try:
            win.addstr(y, x, text[: w - x - 1], attr)
        except curses.error:
            pass


def wrap(text, width):
    lines, cur = [], ""
    for word in text.split():
        if len(cur) + len(word) + 1 > width and cur:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    if cur:
        lines.append(cur)
    return lines


def create_character(stdscr, prefill=None):
    """Returns {'name','race'} or None if cancelled."""
    curses.curs_set(0)
    green = curses.color_pair(1)
    sel_attr = curses.color_pair(2) | curses.A_BOLD
    name = prefill["name"] if prefill else ""
    race = NAMES.index(prefill["race"]) if prefill else 0
    focus = "race" if prefill else "name"  # name | race
    top = 0

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        put(stdscr, 1, 3, "CREATE CHARACTER", green | curses.A_BOLD)

        # Name box
        box_attr = curses.A_BOLD if focus == "name" else curses.A_DIM
        cursor = "_" if focus == "name" else ""
        put(stdscr, 3, 3, "Name:", box_attr)
        put(stdscr, 3, 10, f"[ {name}{cursor}".ljust(10 + MAX_NAME + 1) + " ]", box_attr)

        # Race list (scrolling)
        put(stdscr, 5, 3, "Race:", curses.A_BOLD if focus == "race" else curses.A_DIM)
        rows = max(3, h - 10)
        if race < top:
            top = race
        elif race >= top + rows:
            top = race - rows + 1
        for i in range(top, min(len(NAMES), top + rows)):
            y = 6 + i - top
            label = f" {NAMES[i]:<12}"
            if i == race:
                put(stdscr, y, 3, ("> " if focus == "race" else "* ") + label.strip().ljust(12),
                    sel_attr if focus == "race" else curses.A_BOLD)
            else:
                put(stdscr, y, 3, "  " + label.strip())
        if top > 0:
            put(stdscr, 5, 18, "▲", curses.A_DIM)
        if top + rows < len(NAMES):
            put(stdscr, 6 + rows, 18, "▼", curses.A_DIM)

        # Preview
        art, desc = RACES[NAMES[race]]
        px = 28
        put(stdscr, 5, px, NAMES[race].upper(), green | curses.A_BOLD)
        for j, line in enumerate(art):
            put(stdscr, 7 + j, px + 2, line, green)
        dlines = wrap(desc, max(20, min(44, w - px - 3)))
        for j, line in enumerate(dlines):
            put(stdscr, 8 + len(art) + j, px, line)
        by = 9 + len(art) + len(dlines)
        put(stdscr, by, px, "Race bonus:", curses.A_DIM)
        put(stdscr, by + 1, px, bonus_text(NAMES[race]), curses.A_BOLD)

        # Alt bilgi
        if focus == "name":
            hint = "Type a name   Enter/Down: pick race   Esc: back"
        else:
            hint = "Up/Down: race   Enter: next (class)   Left/Backspace: edit name   Esc: back"
        put(stdscr, h - 2, 3, hint, curses.A_DIM)
        stdscr.refresh()

        try:
            key = stdscr.get_wch()
        except curses.error:
            continue

        if key == "\x1b":
            return None
        if focus == "name":
            if key in ("\n", "\r", curses.KEY_ENTER, curses.KEY_DOWN, "\t"):
                if name.strip():
                    focus = "race"
            elif key in (curses.KEY_BACKSPACE, "\x7f", "\b"):
                name = name[:-1]
            elif isinstance(key, str) and key.isprintable() and len(name) < MAX_NAME:
                name += key
        else:
            if key == curses.KEY_UP:
                race = (race - 1) % len(NAMES)
            elif key == curses.KEY_DOWN:
                race = (race + 1) % len(NAMES)
            elif key in (curses.KEY_LEFT, curses.KEY_BACKSPACE, "\x7f", "\b"):
                focus = "name"
            elif key in ("\n", "\r", curses.KEY_ENTER):
                return {"name": name.strip(), "race": NAMES[race]}
