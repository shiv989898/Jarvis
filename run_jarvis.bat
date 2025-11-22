@echo off
echo ========================================
echo JARVIS Launcher
echo ========================================
echo.

echo Starting JARVIS...
C:\Python313\python.exe main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo Error launching JARVIS
    echo ========================================
    echo.
    echo Please make sure:
    echo   1. Python is installed
    echo   2. All dependencies are installed
    echo   3. Run install.ps1 first if you haven't
    echo.
    pause
)
