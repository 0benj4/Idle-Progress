# Idle Progress

A tiny **idle RPG that runs in your terminal**. Create a hero, press Enter, and watch them adventure
all by themselves: quests, loot, level-ups, shopping trips, blacksmiths and the occasional
bad day. There is nothing to click and nothing to manage. The only key that matters is `Q`.

Inspired by [Progress Quest](https://progressquest.com/), the classic game that plays itself.

> **Made with AI.** This is a hobby project written together with an AI coding assistant
> ([Claude Code](https://claude.com/claude-code) by Anthropic). I came up with the idea and made
> the design decisions; the AI wrote the code and much of the content (quests, items, jokes), and
> I tested and steered it as it went. Expect rough edges, and please keep that in mind if you
> read or reuse the code.

## What you get

- **28 races and 26 classes.** Races change your starting stats. Classes change how you play:
  each has a stat bonus and its own perks (fewer injuries, more gold, better loot, bigger
  backpack, cheaper shops, luckier events, stronger spells...). The class screen shows them.
- **254 main quests and 35 side quests** made of ordered steps, scaled to your level.
- **300 items**, 180 of them wearable gear in five tiers from Basic to Mythic. The hero wears
  the best piece they are allowed to wear, automatically.
- **Town trips** when the backpack is full or the hero got hurt: sell loot, buy supplies and
  gear upgrades (never Mythic, those only drop), study new spells at the spell school and
  upgrade equipment at the blacksmith (+1 to +10, and the hammer can slip).
- **Gear you cannot use yet is kept**, not sold, if it will be an upgrade soon.
- **22 spells** that you buy as tomes. Casting makes fights safer and gives bonus XP.
- **Random events** that happen along the way (36 of them, mostly nice, sometimes not).
- **4 save slots.** The game saves after every step.

## Run it

You need **Python 3.8 or newer**. It runs on **Linux, macOS and Windows** (in Windows Terminal
or any modern terminal). There is nothing else to install by hand.

```sh
git clone https://github.com/0benj4/Idle-Progress.git
cd Idle-Progress
python3 src/menu.py
```

### Windows

**Easiest: the ready-made `.exe`.** Download `idle-progress.exe` from the
[Releases](../../releases) page, put it in a folder of its own and run it, ideally from
**Windows Terminal** (it needs a wide window, see below). No Python needed. Your characters are
saved in a `saves` folder next to the exe.

> Windows may show a "protected your PC" (SmartScreen) warning because the exe is not
> code-signed: click **More info, then Run anyway**. Some antivirus programs also flag
> apps packaged with PyInstaller by mistake. If you prefer, run it from source instead:

1. Install Python from [python.org](https://www.python.org/downloads/) (tick **"Add python.exe to PATH"**).
2. Download or clone this repo.
3. Open **Windows Terminal** in the folder and run `idle-progress.bat` (or `py src\menu.py`).

Windows has no built-in `curses`, so on the **first run from source the game installs the
[`windows-curses`](https://pypi.org/project/windows-curses/) package for you** (one `pip install`,
no admin rights needed). If that ever fails, run `pip install -r requirements.txt` yourself.

> Windows support is new and has not been tested as much as Linux. If something looks wrong
> (colors, symbols, keys), please open an issue.

### Make an `idle-progress` command

The repo ships a small launcher called `idle-progress`. Pick one of these:

```sh
# Option A: a symlink somewhere on your PATH
ln -s "$(pwd)/idle-progress" ~/.local/bin/idle-progress

# Option B: a shell alias (put it in ~/.bashrc or ~/.zshrc)
alias idle-progress='python3 /full/path/to/Idle-Progress/src/menu.py'
```

Then just type `idle-progress` in any terminal.

## Controls

| Key | Action |
| --- | --- |
| `Up` / `Down` or `W` / `S` | Move in menus |
| `Enter` | Select |
| `Q` or `Esc` | Back to the menu (progress is saved) |

During play there is nothing else to press. That is the whole point.

## Saves

Saves are plain JSON files in the `saves/` folder next to `src/` (`slot1.json` ... `slot4.json`).
They are ignored by git, so your characters never get committed. To start over, delete a slot in
the menu with `D`, or remove the file.

## Project layout

The repo root only has the launchers and docs; all game code lives in `src/`.

| Path | What it is |
| --- | --- |
| `idle-progress`, `idle-progress.bat` | Launchers for Linux/macOS and Windows |
| `src/menu.py` | Main menu and entry point |
| `src/game.py` | The game itself: step logic (`tick`), town trips, drawing |
| `src/character.py`, `classes.py`, `classfx.py` | Races, classes and what each class does |
| `src/items.py`, `items_data.py` | The item database, prices, drops |
| `src/quests*.py`, `sidequests_data.py` | Quest content |
| `src/spells.py`, `events.py`, `slots.py` | Spells, random events, save slots |
| `src/ensure_curses.py` | Installs `windows-curses` on the first run under Windows |
| `saves/` | Your characters (created on first run, never committed) |
| `.github/workflows/` | Builds `idle-progress.exe` on GitHub when a version tag is pushed |

Most balance numbers (prices, chances, caps) are constants near the top of `src/game.py` and
`src/classfx.py`, so tuning the game does not need much code reading.

## Notes

- All in-game text is in English.
- The game is inspired by Progress Quest but shares no code or content with it. It is not
  affiliated with or endorsed by any game or company.

## License

[MIT](LICENSE). Do what you like with it.
