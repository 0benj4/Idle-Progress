#!/usr/bin/env python3
"""Idle Progress - main menu (terminal, curses)."""
from ensure_curses import ensure_curses

ensure_curses()          # on Windows: installs windows-curses on the first run

import curses  # noqa: E402
import json
import locale
import os
import sys

from character import create_character, final_stats
from classes import choose_class
from game import run_game
from slots import migrate_old_save, pick_slot, slot_path

locale.setlocale(locale.LC_ALL, "")

# Title art: change it here.
TITLE = r"""
█████ ████  █     █████
  █   █   █ █     █    
  █   █   █ █     ████ 
  █   █   █ █     █    
█████ ████  █████ █████

████  ████   ███   ████ ████  █████  ████  ████
█   █ █   █ █   █ █     █   █ █     █     █    
████  ████  █   █ █  ██ ████  ████   ███   ███ 
█     █  █  █   █ █   █ █  █  █         █     █
█     █   █  ███   ███  █   █ █████ ████  ████ 
""".strip("\n").split("\n")

SUBTITLE = "~ an idle adventure in your terminal ~"

# (label, action)
ITEMS = [
    ("New Game", "new"),
    ("Continue", "continue"),
    ("Quit", "quit"),
]


def put_center(win, y, text, attr=0):
    h, w = win.getmaxyx()
    if 0 <= y < h:
        x = max(0, (w - len(text)) // 2)
        try:
            win.addstr(y, x, text[: w - 1], attr)
        except curses.error:
            pass


def placeholder(stdscr, name):
    stdscr.erase()
    h, _ = stdscr.getmaxyx()
    put_center(stdscr, h // 2 - 1, f"[ {name} ]", curses.A_BOLD)
    put_center(stdscr, h // 2 + 1, "Not implemented yet. Press any key...")
    stdscr.refresh()
    stdscr.getch()


def main(stdscr):
    migrate_old_save()
    curses.curs_set(0)
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
    green = curses.color_pair(1)
    selected_attr = curses.color_pair(2) | curses.A_BOLD
    sel = 0

    while True:
        stdscr.erase()
        h, _ = stdscr.getmaxyx()
        block = len(TITLE) + 2 + len(ITEMS) * 2 + 2
        y = max(0, (h - block) // 2)

        for line in TITLE:
            put_center(stdscr, y, line, green | curses.A_BOLD)
            y += 1
        put_center(stdscr, y, SUBTITLE, curses.A_DIM)
        y += 3

        for i, (label, _) in enumerate(ITEMS):
            if i == sel:
                put_center(stdscr, y, f"  > {label} <  ", selected_attr)
            else:
                put_center(stdscr, y, label)
            y += 2

        put_center(stdscr, y + 1, "Up/Down or W/S: move   Enter: select   Q: quit", curses.A_DIM)
        stdscr.refresh()

        key = stdscr.getch()
        if key in (curses.KEY_UP, ord("w"), ord("k")):
            sel = (sel - 1) % len(ITEMS)
        elif key in (curses.KEY_DOWN, ord("s"), ord("j")):
            sel = (sel + 1) % len(ITEMS)
        elif key in (ord("q"), 27):
            return
        elif key in (curses.KEY_ENTER, 10, 13):
            action = ITEMS[sel][1]
            if action == "quit":
                return
            if action == "new":
                slot = pick_slot(stdscr, "new")
                if slot is None:
                    continue
                char, cls = None, None
                while True:
                    char = create_character(stdscr, char)
                    if char is None:
                        break
                    cls = choose_class(stdscr, char)
                    if cls:
                        break
                if char and cls:
                    char["class"] = cls
                    char["stats"] = final_stats(char["race"], cls)
                    run_game(stdscr, {"character": char}, slot_path(slot))
            elif action == "continue":
                slot = pick_slot(stdscr, "continue")
                if slot is None:
                    continue
                try:
                    with open(slot_path(slot)) as f:
                        data = json.load(f)
                    data["character"]
                except (OSError, ValueError, KeyError):
                    placeholder(stdscr, "That save could not be read.")
                    continue
                run_game(stdscr, data, slot_path(slot))
            else:
                placeholder(stdscr, ITEMS[sel][0])


def selftest():
    """Headless check used when building the .exe: everything loads, saves are writable."""
    from character import RACES
    from classes import CLASSES
    from classfx import FX
    from items import ITEM_INFO
    from quests import QUESTS
    from slots import SAVE_DIR
    from spells import SPELLS
    assert QUESTS and ITEM_INFO and SPELLS and RACES and set(FX) == set(CLASSES)
    os.makedirs(SAVE_DIR, exist_ok=True)
    probe = os.path.join(SAVE_DIR, ".write-test")
    with open(probe, "w") as f:
        f.write("ok")
    os.remove(probe)
    print(f"selftest ok: {len(QUESTS)} quests, {len(ITEM_INFO)} items, "
          f"{len(RACES)} races, {len(CLASSES)} classes; saves in {SAVE_DIR}")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
        sys.exit(0)
    curses.wrapper(main)
