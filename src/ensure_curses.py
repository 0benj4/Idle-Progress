"""Windows has no built-in `curses`. On first run we install the `windows-curses`
package for the player, so the game starts with no manual setup.
Call ensure_curses() before anything imports curses."""
import importlib
import subprocess
import sys

PACKAGE = "windows-curses"


def _in_venv():
    return sys.prefix != getattr(sys, "base_prefix", sys.prefix)


def ensure_curses():
    try:
        import curses  # noqa: F401
        return
    except ImportError:
        pass
    if getattr(sys, "frozen", False):      # packaged .exe: pip cannot help here
        sys.exit("This build is missing its terminal library. Please download the game again.")
    if sys.platform != "win32":
        sys.exit("This game needs Python's 'curses' module, but this Python has none.\n"
                 "Install a Python build that includes it (python3-curses on some distros).")

    print(f"First run: installing '{PACKAGE}' (the terminal UI library for Windows)...")
    cmd = [sys.executable, "-m", "pip", "install", PACKAGE]
    if not _in_venv():
        cmd.insert(4, "--user")      # no admin rights needed
    try:
        subprocess.check_call(cmd)
    except (OSError, subprocess.CalledProcessError):
        sys.exit("\nCould not install it automatically. Please run this yourself:\n"
                 f"    {sys.executable} -m pip install {PACKAGE}\n"
                 "then start the game again.")
    importlib.invalidate_caches()
    try:
        import curses  # noqa: F401
    except ImportError:
        sys.exit(f"'{PACKAGE}' was installed, but Python cannot load it yet.\n"
                 "Please start the game again.")
