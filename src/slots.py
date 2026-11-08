"""Save slots: 4 files in the saves/ folder next to src/. Pick, overwrite-confirm and delete."""
import curses
import json
import os
import sys

from character import put

if getattr(sys, "frozen", False):      # the packaged .exe: saves go next to the .exe
    BASE = os.path.dirname(os.path.abspath(sys.executable))
else:                                  # from source: the repo folder (code lives in src/)
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVE_DIR = os.path.join(BASE, "saves")
SLOT_COUNT = 4


def slot_path(i):
    return os.path.join(SAVE_DIR, f"slot{i + 1}.json")


def migrate_old_save():
    """Old single-file save.json becomes slot 1 (only if slot 1 is free)."""
    old = os.path.join(BASE, "save.json")
    os.makedirs(SAVE_DIR, exist_ok=True)
    if os.path.exists(old) and not os.path.exists(slot_path(0)):
        os.replace(old, slot_path(0))


def summary(i):
    """None if empty, else a one-line description."""
    path = slot_path(i)
    if not os.path.exists(path):
        return None
    try:
        with open(path) as f:
            d = json.load(f)
        c, p = d["character"], d.get("progress", {})
        return (f"{c['name']} - {c['race']} {c.get('class', '')}   "
                f"Lv {p.get('level', 1)}   {p.get('done', 0)} quests done")
    except (OSError, ValueError, KeyError):
        return "(unreadable save)"


def delete_slot(i):
    try:
        os.remove(slot_path(i))
    except OSError:
        pass


def confirm(stdscr, text):
    """Y/N prompt on the bottom lines. Returns True on Y."""
    h, w = stdscr.getmaxyx()
    put(stdscr, h - 4, 3, " " * max(0, w - 6))
    put(stdscr, h - 4, 3, f"{text}  (Y / N)", curses.A_BOLD)
    stdscr.refresh()
    while True:
        k = stdscr.getch()
        if k in (ord("y"), ord("Y")):
            return True
        if k in (ord("n"), ord("N"), 27):
            return False


def pick_slot(stdscr, mode):
    """mode 'new' or 'continue'. Returns a slot index, or None if cancelled."""
    green = curses.color_pair(1)
    sel_attr = curses.color_pair(2) | curses.A_BOLD
    sel, msg = 0, ""
    title = "NEW GAME - choose a slot" if mode == "new" else "CONTINUE - choose a slot"
    while True:
        stdscr.erase()
        h, _ = stdscr.getmaxyx()
        put(stdscr, 1, 3, title, green | curses.A_BOLD)
        for i in range(SLOT_COUNT):
            text = summary(i)
            label = f"  Slot {i + 1}   {text if text else '(empty)'}  "
            if i == sel:
                put(stdscr, 4 + i * 2, 3, ">" + label, sel_attr)
            else:
                put(stdscr, 4 + i * 2, 3, " " + label, 0 if text else curses.A_DIM)
        put(stdscr, h - 5, 3, msg, curses.A_BOLD)
        put(stdscr, h - 2, 3, "Up/Down: move   Enter: select   D: delete slot   Esc: back",
            curses.A_DIM)
        stdscr.refresh()

        key = stdscr.getch()
        msg = ""
        if key in (curses.KEY_UP, ord("w"), ord("k")):
            sel = (sel - 1) % SLOT_COUNT
        elif key in (curses.KEY_DOWN, ord("s"), ord("j")):
            sel = (sel + 1) % SLOT_COUNT
        elif key in (27, ord("q")):
            return None
        elif key in (ord("d"), ord("D")):
            if summary(sel) is None:
                msg = "That slot is already empty."
            elif confirm(stdscr, f"Delete slot {sel + 1} forever?"):
                delete_slot(sel)
                msg = f"Slot {sel + 1} deleted."
        elif key in (curses.KEY_ENTER, 10, 13):
            used = summary(sel) is not None
            if mode == "continue":
                if used:
                    return sel
                msg = "That slot is empty - pick a saved game."
            elif not used or confirm(stdscr, f"Slot {sel + 1} is used. Overwrite it?"):
                return sel
