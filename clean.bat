@echo off
REM Clean up cache files
REM Run with: clean.bat

echo.
echo ===================================
echo Cleaning up cache files...
echo ===================================
echo.

for /d /r . %%d in (__pycache__) do @if exist "%%d" (
    echo Removing %%d
    rmdir /s /q "%%d"
)

for /r . %%f in (*.pyc) do @if exist "%%f" (
    echo Removing %%f
    del /q "%%f"
)

echo.
echo ===================================
echo Cleanup complete!
echo ===================================
pause
