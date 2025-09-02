import requests
import random
import time
import os
import sys
from datetime import datetime
import re

class Colors:
    """ANSI color codes for enhanced terminal output"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Regular colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'

class EnhancedTextMemoryGame:
    def __init__(self):
        self.grid_size = 6
        self.total_pairs = (self.grid_size * self.grid_size) // 2
        self.board = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.revealed = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.matched = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.characters = []
        self.moves = 0
        self.matches_found = 0
        self.start_time = None
        self.game_time = 0
        self.combo_count = 0
        self.last_match_time = 0
        self.hint_count = 3  # Player gets 3 hints
        self.difficulty = "normal"  # easy, normal, hard
        
        # Game history for better UX
        self.move_history = []
        self.last_revealed = []
        
        # Enable color support on Windows
        if os.name == 'nt':
            os.system('color')
        
        self.show_welcome_screen()
        self.load_characters()
        self.setup_board()
        
    def show_welcome_screen(self):
        """Enhanced welcome screen with ASCII art and options"""
        self.clear_screen()
        print(f"{Colors.BRIGHT_CYAN}{Colors.BOLD}")
        print("╔══════════════════════════════════════════════════════════════════╗")
        print("║                                                                  ║")
        print("║        ⭐ STAR WARS ENHANCED MEMORY GAME ⭐                    ║")
        print("║                                                                  ║")
        print("║    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    ║")
        print("║    ░    🌌 Journey through the galaxy of memory! 🌌    ░    ║")
        print("║    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    ║")
        print("║                                                                  ║")
        print("╚══════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.RESET}")
        
        print(f"\n{Colors.BRIGHT_YELLOW}Choose your difficulty:{Colors.RESET}")
        print(f"{Colors.GREEN}1. 🟢 Padawan (Easy)    - 4x4 grid, extra hints{Colors.RESET}")
        print(f"{Colors.YELLOW}2. 🟡 Jedi (Normal)     - 6x6 grid, some hints{Colors.RESET}")
        print(f"{Colors.RED}3. 🔴 Master (Hard)     - 6x6 grid, no hints{Colors.RESET}")
        
        while True:
            choice = input(f"\n{Colors.BRIGHT_CYAN}Enter your choice (1-3): {Colors.RESET}").strip()
            if choice == "1":
                self.difficulty = "easy"
                self.grid_size = 4
                self.hint_count = 5
                break
            elif choice == "2":
                self.difficulty = "normal"
                self.grid_size = 6
                self.hint_count = 3
                break
            elif choice == "3":
                self.difficulty = "hard"
                self.grid_size = 6
                self.hint_count = 0
                break
            else:
                print(f"{Colors.RED}Invalid choice! Please enter 1, 2, or 3.{Colors.RESET}")
        
        self.total_pairs = (self.grid_size * self.grid_size) // 2
        self.board = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.revealed = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.matched = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        print(f"\n{Colors.BRIGHT_GREEN}Great choice! Loading your {self.difficulty} difficulty game...{Colors.RESET}")
        time.sleep(1.5)
    
    def load_characters(self):
        """Load characters with progress indication"""
        print(f"\n{Colors.BRIGHT_BLUE}🚀 Loading Star Wars characters from a galaxy far, far away...{Colors.RESET}")
        
        # Animated loading
        for i in range(3):
            for char in "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏":
                print(f"\r{Colors.BRIGHT_BLUE}{char} Connecting to the Force...{Colors.RESET}", end="", flush=True)
                time.sleep(0.1)
        
        try:
            response = requests.get("https://akabab.github.io/starwars-api/api/all.json")
            if response.status_code == 200:
                all_characters = response.json()
                if len(all_characters) >= self.total_pairs:
                    self.characters = random.sample(all_characters, self.total_pairs)
                else:
                    self.characters = all_characters[:self.total_pairs]
                print(f"\r{Colors.BRIGHT_GREEN}✅ Successfully loaded {len(self.characters)} characters!{Colors.RESET}")
            else:
                print(f"\r{Colors.YELLOW}⚠️  API connection failed. Using backup characters...{Colors.RESET}")
                self.use_fallback_characters()
        except Exception as e:
            print(f"\r{Colors.YELLOW}⚠️  Connection error. Using backup characters...{Colors.RESET}")
            self.use_fallback_characters()
        
        time.sleep(1)
    
    def use_fallback_characters(self):
        """Enhanced fallback with more characters"""
        fallback_names = [
            "Luke Skywalker", "Princess Leia", "Han Solo", "Chewbacca", "Obi-Wan Kenobi",
            "Darth Vader", "Yoda", "R2-D2", "C-3PO", "Emperor Palpatine",
            "Anakin Skywalker", "Padmé Amidala", "Mace Windu", "Qui-Gon Jinn", 
            "Count Dooku", "General Grievous", "Boba Fett", "Jango Fett", 
            "Rey", "Finn", "Poe Dameron", "Kylo Ren", "BB-8", "Captain Phasma",
            "Ahsoka Tano", "Ezra Bridger", "Kanan Jarrus", "Sabine Wren",
            "Grand Admiral Thrawn", "Director Krennic", "Jyn Erso", "Cassian Andor"
        ]
        
        self.characters = []
        for i in range(min(self.total_pairs, len(fallback_names))):
            self.characters.append({
                'id': i + 1,
                'name': fallback_names[i],
                'homeworld': 'Unknown',
                'species': 'Unknown'
            })
    
    def setup_board(self):
        """Set up board with shuffle animation"""
        print(f"\n{Colors.BRIGHT_MAGENTA}🎲 Shuffling the galaxy...{Colors.RESET}")
        
        # Create pairs
        all_cards = []
        for character in self.characters:
            all_cards.extend([character, character])
        
        # Fill remaining slots if needed
        while len(all_cards) < self.grid_size * self.grid_size:
            all_cards.append({'id': 999, 'name': 'Empty'})
        
        # Animated shuffle
        for i in range(5):
            random.shuffle(all_cards)
            print(f"\r{Colors.BRIGHT_MAGENTA}🎲 Shuffling{'.' * (i + 1)}{Colors.RESET}", end="", flush=True)
            time.sleep(0.3)
        
        # Place on board
        index = 0
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.board[i][j] = all_cards[index]
                index += 1
        
        print(f"\r{Colors.BRIGHT_GREEN}✅ Galaxy shuffled and ready!{Colors.RESET}")
        time.sleep(1)
    
    def clear_screen(self):
        """Clear screen with smooth transition"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_character_emoji(self, name):
        """Get emoji for character based on name"""
        emoji_map = {
            'luke': '👦', 'leia': '👸', 'han': '🤠', 'chewbacca': '🐻', 'chewie': '🐻',
            'obi-wan': '🧙', 'vader': '😈', 'yoda': '👴', 'r2-d2': '🤖', 'c-3po': '🦾',
            'palpatine': '👹', 'emperor': '👹', 'anakin': '👨', 'padme': '👩',
            'mace': '💜', 'qui-gon': '🧙', 'dooku': '🗡️', 'grievous': '🦾',
            'boba': '🚀', 'jango': '🚀', 'rey': '✨', 'finn': '⚔️', 'poe': '✈️',
            'kylo': '😡', 'bb-8': '⚽', 'phasma': '🛡️', 'ahsoka': '⚔️',
            'thrawn': '👽', 'jyn': '🎯', 'cassian': '🔫'
        }
        
        name_lower = name.lower()
        for key, emoji in emoji_map.items():
            if key in name_lower:
                return emoji
        return '👤'  # Default person emoji
    
    def display_board(self):
        """Enhanced board display with colors and better formatting"""
        self.clear_screen()
        
        # Header with game info
        print(f"{Colors.BRIGHT_CYAN}{Colors.BOLD}")
        print("╔" + "═" * 78 + "╗")
        print(f"║{' ' * 20}⭐ STAR WARS MEMORY GAME ⭐{' ' * 21}║")
        print("╚" + "═" * 78 + "╝")
        print(f"{Colors.RESET}")
        
        # Game stats
        current_time = time.time() - self.start_time if self.start_time else 0
        minutes = int(current_time // 60)
        seconds = int(current_time % 60)
        
        difficulty_colors = {
            'easy': Colors.GREEN,
            'normal': Colors.YELLOW,
            'hard': Colors.RED
        }
        
        difficulty_color = difficulty_colors.get(self.difficulty, Colors.WHITE)
        
        print(f"{Colors.BRIGHT_WHITE}📊 Stats: {Colors.RESET}", end="")
        print(f"{Colors.CYAN}Moves: {Colors.BRIGHT_WHITE}{self.moves}{Colors.RESET} | ", end="")
        print(f"{Colors.GREEN}Matches: {Colors.BRIGHT_WHITE}{self.matches_found}/{self.total_pairs}{Colors.RESET} | ", end="")
        print(f"{Colors.YELLOW}Time: {Colors.BRIGHT_WHITE}{minutes:02d}:{seconds:02d}{Colors.RESET} | ", end="")
        print(f"{difficulty_color}Difficulty: {Colors.BRIGHT_WHITE}{self.difficulty.title()}{Colors.RESET}")
        
        if self.hint_count > 0:
            print(f"{Colors.MAGENTA}💡 Hints available: {Colors.BRIGHT_WHITE}{self.hint_count}{Colors.RESET}")
        
        if self.combo_count > 1:
            print(f"{Colors.BRIGHT_YELLOW}🔥 COMBO STREAK: x{self.combo_count}! {Colors.RESET}")
        
        print("─" * 80)
        
        # Column headers with better spacing
        print(f"{Colors.BRIGHT_BLUE}    ", end="")
        for j in range(self.grid_size):
            print(f"{j+1:^12}", end="")
        print(f"{Colors.RESET}")
        
        # Board with enhanced visual design
        for i in range(self.grid_size):
            print(f"{Colors.BRIGHT_BLUE}{chr(65+i):>2}: {Colors.RESET}", end="")
            for j in range(self.grid_size):
                if self.matched[i][j]:
                    # Show matched cards with checkmark and character info
                    name = self.board[i][j]['name']
                    emoji = self.get_character_emoji(name)
                    short_name = (name[:8] + "..") if len(name) > 10 else name
                    print(f"{Colors.BRIGHT_GREEN}✓{emoji}{short_name:<8}{Colors.RESET}", end=" ")
                elif self.revealed[i][j]:
                    # Show temporarily revealed cards
                    name = self.board[i][j]['name']
                    emoji = self.get_character_emoji(name)
                    short_name = (name[:8] + "..") if len(name) > 10 else name
                    print(f"{Colors.BRIGHT_YELLOW}{emoji}{short_name:<9}{Colors.RESET}", end=" ")
                else:
                    # Show hidden cards with star wars theming
                    card_symbols = ["⭐", "🌌", "⚔️", "🚀", "👑", "🛸"]
                    symbol = card_symbols[(i + j) % len(card_symbols)]
                    print(f"{Colors.BLUE}{Colors.BG_BLUE} {symbol} ????? {Colors.RESET}", end=" ")
            print()
        
        print("─" * 80)
        
        # Game completion status
        if self.matches_found == self.total_pairs:
            final_time = time.time() - self.start_time
            minutes = int(final_time // 60)
            seconds = int(final_time % 60)
            
            print(f"{Colors.BRIGHT_GREEN}{Colors.BOLD}")
            print("🎉" * 20)
            print("🏆 VICTORY! THE FORCE IS STRONG WITH YOU! 🏆")
            print("🎉" * 20)
            print(f"{Colors.RESET}")
            
            print(f"{Colors.BRIGHT_CYAN}📈 Final Statistics:{Colors.RESET}")
            print(f"   ⏱️  Time: {Colors.BRIGHT_WHITE}{minutes:02d}:{seconds:02d}{Colors.RESET}")
            print(f"   🎯 Moves: {Colors.BRIGHT_WHITE}{self.moves}{Colors.RESET}")
            print(f"   🔥 Best Combo: {Colors.BRIGHT_WHITE}x{max(1, self.combo_count)}{Colors.RESET}")
            print(f"   🏅 Difficulty: {difficulty_color}{self.difficulty.title()}{Colors.RESET}")
            
            # Performance rating
            efficiency = (self.total_pairs * 2) / max(self.moves, 1)
            if efficiency > 0.8:
                rating = f"{Colors.BRIGHT_GREEN}🌟 Jedi Master{Colors.RESET}"
            elif efficiency > 0.6:
                rating = f"{Colors.BRIGHT_BLUE}⚔️  Jedi Knight{Colors.RESET}"
            elif efficiency > 0.4:
                rating = f"{Colors.BRIGHT_YELLOW}🎓 Padawan{Colors.RESET}"
            else:
                rating = f"{Colors.BRIGHT_MAGENTA}👶 Youngling{Colors.RESET}"
            
            print(f"   🎖️  Rating: {rating}")
            
        else:
            print(f"{Colors.BRIGHT_WHITE}💡 Commands: {Colors.RESET}", end="")
            print(f"{Colors.CYAN}[A1-{chr(64+self.grid_size)}{self.grid_size}] {Colors.RESET}to select | ", end="")
            if self.hint_count > 0:
                print(f"{Colors.MAGENTA}[hint] {Colors.RESET}for help | ", end="")
            print(f"{Colors.YELLOW}[undo] {Colors.RESET}last move | ", end="")
            print(f"{Colors.RED}[quit] {Colors.RESET}to exit")
    
    def get_coordinates(self, coord_str):
        """Enhanced coordinate parsing with better error handling"""
        coord_str = coord_str.strip().upper()
        
        # Handle different input formats
        if re.match(r'^[A-Z]\d+$', coord_str):
            try:
                row = ord(coord_str[0]) - ord('A')
                col = int(coord_str[1:]) - 1
                
                if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
                    return row, col
            except (ValueError, IndexError):
                pass
        
        return None, None
    
    def is_valid_move(self, row, col):
        """Check if a move is valid"""
        return (0 <= row < self.grid_size and 
                0 <= col < self.grid_size and 
                not self.matched[row][col] and 
                not self.revealed[row][col])
    
    def give_hint(self):
        """Provide a helpful hint to the player"""
        if self.hint_count <= 0:
            print(f"{Colors.RED}❌ No hints available!{Colors.RESET}")
            return False
        
        # Find a pair that can be hinted
        for character in self.characters:
            positions = []
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    if (self.board[i][j]['id'] == character['id'] and 
                        not self.matched[i][j] and not self.revealed[i][j]):
                        positions.append((i, j))
            
            if len(positions) >= 2:
                pos1, pos2 = positions[:2]
                name = character['name']
                coord1 = f"{chr(65 + pos1[0])}{pos1[1] + 1}"
                coord2 = f"{chr(65 + pos2[0])}{pos2[1] + 1}"
                
                print(f"{Colors.BRIGHT_MAGENTA}💡 HINT: {Colors.BRIGHT_YELLOW}{name}{Colors.RESET} can be found at positions {Colors.BRIGHT_CYAN}{coord1}{Colors.RESET} and {Colors.BRIGHT_CYAN}{coord2}{Colors.RESET}")
                self.hint_count -= 1
                time.sleep(2)
                return True
        
        print(f"{Colors.YELLOW}💡 No obvious pairs to hint at the moment!{Colors.RESET}")
        return False
    
    def undo_last_move(self):
        """Undo the last move"""
        if not self.move_history:
            print(f"{Colors.RED}❌ No moves to undo!{Colors.RESET}")
            return False
        
        # Remove last move from history and revert board state
        last_move = self.move_history.pop()
        for pos in last_move:
            row, col = pos
            self.revealed[row][col] = False
        
        if self.moves > 0:
            self.moves -= 1
        
        print(f"{Colors.BRIGHT_GREEN}↶ Last move undone!{Colors.RESET}")
        time.sleep(1)
        return True
    
    def play_turn(self):
        """Enhanced turn with better feedback"""
        first_card = None
        second_card = None
        
        # Get first card
        while first_card is None:
            self.display_board()
            choice = input(f"\n{Colors.BRIGHT_CYAN}🎯 Select first card: {Colors.RESET}").strip().lower()
            
            if choice == 'quit':
                return False
            elif choice == 'hint':
                self.give_hint()
                continue
            elif choice == 'undo':
                self.undo_last_move()
                continue
            
            row, col = self.get_coordinates(choice)
            if row is not None and self.is_valid_move(row, col):
                first_card = (row, col)
                self.revealed[row][col] = True
                print(f"{Colors.BRIGHT_GREEN}✓ Card selected: {self.board[row][col]['name']}{Colors.RESET}")
                time.sleep(1)
            else:
                print(f"{Colors.RED}❌ Invalid selection! Use format like A1, B3, etc.{Colors.RESET}")
                time.sleep(1)
        
        # Get second card
        while second_card is None:
            self.display_board()
            choice = input(f"\n{Colors.BRIGHT_CYAN}🎯 Select second card: {Colors.RESET}").strip().lower()
            
            if choice == 'quit':
                return False
            elif choice == 'hint':
                self.give_hint()
                continue
            elif choice == 'undo':
                # For second card, just cancel this turn
                r1, c1 = first_card
                self.revealed[r1][c1] = False
                print(f"{Colors.YELLOW}↶ Turn cancelled{Colors.RESET}")
                time.sleep(1)
                return True
            
            row, col = self.get_coordinates(choice)
            if row is not None and self.is_valid_move(row, col):
                second_card = (row, col)
                self.revealed[row][col] = True
                print(f"{Colors.BRIGHT_GREEN}✓ Card selected: {self.board[row][col]['name']}{Colors.RESET}")
                time.sleep(1)
            else:
                print(f"{Colors.RED}❌ Invalid selection! Use format like A1, B3, etc.{Colors.RESET}")
                time.sleep(1)
        
        # Show both cards
        self.display_board()
        self.moves += 1
        current_time = time.time()
        
        # Add to move history
        self.move_history.append([first_card, second_card])
        
        # Check for match
        r1, c1 = first_card
        r2, c2 = second_card
        
        if self.board[r1][c1]['id'] == self.board[r2][c2]['id']:
            print(f"{Colors.BRIGHT_GREEN}{Colors.BOLD}🎉 MATCH! 🎉{Colors.RESET}")
            print(f"{Colors.BRIGHT_CYAN}You found: {Colors.BRIGHT_YELLOW}{self.board[r1][c1]['name']}{Colors.RESET}")
            
            self.matched[r1][c1] = True
            self.matched[r2][c2] = True
            self.matches_found += 1
            
            # Combo system
            if current_time - self.last_match_time < 10.0:  # 10 seconds for combo
                self.combo_count += 1
                if self.combo_count > 1:
                    print(f"{Colors.BRIGHT_YELLOW}🔥 COMBO STREAK: x{self.combo_count}!{Colors.RESET}")
            else:
                self.combo_count = 1
            
            self.last_match_time = current_time
            
            # Bonus for consecutive matches
            if self.combo_count > 3:
                print(f"{Colors.BRIGHT_MAGENTA}⭐ INCREDIBLE! You're on fire! ⭐{Colors.RESET}")
            
        else:
            print(f"{Colors.RED}❌ No match.{Colors.RESET}")
            print(f"{Colors.BRIGHT_WHITE}Cards will be hidden again...{Colors.RESET}")
            time.sleep(2.5)  # Longer time to memorize
            self.revealed[r1][c1] = False
            self.revealed[r2][c2] = False
            self.combo_count = 0  # Reset combo on miss
        
        time.sleep(1.5)
        return True
    
    def play(self):
        """Enhanced main game loop"""
        print(f"\n{Colors.BRIGHT_GREEN}🌟 Welcome to the Enhanced Star Wars Memory Game! 🌟{Colors.RESET}")
        print(f"{Colors.BRIGHT_WHITE}Match pairs of characters by remembering their positions.{Colors.RESET}")
        print(f"{Colors.CYAN}May the Force be with you!{Colors.RESET}")
        print(f"\n{Colors.BRIGHT_YELLOW}Press Enter to begin your journey...{Colors.RESET}")
        input()
        
        self.start_time = time.time()
        
        while self.matches_found < self.total_pairs:
            if not self.play_turn():
                print(f"\n{Colors.BRIGHT_CYAN}Thanks for playing! May the Force be with you! 🌟{Colors.RESET}")
                return
        
        # Final display
        self.display_board()
        
        # Additional celebration
        print(f"\n{Colors.BRIGHT_MAGENTA}✨ The galaxy celebrates your victory! ✨{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}🎊 Thank you for playing the Enhanced Star Wars Memory Game! 🎊{Colors.RESET}")

if __name__ == "__main__":
    try:
        game = EnhancedTextMemoryGame()
        game.play()
    except KeyboardInterrupt:
        print(f"\n{Colors.BRIGHT_YELLOW}Game interrupted. May the Force be with you! 🌟{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}An error occurred: {e}{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}The Force will guide us through this! 🌟{Colors.RESET}")
