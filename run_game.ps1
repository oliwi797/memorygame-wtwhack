Write-Host "Star Wars Memory Game Launcher" -ForegroundColor Yellow
Write-Host "==============================" -ForegroundColor Yellow
Write-Host ""
Write-Host "Choose your version:" -ForegroundColor Cyan
Write-Host "1. GUI Version (Recommended - with graphics and images)" -ForegroundColor Green
Write-Host "2. Text Version (Console-based)" -ForegroundColor Green
Write-Host "3. Exit" -ForegroundColor Red
Write-Host ""

$choice = Read-Host "Enter your choice (1-3)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "Starting GUI version..." -ForegroundColor Green
        Write-Host "This may take a moment to load character images..." -ForegroundColor Yellow
        Write-Host ""
        & ".\\.venv\\Scripts\\Activate.ps1"
        python memory_game.py
    }
    "2" {
        Write-Host ""
        Write-Host "Starting text version..." -ForegroundColor Green
        Write-Host ""
        & ".\\.venv\\Scripts\\Activate.ps1"
        python text_memory_game.py
    }
    "3" {
        Write-Host "Goodbye!" -ForegroundColor Yellow
        exit
    }
    default {
        Write-Host "Invalid choice. Please try again." -ForegroundColor Red
        Read-Host "Press Enter to continue"
    }
}
