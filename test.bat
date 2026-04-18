@echo off
REM Test automation batch file for Windows
REM Run unit tests with: test.bat

echo.
echo ===================================
echo Running unit tests...
echo ===================================
echo.

python -m unittest test_game.py -v

echo.
echo ===================================
echo Test run complete!
echo ===================================
pause
