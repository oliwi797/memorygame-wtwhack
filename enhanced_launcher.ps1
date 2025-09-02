Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "                 🌟 STAR WARS MEMORY GAME LAUNCHER 🌟              " -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "Welcome to the Enhanced Memory Game Experience!" -ForegroundColor Green
Write-Host ""

Write-Host "🎮 AVAILABLE GAME VERSIONS:" -ForegroundColor Magenta
Write-Host ""

Write-Host "1. 🚀 " -NoNewline -ForegroundColor Yellow
Write-Host "Enhanced GUI Edition" -ForegroundColor Green -BackgroundColor Black
Write-Host "   ✨ Smooth animations & particle effects" -ForegroundColor Gray
Write-Host "   🎨 Professional UI with hover effects" -ForegroundColor Gray
Write-Host "   🎵 Visual feedback & screen shake" -ForegroundColor Gray
Write-Host "   🏆 Combo system & performance ratings" -ForegroundColor Gray
Write-Host "   📊 Advanced statistics tracking" -ForegroundColor Gray
Write-Host ""

Write-Host "2. 🎯 " -NoNewline -ForegroundColor Yellow
Write-Host "Enhanced Console Edition" -ForegroundColor Blue -BackgroundColor Black
Write-Host "   🌈 Rich colors & beautiful typography" -ForegroundColor Gray
Write-Host "   😊 Character emojis & visual themes" -ForegroundColor Gray
Write-Host "   💡 Smart hint system & undo feature" -ForegroundColor Gray
Write-Host "   🎚️ Multiple difficulty levels" -ForegroundColor Gray
Write-Host "   📈 Real-time performance tracking" -ForegroundColor Gray
Write-Host ""

Write-Host "3. 📚 " -NoNewline -ForegroundColor Yellow
Write-Host "Original Versions (Classic)" -ForegroundColor White
Write-Host "   🎮 Original GUI version" -ForegroundColor Gray
Write-Host "   💻 Original console version" -ForegroundColor Gray
Write-Host ""

Write-Host "4. ❌ " -NoNewline -ForegroundColor Red
Write-Host "Exit" -ForegroundColor Red
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan

$choice = Read-Host "`n🎯 Enter your choice (1-4)"

Write-Host ""

switch ($choice) {
    "1" {
        Write-Host "🚀 Launching Enhanced GUI Edition..." -ForegroundColor Green
        Write-Host "✨ Preparing visual effects and animations..." -ForegroundColor Yellow
        Write-Host "🎨 Loading enhanced graphics..." -ForegroundColor Cyan
        Write-Host ""
        Write-Host "⚡ This may take a moment to load character images..." -ForegroundColor Yellow
        Write-Host ""

        & ".\.venv\Scripts\Activate.ps1"
        python enhanced_memory_game.py
    }
    "2" {
        Write-Host "🎯 Launching Enhanced Console Edition..." -ForegroundColor Blue
        Write-Host "🌈 Initializing colorful interface..." -ForegroundColor Magenta
        Write-Host "💡 Preparing smart features..." -ForegroundColor Cyan
        Write-Host ""

        & ".\.venv\Scripts\Activate.ps1"
        python enhanced_text_game.py
    }
    "3" {
        Write-Host "📚 Classic Versions Menu:" -ForegroundColor White
        Write-Host ""
        Write-Host "A. Original GUI Game" -ForegroundColor Green
        Write-Host "B. Original Console Game" -ForegroundColor Blue
        Write-Host ""

        $classic_choice = Read-Host "Choose classic version (A/B)"

        & ".\.venv\Scripts\Activate.ps1"

        if ($classic_choice -eq "A" -or $classic_choice -eq "a") {
            Write-Host "🎮 Starting Original GUI version..." -ForegroundColor Green
            python memory_game.py
        }
        elseif ($classic_choice -eq "B" -or $classic_choice -eq "b") {
            Write-Host "💻 Starting Original Console version..." -ForegroundColor Blue
            python text_memory_game.py
        }
        else {
            Write-Host "Invalid choice. Returning to main menu..." -ForegroundColor Red
        }
    }
    "4" {
        Write-Host "🌟 May the Force be with you! Goodbye! 🌟" -ForegroundColor Yellow
        exit
    }
    default {
        Write-Host "❌ Invalid choice. Please run the launcher again and select 1-4." -ForegroundColor Red
        Read-Host "Press Enter to exit"
    }
}

Write-Host ""
Write-Host "🎊 Thanks for playing! Rate your experience:" -ForegroundColor Cyan
Write-Host "⭐⭐⭐⭐⭐ Jedi Master" -ForegroundColor Green
Write-Host "⭐⭐⭐⭐   Jedi Knight" -ForegroundColor Blue
Write-Host "⭐⭐⭐     Padawan" -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to continue"
