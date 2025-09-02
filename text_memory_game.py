import requests
import random
import time
import os

class TextMemoryGame:
    def __init__(self):
        self.grid_size = 6
        self.total_pairs = (self.grid_size * self.grid_size) // 2
        self.board = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.revealed = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.matched = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.characters = []
        self.moves = 0
        self.matches_found = 0

        self.load_characters()
        self.setup_board()

    def load_characters(self):
        """Load characters from Star Wars API"""
        print("Loading Star Wars characters...")
        try:
            response = requests.get("https://akabab.github.io/starwars-api/api/all.json")
            if response.status_code == 200:
                all_characters = response.json()
                # Select random characters for the game
                if len(all_characters) >= self.total_pairs:
                    self.characters = random.sample(all_characters, self.total_pairs)
                else:
                    self.characters = all_characters[:self.total_pairs]
                print(f"Loaded {len(self.characters)} characters")
            else:
                print(f"Error loading characters: HTTP {response.status_code}")
                self.use_fallback_characters()
        except Exception as e:
            print(f"Error loading characters: {e}")
            self.use_fallback_characters()

    def use_fallback_characters(self):
        """Use fallback character data if API fails"""
        print("Using fallback characters...")
        fallback_chars = []
        names = ["Luke", "Leia", "Han", "Chewbacca", "Obi-Wan", "Vader", "Yoda", "R2-D2", "C-3PO",
                "Palpatine", "Anakin", "Padme", "Mace", "Qui-Gon", "Jar Jar", "Boba", "Jango", "Rey"]
        for i in range(min(self.total_pairs, len(names))):
            fallback_chars.append({
                'id': i + 1,
                'name': names[i],
            })
        self.characters = fallback_chars

    def setup_board(self):
        """Set up the game board with character pairs"""
        # Create pairs
        all_cards = []
        for character in self.characters:
            all_cards.extend([character, character])

        # Fill remaining slots if needed
        while len(all_cards) < self.grid_size * self.grid_size:
            all_cards.append({'id': 999, 'name': 'Empty'})

        # Shuffle cards
        random.shuffle(all_cards)

        # Place on board
        index = 0
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.board[i][j] = all_cards[index]
                index += 1

    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_board(self):
        """Display the current state of the board"""
        self.clear_screen()
        print("=" * 60)
        print("STAR WARS MEMORY GAME")
        print("=" * 60)
        print(f"Moves: {self.moves} | Matches: {self.matches_found}/{self.total_pairs}")
        print("-" * 60)

        # Column headers
        print("    ", end="")
        for j in range(self.grid_size):
            print(f"{j+1:^8}", end=" ")
        print()

        # Board rows
        for i in range(self.grid_size):
            print(f"{chr(65+i):>2}: ", end="")
            for j in range(self.grid_size):
                if self.matched[i][j]:
                    # Show matched cards
                    name = self.board[i][j]['name'][:7]
                    print(f"{name:^8}", end=" ")
                elif self.revealed[i][j]:
                    # Show temporarily revealed cards
                    name = self.board[i][j]['name'][:7]
                    print(f"{name:^8}", end=" ")
                else:
                    # Show hidden cards
                    print("   ??   ", end=" ")
            print()

        print("-" * 60)
        if self.matches_found == self.total_pairs:
            print("🎉 CONGRATULATIONS! YOU WON! 🎉")
            print(f"You completed the game in {self.moves} moves!")
        else:
            print("Enter coordinates (e.g., A1, B3) or 'quit' to exit")

    def get_coordinates(self, coord_str):
        """Convert coordinate string (like A1) to row, col indices"""
        if len(coord_str) < 2:
            return None, None

        try:
            row = ord(coord_str[0].upper()) - ord('A')
            col = int(coord_str[1:]) - 1

            if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
                return row, col
            else:
                return None, None
        except (ValueError, IndexError):
            return None, None

    def is_valid_move(self, row, col):
        """Check if a move is valid"""
        return (0 <= row < self.grid_size and
                0 <= col < self.grid_size and
                not self.matched[row][col] and
                not self.revealed[row][col])

    def play_turn(self):
        """Handle one turn of the game"""
        first_card = None
        second_card = None

        # Get first card
        while first_card is None:
            self.display_board()
            choice = input("Select first card: ").strip()
            if choice.lower() == 'quit':
                return False

            row, col = self.get_coordinates(choice)
            if row is not None and self.is_valid_move(row, col):
                first_card = (row, col)
                self.revealed[row][col] = True
            else:
                print("Invalid selection! Try again.")
                time.sleep(1)

        # Get second card
        while second_card is None:
            self.display_board()
            choice = input("Select second card: ").strip()
            if choice.lower() == 'quit':
                return False

            row, col = self.get_coordinates(choice)
            if row is not None and self.is_valid_move(row, col):
                second_card = (row, col)
                self.revealed[row][col] = True
            else:
                print("Invalid selection! Try again.")
                time.sleep(1)

        # Show both cards
        self.display_board()
        self.moves += 1

        # Check for match
        r1, c1 = first_card
        r2, c2 = second_card

        if self.board[r1][c1]['id'] == self.board[r2][c2]['id']:
            print("🎉 MATCH! 🎉")
            self.matched[r1][c1] = True
            self.matched[r2][c2] = True
            self.matches_found += 1
        else:
            print("No match. Cards will be hidden again.")
            time.sleep(2)
            self.revealed[r1][c1] = False
            self.revealed[r2][c2] = False

        time.sleep(2)
        return True

    def play(self):
        """Main game loop"""
        print("Welcome to the Star Wars Memory Game!")
        print("Match pairs of characters by remembering their positions.")
        print("Use coordinates like A1, B3, etc. to select cards.")
        print("\nPress Enter to start...")
        input()

        while self.matches_found < self.total_pairs:
            if not self.play_turn():
                print("Thanks for playing!")
                return

        self.display_board()
        print(f"\n🏆 Game completed in {self.moves} moves! 🏆")
        print("Thanks for playing the Star Wars Memory Game!")

if __name__ == "__main__":
    game = TextMemoryGame()
    game.play()
