import pygame
import requests
import random
import sys
from typing import List, Dict, Tuple, Optional
import io
from urllib.request import urlopen

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 6
CARD_WIDTH = 100
CARD_HEIGHT = 120
CARD_MARGIN = 10
WINDOW_WIDTH = GRID_SIZE * (CARD_WIDTH + CARD_MARGIN) - CARD_MARGIN + 100
WINDOW_HEIGHT = GRID_SIZE * (CARD_HEIGHT + CARD_MARGIN) - CARD_MARGIN + 150

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 200)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

class Card:
    def __init__(self, character_data: Dict, x: int, y: int):
        self.character_data = character_data
        self.x = x
        self.y = y
        self.width = CARD_WIDTH
        self.height = CARD_HEIGHT
        self.is_flipped = False
        self.is_matched = False
        self.image = None
        self.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        
    def load_image(self):
        """Load character image from URL"""
        try:
            if 'image' in self.character_data and self.character_data['image']:
                response = urlopen(self.character_data['image'])
                image_data = response.read()
                image_surface = pygame.image.load(io.BytesIO(image_data))
                self.image = pygame.transform.scale(image_surface, (CARD_WIDTH - 10, CARD_HEIGHT - 30))
        except Exception as e:
            print(f"Error loading image for {self.character_data.get('name', 'Unknown')}: {e}")
            self.image = None
    
    def draw(self, screen, font):
        """Draw the card on screen"""
        if self.is_matched:
            # Draw matched card with green border
            pygame.draw.rect(screen, GREEN, self.rect, 3)
        elif self.is_flipped:
            # Draw flipped card (show character)
            pygame.draw.rect(screen, WHITE, self.rect)
            pygame.draw.rect(screen, BLACK, self.rect, 2)
            
            if self.image:
                # Draw character image
                image_rect = self.image.get_rect()
                image_rect.centerx = self.rect.centerx
                image_rect.y = self.rect.y + 5
                screen.blit(self.image, image_rect)
            
            # Draw character name
            name = self.character_data.get('name', 'Unknown')
            if len(name) > 12:
                name = name[:12] + "..."
            text = font.render(name, True, BLACK)
            text_rect = text.get_rect()
            text_rect.centerx = self.rect.centerx
            text_rect.bottom = self.rect.bottom - 5
            screen.blit(text, text_rect)
        else:
            # Draw card back (not flipped)
            pygame.draw.rect(screen, BLUE, self.rect)
            pygame.draw.rect(screen, BLACK, self.rect, 2)
            
            # Draw Star Wars logo or text
            text = font.render("STAR", True, WHITE)
            text_rect = text.get_rect()
            text_rect.centerx = self.rect.centerx
            text_rect.centery = self.rect.centery - 10
            screen.blit(text, text_rect)
            
            text = font.render("WARS", True, WHITE)
            text_rect = text.get_rect()
            text_rect.centerx = self.rect.centerx
            text_rect.centery = self.rect.centery + 10
            screen.blit(text, text_rect)
    
    def is_clicked(self, pos: Tuple[int, int]) -> bool:
        """Check if the card was clicked"""
        return self.rect.collidepoint(pos)

class MemoryGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Star Wars Memory Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
        
        self.cards: List[Card] = []
        self.flipped_cards: List[Card] = []
        self.matches_found = 0
        self.total_pairs = (GRID_SIZE * GRID_SIZE) // 2
        self.game_won = False
        self.moves = 0
        
        self.load_characters()
        self.create_cards()
        
    def load_characters(self):
        """Load characters from Star Wars API"""
        print("Loading Star Wars characters...")
        try:
            response = requests.get("https://akabab.github.io/starwars-api/api/all.json")
            if response.status_code == 200:
                all_characters = response.json()
                # Filter characters that have images and select random ones
                characters_with_images = [char for char in all_characters if char.get('image')]
                if len(characters_with_images) < self.total_pairs:
                    print(f"Warning: Only {len(characters_with_images)} characters with images available")
                    self.characters = characters_with_images
                else:
                    self.characters = random.sample(characters_with_images, self.total_pairs)
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
        for i in range(self.total_pairs):
            fallback_chars.append({
                'id': i + 1,
                'name': f'Character {i + 1}',
                'image': None
            })
        self.characters = fallback_chars
    
    def create_cards(self):
        """Create and shuffle cards"""
        print("Creating cards...")
        
        # Create pairs of cards
        all_cards_data = []
        for character in self.characters:
            all_cards_data.extend([character, character])  # Create pair
        
        # Shuffle the cards
        random.shuffle(all_cards_data)
        
        # Create card objects and position them in grid
        self.cards = []
        card_index = 0
        start_x = 50
        start_y = 100
        
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if card_index < len(all_cards_data):
                    x = start_x + col * (CARD_WIDTH + CARD_MARGIN)
                    y = start_y + row * (CARD_HEIGHT + CARD_MARGIN)
                    card = Card(all_cards_data[card_index], x, y)
                    self.cards.append(card)
                    card_index += 1
        
        # Load images for all cards (this might take a moment)
        print("Loading character images...")
        for i, card in enumerate(self.cards):
            print(f"Loading image {i + 1}/{len(self.cards)}")
            card.load_image()
        print("All images loaded!")
    
    def handle_card_click(self, pos: Tuple[int, int]):
        """Handle clicking on a card"""
        if self.game_won or len(self.flipped_cards) >= 2:
            return
        
        # Find clicked card
        clicked_card = None
        for card in self.cards:
            if card.is_clicked(pos) and not card.is_flipped and not card.is_matched:
                clicked_card = card
                break
        
        if clicked_card:
            # Flip the card
            clicked_card.is_flipped = True
            self.flipped_cards.append(clicked_card)
            
            # Check if two cards are flipped
            if len(self.flipped_cards) == 2:
                self.moves += 1
                self.check_match()
    
    def check_match(self):
        """Check if two flipped cards match"""
        if len(self.flipped_cards) != 2:
            return
        
        card1, card2 = self.flipped_cards
        
        # Check if cards match (same character ID)
        if card1.character_data['id'] == card2.character_data['id']:
            # Match found!
            card1.is_matched = True
            card2.is_matched = True
            self.matches_found += 1
            self.flipped_cards = []
            
            # Check if game is won
            if self.matches_found == self.total_pairs:
                self.game_won = True
        else:
            # No match - cards will be flipped back after a delay
            pass
    
    def flip_back_cards(self):
        """Flip back non-matching cards"""
        if len(self.flipped_cards) == 2:
            card1, card2 = self.flipped_cards
            if not card1.is_matched and not card2.is_matched:
                card1.is_flipped = False
                card2.is_flipped = False
            self.flipped_cards = []
    
    def draw(self):
        """Draw the game screen"""
        self.screen.fill(LIGHT_GRAY)
        
        # Draw title
        title_text = self.title_font.render("Star Wars Memory Game", True, BLACK)
        title_rect = title_text.get_rect()
        title_rect.centerx = WINDOW_WIDTH // 2
        title_rect.y = 20
        self.screen.blit(title_text, title_rect)
        
        # Draw game stats
        stats_text = f"Moves: {self.moves} | Matches: {self.matches_found}/{self.total_pairs}"
        stats_surface = self.font.render(stats_text, True, BLACK)
        stats_rect = stats_surface.get_rect()
        stats_rect.centerx = WINDOW_WIDTH // 2
        stats_rect.y = 60
        self.screen.blit(stats_surface, stats_rect)
        
        # Draw all cards
        for card in self.cards:
            card.draw(self.screen, self.font)
        
        # Draw win message
        if self.game_won:
            win_text = self.title_font.render("Congratulations! You Won!", True, GREEN)
            win_rect = win_text.get_rect()
            win_rect.centerx = WINDOW_WIDTH // 2
            win_rect.bottom = WINDOW_HEIGHT - 50
            self.screen.blit(win_text, win_rect)
            
            restart_text = self.font.render("Press R to restart or ESC to exit", True, BLACK)
            restart_rect = restart_text.get_rect()
            restart_rect.centerx = WINDOW_WIDTH // 2
            restart_rect.bottom = WINDOW_HEIGHT - 20
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def restart_game(self):
        """Restart the game"""
        self.flipped_cards = []
        self.matches_found = 0
        self.game_won = False
        self.moves = 0
        
        # Reset all cards
        for card in self.cards:
            card.is_flipped = False
            card.is_matched = False
        
        # Shuffle cards again
        random.shuffle(self.cards)
        
        # Reposition cards
        card_index = 0
        start_x = 50
        start_y = 100
        
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if card_index < len(self.cards):
                    x = start_x + col * (CARD_WIDTH + CARD_MARGIN)
                    y = start_y + row * (CARD_HEIGHT + CARD_MARGIN)
                    self.cards[card_index].x = x
                    self.cards[card_index].y = y
                    self.cards[card_index].rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
                    card_index += 1
    
    def run(self):
        """Main game loop"""
        running = True
        flip_back_timer = 0
        flip_back_delay = 60  # 1 second at 60 FPS
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r and self.game_won:
                        self.restart_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_card_click(event.pos)
            
            # Handle flipping back non-matching cards after delay
            if len(self.flipped_cards) == 2:
                card1, card2 = self.flipped_cards
                if not card1.is_matched and not card2.is_matched:
                    flip_back_timer += 1
                    if flip_back_timer >= flip_back_delay:
                        self.flip_back_cards()
                        flip_back_timer = 0
            else:
                flip_back_timer = 0
            
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    print("Starting Star Wars Memory Game...")
    print("This may take a moment to load character images...")
    game = MemoryGame()
    game.run()
