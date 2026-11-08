@echo off
rem Launcher for Idle Progress on Windows (double-click it, or run it in Windows Terminal).
where py >nul 2>nul && (py -3 "%~dp0src\menu.py" %* & goto :eof)
python "%~dp0src\menu.py" %*
