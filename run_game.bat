@echo off
echo Star Wars Memory Game Launcher
echo ==============================
echo.
echo Choose your version:
echo 1. GUI Version (Recommended - with graphics and images)
echo 2. Text Version (Console-based)
echo 3. Exit
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Starting GUI version...
    echo This may take a moment to load character images...
    echo.
    call .venv\Scripts\activate.bat
    python memory_game.py
) else if "%choice%"=="2" (
    echo.
    echo Starting text version...
    echo.
    call .venv\Scripts\activate.bat
    python text_memory_game.py
) else if "%choice%"=="3" (
    echo Goodbye!
    exit /b 0
) else (
    echo Invalid choice. Please try again.
    pause
    goto :eof
)

pause
