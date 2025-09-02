import requests
import random
import time
import os
import sys
from datetime import datetime
import re

class Colors:
    """WTW Color Palette - ANSI color codes for enhanced terminal output"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

    # WTW Palette converted to ANSI colors
    # Primary Ultraviolet palette
    ULTRAVIOLET_PRIMARY = '\033[38;2;127;53;178m'     # #7f35b2 - Primary brand color
    ULTRAVIOLET_LIGHT = '\033[38;2;193;140;222m'      # #bd8cde - Lighter variant
    ULTRAVIOLET_DARK = '\033[38;2;97;30;144m'         # #611e90 - Darker variant
    ULTRAVIOLET_SUBTLE = '\033[38;2;241;225;253m'     # #f1e1fd - Very light background

    # Grey Matter (Neutral) palette
    GREY_50 = '\033[38;2;242;243;244m'                # #f2f3f4 - Lightest
    GREY_100 = '\033[38;2;231;232;233m'               # #e7e8e9
    GREY_200 = '\033[38;2;202;203;205m'               # #cacbcd
    GREY_400 = '\033[38;2;143;145;148m'               # #8f9194
    GREY_600 = '\033[38;2;92;93;95m'                  # #5c5d5f
    GREY_700 = '\033[38;2;65;66;68m'                  # #414244
    GREY_800 = '\033[38;2;42;42;43m'                  # #2a2a2b
    GREY_900 = '\033[38;2;23;23;24m'                  # #171718

    # Stratosphere (Blue) for information
    STRATOSPHERE_PRIMARY = '\033[38;2;50;127;239m'    # #327fef
    STRATOSPHERE_LIGHT = '\033[38;2;121;177;251m'     # #79b1fb
    STRATOSPHERE_DARK = '\033[38;2;4;62;142m'         # #043e8e

    # Success colors
    SUCCESS_PRIMARY = '\033[38;2;0;123;46m'           # #007b2e
    SUCCESS_LIGHT = '\033[38;2;111;191;138m'          # #6fbf8a

    # Error colors
    ERROR_PRIMARY = '\033[38;2;212;12;12m'            # #d40c0c
    ERROR_LIGHT = '\033[38;2;255;116;108m'            # #ff746c

    # Warning colors
    WARNING_PRIMARY = '\033[38;2;254;121;0m'          # #fe7900
    WARNING_LIGHT = '\033[38;2;255;175;20m'           # #ffaf14

    # Fireworks (Accent pink)
    FIREWORKS_PRIMARY = '\033[38;2;201;0;172m'        # #c900ac
    FIREWORKS_LIGHT = '\033[38;2;244;136;228m'        # #f488e4

    # Coral Reef (Secondary accent)
    CORAL_PRIMARY = '\033[38;2;246;81;127m'           # #f6517f
    CORAL_LIGHT = '\033[38;2;253;139;176m'            # #fd8bb0

    # Background colors using RGB codes
    BG_ULTRAVIOLET = '\033[48;2;127;53;178m'          # Background ultraviolet
    BG_GREY_DARK = '\033[48;2;42;42;43m'              # Dark background
    BG_GREY_LIGHT = '\033[48;2;242;243;244m'          # Light background

    # Text semantic colors based on WTW guidelines
    TEXT_PRIMARY = '\033[38;2;34;34;34m'              # $text-default equivalent
    TEXT_SECONDARY = '\033[38;2;92;93;95m'            # $text-secondary equivalent
    TEXT_CONTRAST = '\033[38;2;255;255;255m'          # White for dark backgrounds
    TEXT_ACCENT = ULTRAVIOLET_PRIMARY                 # Primary brand color
    TEXT_SUCCESS = SUCCESS_PRIMARY
    TEXT_ERROR = ERROR_PRIMARY
    TEXT_WARNING = WARNING_PRIMARY
    TEXT_INFO = STRATOSPHERE_PRIMARY

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

    def show_welcome_screen(self):
        """Enhanced welcome screen with WTW branding and ultraviolet theme"""
        self.clear_screen()
        print(f"{Colors.ULTRAVIOLET_PRIMARY}{Colors.BOLD}")
        print("╔══════════════════════════════════════════════════════════════════╗")
        print("║                                                                  ║")
        print("║        ⭐ STAR WARS ENHANCED MEMORY GAME ⭐                    ║")
        print("║                  Powered by WTW Design System                   ║")
        print("║                                                                  ║")
        print("║    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    ║")
        print("║    ▓    🌌 Journey through the galaxy of memory! 🌌    ▓    ║")
        print("║    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    ║")
        print("║                                                                  ║")
        print("╚══════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.RESET}")

        print(f"\n{Colors.FIREWORKS_PRIMARY}Choose your difficulty:{Colors.RESET}")
        print(f"{Colors.SUCCESS_PRIMARY}1. 🟢 Padawan (Easy)    {Colors.GREY_600}- 4x4 grid, extra hints{Colors.RESET}")
        print(f"{Colors.WARNING_PRIMARY}2. 🟡 Jedi (Normal)     {Colors.GREY_600}- 6x6 grid, some hints{Colors.RESET}")
        print(f"{Colors.ERROR_PRIMARY}3. 🔴 Master (Hard)     {Colors.GREY_600}- 6x6 grid, no hints{Colors.RESET}")

        while True:
            choice = input(f"\n{Colors.ULTRAVIOLET_PRIMARY}Enter your choice (1-3): {Colors.RESET}").strip()
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
                print(f"{Colors.ERROR_PRIMARY}Invalid choice! Please enter 1, 2, or 3.{Colors.RESET}")

        self.total_pairs = (self.grid_size * self.grid_size) // 2
        self.board = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.revealed = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.matched = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        print(f"\n{Colors.SUCCESS_PRIMARY}Great choice! Loading your {self.difficulty} difficulty game...{Colors.RESET}")
        time.sleep(1.5)
    def load_characters(self):
        """Load characters with WTW-themed progress indication"""
        print(f"\n{Colors.STRATOSPHERE_PRIMARY}🚀 Loading Star Wars characters from a galaxy far, far away...{Colors.RESET}")

        # Animated loading with ultraviolet theme
        for i in range(3):
            for char in "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏":
                print(f"\r{Colors.ULTRAVIOLET_PRIMARY}{char} Connecting to the Force...{Colors.RESET}", end="", flush=True)
                time.sleep(0.1)

        try:
            response = requests.get("https://akabab.github.io/starwars-api/api/all.json")
            if response.status_code == 200:
                all_characters = response.json()
                if len(all_characters) >= self.total_pairs:
                    self.characters = random.sample(all_characters, self.total_pairs)
                else:
                    self.characters = all_characters[:self.total_pairs]
                print(f"\r{Colors.SUCCESS_PRIMARY}✅ Successfully loaded {len(self.characters)} characters!{Colors.RESET}")
            else:
                print(f"\r{Colors.WARNING_PRIMARY}⚠️  API connection failed. Using backup characters...{Colors.RESET}")
                self.use_fallback_characters()
        except Exception as e:
            print(f"\r{Colors.WARNING_PRIMARY}⚠️  Connection error. Using backup characters...{Colors.RESET}")
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
        """Set up board with WTW-themed shuffle animation"""
        print(f"\n{Colors.FIREWORKS_PRIMARY}🎲 Shuffling the galaxy...{Colors.RESET}")

        # Create pairs
        all_cards = []
        for character in self.characters:
            all_cards.extend([character, character])

        # Fill remaining slots if needed
        while len(all_cards) < self.grid_size * self.grid_size:
            all_cards.append({'id': 999, 'name': 'Empty'})

        # Animated shuffle with ultraviolet theme
        for i in range(5):
            random.shuffle(all_cards)
            print(f"\r{Colors.ULTRAVIOLET_PRIMARY}🎲 Shuffling{'.' * (i + 1)}{Colors.RESET}", end="", flush=True)
            time.sleep(0.3)

        # Place on board
        index = 0
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.board[i][j] = all_cards[index]
                index += 1

        print(f"\r{Colors.SUCCESS_PRIMARY}✅ Galaxy shuffled and ready!{Colors.RESET}")
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
        """Enhanced board display with WTW colors and ultraviolet theme"""
        self.clear_screen()

        # Header with WTW branding
        print(f"{Colors.ULTRAVIOLET_PRIMARY}{Colors.BOLD}")
        print("╔" + "═" * 78 + "╗")
        print(f"║{' ' * 15}⭐ STAR WARS MEMORY GAME - WTW EDITION ⭐{' ' * 16}║")
        print("╚" + "═" * 78 + "╝")
        print(f"{Colors.RESET}")

        # Game stats with WTW semantic colors
        current_time = time.time() - self.start_time if self.start_time else 0
        minutes = int(current_time // 60)
        seconds = int(current_time % 60)

        difficulty_colors = {
            'easy': Colors.SUCCESS_PRIMARY,
            'normal': Colors.WARNING_PRIMARY,
            'hard': Colors.ERROR_PRIMARY
        }

        difficulty_color = difficulty_colors.get(self.difficulty, Colors.TEXT_PRIMARY)

        print(f"{Colors.TEXT_CONTRAST}📊 Stats: {Colors.RESET}", end="")
        print(f"{Colors.STRATOSPHERE_PRIMARY}Moves: {Colors.TEXT_CONTRAST}{self.moves}{Colors.RESET} | ", end="")
        print(f"{Colors.SUCCESS_PRIMARY}Matches: {Colors.TEXT_CONTRAST}{self.matches_found}/{self.total_pairs}{Colors.RESET} | ", end="")
        print(f"{Colors.FIREWORKS_PRIMARY}Time: {Colors.TEXT_CONTRAST}{minutes:02d}:{seconds:02d}{Colors.RESET} | ", end="")
        print(f"{difficulty_color}Difficulty: {Colors.TEXT_CONTRAST}{self.difficulty.title()}{Colors.RESET}")

        if self.hint_count > 0:
            print(f"{Colors.CORAL_PRIMARY}💡 Hints available: {Colors.TEXT_CONTRAST}{self.hint_count}{Colors.RESET}")

        if self.combo_count > 1:
            print(f"{Colors.FIREWORKS_PRIMARY}🔥 COMBO STREAK: x{self.combo_count}! {Colors.RESET}")

        print("─" * 80)

        # Column headers with ultraviolet theme
        print(f"{Colors.ULTRAVIOLET_PRIMARY}    ", end="")
        for j in range(self.grid_size):
            print(f"{j+1:^12}", end="")
        print(f"{Colors.RESET}")

        # Board with WTW color scheme
        for i in range(self.grid_size):
            print(f"{Colors.ULTRAVIOLET_PRIMARY}{chr(65+i):>2}: {Colors.RESET}", end="")
            for j in range(self.grid_size):
                if self.matched[i][j]:
                    # Show matched cards with success color and character info
                    name = self.board[i][j]['name']
                    emoji = self.get_character_emoji(name)
                    short_name = (name[:8] + "..") if len(name) > 10 else name
                    print(f"{Colors.SUCCESS_PRIMARY}✓{emoji}{short_name:<8}{Colors.RESET}", end=" ")
                elif self.revealed[i][j]:
                    # Show temporarily revealed cards with accent color
                    name = self.board[i][j]['name']
                    emoji = self.get_character_emoji(name)
                    short_name = (name[:8] + "..") if len(name) > 10 else name
                    print(f"{Colors.CORAL_PRIMARY}{emoji}{short_name:<9}{Colors.RESET}", end=" ")
                else:
                    # Show hidden cards with ultraviolet theme
                    card_symbols = ["⭐", "🌌", "⚔️", "🚀", "👑", "🛸"]
                    symbol = card_symbols[(i + j) % len(card_symbols)]
                    print(f"{Colors.BG_ULTRAVIOLET}{Colors.TEXT_CONTRAST} {symbol} ????? {Colors.RESET}", end=" ")
            print()

        print("─" * 80)

        # Game completion status with WTW victory theme
        if self.matches_found == self.total_pairs:
            final_time = time.time() - self.start_time
            minutes = int(final_time // 60)
            seconds = int(final_time % 60)

            print(f"{Colors.SUCCESS_PRIMARY}{Colors.BOLD}")
            print("🎉" * 20)
            print("🏆 VICTORY! THE FORCE IS STRONG WITH YOU! 🏆")
            print("🎉" * 20)
            print(f"{Colors.RESET}")

            print(f"{Colors.ULTRAVIOLET_PRIMARY}📈 Final Statistics:{Colors.RESET}")
            print(f"   ⏱️  Time: {Colors.TEXT_CONTRAST}{minutes:02d}:{seconds:02d}{Colors.RESET}")
            print(f"   🎯 Moves: {Colors.TEXT_CONTRAST}{self.moves}{Colors.RESET}")
            print(f"   🔥 Best Combo: {Colors.TEXT_CONTRAST}x{max(1, self.combo_count)}{Colors.RESET}")
            print(f"   🏅 Difficulty: {difficulty_color}{self.difficulty.title()}{Colors.RESET}")

            # Performance rating with WTW color scheme
            efficiency = (self.total_pairs * 2) / max(self.moves, 1)
            if efficiency > 0.8:
                rating = f"{Colors.SUCCESS_PRIMARY}🌟 Jedi Master{Colors.RESET}"
            elif efficiency > 0.6:
                rating = f"{Colors.STRATOSPHERE_PRIMARY}⚔️  Jedi Knight{Colors.RESET}"
            elif efficiency > 0.4:
                rating = f"{Colors.WARNING_PRIMARY}🎓 Padawan{Colors.RESET}"
            else:
                rating = f"{Colors.FIREWORKS_PRIMARY}👶 Youngling{Colors.RESET}"

            print(f"   🎖️  Rating: {rating}")

        else:
            print(f"{Colors.TEXT_CONTRAST}💡 Commands: {Colors.RESET}", end="")
            print(f"{Colors.ULTRAVIOLET_PRIMARY}[A1-{chr(64+self.grid_size)}{self.grid_size}] {Colors.RESET}to select | ", end="")
            if self.hint_count > 0:
                print(f"{Colors.CORAL_PRIMARY}[hint] {Colors.RESET}for help | ", end="")
            print(f"{Colors.WARNING_PRIMARY}[undo] {Colors.RESET}last move | ", end="")
            print(f"{Colors.ERROR_PRIMARY}[quit] {Colors.RESET}to exit")

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
        """Provide a helpful hint with WTW styling"""
        if self.hint_count <= 0:
            print(f"{Colors.ERROR_PRIMARY}❌ No hints available!{Colors.RESET}")
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

                print(f"{Colors.CORAL_PRIMARY}💡 HINT: {Colors.FIREWORKS_PRIMARY}{name}{Colors.RESET} can be found at positions {Colors.ULTRAVIOLET_PRIMARY}{coord1}{Colors.RESET} and {Colors.ULTRAVIOLET_PRIMARY}{coord2}{Colors.RESET}")
                self.hint_count -= 1
                time.sleep(2)
                return True

        print(f"{Colors.WARNING_PRIMARY}💡 No obvious pairs to hint at the moment!{Colors.RESET}")
        return False

    def undo_last_move(self):
        """Undo the last move with WTW feedback"""
        if not self.move_history:
            print(f"{Colors.ERROR_PRIMARY}❌ No moves to undo!{Colors.RESET}")
            return False

        # Remove last move from history and revert board state
        last_move = self.move_history.pop()
        for pos in last_move:
            row, col = pos
            self.revealed[row][col] = False

        if self.moves > 0:
            self.moves -= 1

        print(f"{Colors.SUCCESS_PRIMARY}↶ Last move undone!{Colors.RESET}")
        time.sleep(1)
        return True

    def play_turn(self):
        """Enhanced turn with better feedback"""
        first_card = None
        second_card = None

        # Get first card with WTW styling
        while first_card is None:
            self.display_board()
            choice = input(f"\n{Colors.ULTRAVIOLET_PRIMARY}🎯 Select first card: {Colors.RESET}").strip().lower()

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
                print(f"{Colors.SUCCESS_PRIMARY}✓ Card selected: {self.board[row][col]['name']}{Colors.RESET}")
                time.sleep(1)
            else:
                print(f"{Colors.ERROR_PRIMARY}❌ Invalid selection! Use format like A1, B3, etc.{Colors.RESET}")
                time.sleep(1)

        # Get second card
        while second_card is None:
            self.display_board()
            choice = input(f"\n{Colors.ULTRAVIOLET_PRIMARY}🎯 Select second card: {Colors.RESET}").strip().lower()

            if choice == 'quit':
                return False
            elif choice == 'hint':
                self.give_hint()
                continue
            elif choice == 'undo':
                # For second card, just cancel this turn
                r1, c1 = first_card
                self.revealed[r1][c1] = False
                print(f"{Colors.WARNING_PRIMARY}↶ Turn cancelled{Colors.RESET}")
                time.sleep(1)
                return True

            row, col = self.get_coordinates(choice)
            if row is not None and self.is_valid_move(row, col):
                second_card = (row, col)
                self.revealed[row][col] = True
                print(f"{Colors.SUCCESS_PRIMARY}✓ Card selected: {self.board[row][col]['name']}{Colors.RESET}")
                time.sleep(1)
            else:
                print(f"{Colors.ERROR_PRIMARY}❌ Invalid selection! Use format like A1, B3, etc.{Colors.RESET}")
                time.sleep(1)

        # Show both cards
        self.display_board()
        self.moves += 1
        current_time = time.time()

        # Add to move history
        self.move_history.append([first_card, second_card])

        # Check for match with WTW celebration
        r1, c1 = first_card
        r2, c2 = second_card

        if self.board[r1][c1]['id'] == self.board[r2][c2]['id']:
            print(f"{Colors.SUCCESS_PRIMARY}{Colors.BOLD}🎉 MATCH! 🎉{Colors.RESET}")
            print(f"{Colors.ULTRAVIOLET_PRIMARY}You found: {Colors.FIREWORKS_PRIMARY}{self.board[r1][c1]['name']}{Colors.RESET}")

            self.matched[r1][c1] = True
            self.matched[r2][c2] = True
            self.matches_found += 1

            # Combo system with WTW colors
            if current_time - self.last_match_time < 10.0:  # 10 seconds for combo
                self.combo_count += 1
                if self.combo_count > 1:
                    print(f"{Colors.FIREWORKS_PRIMARY}🔥 COMBO STREAK: x{self.combo_count}!{Colors.RESET}")
            else:
                self.combo_count = 1

            self.last_match_time = current_time

            # Bonus for consecutive matches with ultraviolet theme
            if self.combo_count > 3:
                print(f"{Colors.ULTRAVIOLET_PRIMARY}⭐ INCREDIBLE! You're on fire! ⭐{Colors.RESET}")

        else:
            print(f"{Colors.ERROR_PRIMARY}❌ No match.{Colors.RESET}")
            print(f"{Colors.TEXT_CONTRAST}Cards will be hidden again...{Colors.RESET}")
            time.sleep(2.5)  # Longer time to memorize
            self.revealed[r1][c1] = False
            self.revealed[r2][c2] = False
            self.combo_count = 0  # Reset combo on miss

        time.sleep(1.5)
        return True

    def play(self):
        """Enhanced main game loop with WTW branding"""
        print(f"\n{Colors.SUCCESS_PRIMARY}🌟 Welcome to the Enhanced Star Wars Memory Game! 🌟{Colors.RESET}")
        print(f"{Colors.TEXT_CONTRAST}Match pairs of characters by remembering their positions.{Colors.RESET}")
        print(f"{Colors.ULTRAVIOLET_PRIMARY}May the Force be with you!{Colors.RESET}")
        print(f"\n{Colors.FIREWORKS_PRIMARY}Press Enter to begin your journey...{Colors.RESET}")
        input()

        self.start_time = time.time()

        while self.matches_found < self.total_pairs:
            if not self.play_turn():
                print(f"\n{Colors.ULTRAVIOLET_PRIMARY}Thanks for playing! May the Force be with you! 🌟{Colors.RESET}")
                return

        # Final display
        self.display_board()

        # Additional celebration with WTW theme
        print(f"\n{Colors.FIREWORKS_PRIMARY}✨ The galaxy celebrates your victory! ✨{Colors.RESET}")
        print(f"{Colors.ULTRAVIOLET_PRIMARY}🎊 Thank you for playing the WTW Enhanced Star Wars Memory Game! 🎊{Colors.RESET}")

if __name__ == "__main__":
    try:
        game = EnhancedTextMemoryGame()
        game.play()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING_PRIMARY}Game interrupted. May the Force be with you! 🌟{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.ERROR_PRIMARY}An error occurred: {e}{Colors.RESET}")
        print(f"{Colors.ULTRAVIOLET_PRIMARY}The Force will guide us through this! 🌟{Colors.RESET}")
