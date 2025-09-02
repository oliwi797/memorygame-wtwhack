# 🌟 Star Wars Memory Card Game - Enhanced Edition

A professionally designed memory card flipping game with smooth animations, rich visual feedback, and enhanced user experience. Features both an advanced GUI version and a beautifully designed console version.

## ✨ Enhanced Features

### 🚀 Enhanced GUI Edition
- **Smooth Animations**: Card flip effects with 3D rotation and scaling
- **Particle Effects**: Celebration bursts and visual feedback
- **Professional UI**: Hover effects, glow highlights, and screen shake
- **Smart Statistics**: Real-time performance tracking and combo system
- **Enhanced Loading**: Progress bars and smooth transitions

### 🎯 Enhanced Console Edition  
- **Rich Typography**: Colorful ANSI interface with Star Wars theming
- **Character Emojis**: Visual representation of each character
- **Multiple Difficulties**: Padawan (4x4), Jedi (6x6), Master (hard mode)
- **Smart Features**: Hint system, undo functionality, and combo tracking
- **Beautiful ASCII Art**: Professional console interface design

### 📊 Universal Improvements
- Uses real Star Wars character data and images from the API
- Robust error handling with graceful fallbacks
- Cross-platform compatibility and accessibility features
- Advanced statistics and performance ratings
- Smooth user experience with clear feedback

## Game Rules

1. The game starts with all cards face down
2. Click/select two cards to flip them over
3. If the cards match (same character), they stay face up
4. If they don't match, they flip back over after a short delay
5. Remember the positions to make matches
6. Win when all pairs are matched!

## Requirements

- Python 3.7+
- pygame (for GUI version)
- requests (for API calls)

## Installation

1. Install the required packages:
```bash
pip install pygame requests
```

## How to Run

### 🎮 Enhanced Launcher (Recommended)
**Windows PowerShell:**
```powershell
.\enhanced_launcher.ps1
```

This interactive launcher provides:
- Beautiful interface with descriptions of each version
- Easy selection between enhanced and classic versions
- Automatic environment setup and guidance

### 🎯 Quick Start Options

**Enhanced GUI (Best Visual Experience):**
```powershell
.venv\Scripts\activate; python enhanced_memory_game.py
```

**Enhanced Console (Rich Terminal Experience):**
```powershell
.venv\Scripts\activate; python enhanced_text_game.py
```

**Classic Launcher:**
```powershell
.\run_game.ps1
```

### Manual Execution

First, activate the virtual environment:
```bash
# Windows
.venv\Scripts\activate

# Then run any version:
```

#### 🚀 Enhanced GUI Version (Recommended)
```bash
python enhanced_memory_game.py
```

**Features:**
- Smooth card flip animations with 3D effects
- Particle celebration system
- Hover effects and visual feedback
- Professional color scheme and typography
- Combo system and achievement ratings
- Advanced statistics tracking

#### 🎯 Enhanced Console Version
```bash
python enhanced_text_game.py
```

**Features:**
- Rich ANSI colors and beautiful typography
- Character emojis and themed interface  
- Multiple difficulty levels (Padawan/Jedi/Master)
- Smart hint system and undo functionality
- Real-time performance tracking
- ASCII art and visual polish

#### 📚 Classic Versions
```bash
python memory_game.py      # Original GUI
python text_memory_game.py # Original Console
```

## Controls & Features

### 🚀 Enhanced GUI Version:
- **Left Click**: Flip a card with smooth animation
- **Mouse Hover**: Cards scale up with visual feedback
- **R**: Restart game (when completed)
- **ESC**: Exit game
- **Visual Effects**: Particle celebrations, screen shake, combo indicators

### 🎯 Enhanced Console Version:
- **Coordinate Input**: Type coordinates like A1, B3, etc.
- **hint**: Get smart hints about character locations
- **undo**: Revert your last move
- **quit**: Exit the game at any time
- **Difficulty Selection**: Choose Padawan, Jedi, or Master difficulty
- **Rich Interface**: Colors, emojis, and ASCII art

### 📚 Classic Versions:
- **GUI**: Mouse clicks and keyboard shortcuts
- **Console**: Basic coordinate input and quit command

## API Information

This game uses the Star Wars API (https://akabab.github.io/starwars-api/) to fetch character data including:
- Character names
- Character images (GUI version only)
- Character IDs for matching

If the API is unavailable, the game will fall back to a predefined set of Star Wars characters.

## Technical Details

- **Grid Size**: 6x6 (36 cards)
- **Total Pairs**: 18 pairs of characters
- **API Endpoint**: `https://akabab.github.io/starwars-api/api/all.json`
- **Image Loading**: Dynamic loading from character image URLs
- **Matching Logic**: Based on character ID comparison

## Troubleshooting

1. **Import errors**: Make sure pygame and requests are installed
2. **Slow loading**: Character images are downloaded on startup (GUI version)
3. **API issues**: Game will use fallback characters if API is unavailable
4. **Display issues**: Try the text version if GUI has problems

## Project Structure

```
hackathon/
├── memory_game.py          # GUI version with pygame
├── text_memory_game.py     # Text-based version
├── run_game.bat           # Windows batch launcher
├── run_game.ps1           # PowerShell launcher
├── .venv/                 # Virtual environment
└── README.md              # This file
```

Enjoy the game and may the Force be with you! 🌟
