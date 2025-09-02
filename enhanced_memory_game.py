import pygame
import requests
import random
import sys
import math
import time
from typing import List, Dict, Tuple, Optional
import io
from urllib.request import urlopen

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants - will be dynamically set based on difficulty
CARD_WIDTH = 100
CARD_HEIGHT = 120
CARD_MARGIN = 12

# Difficulty configurations
DIFFICULTY_CONFIGS = {
    'Easy': {'grid_size': 4, 'pairs': 8, 'time_bonus': 1.5},
    'Medium': {'grid_size': 6, 'pairs': 18, 'time_bonus': 1.0},
    'Hard': {'grid_size': 8, 'pairs': 32, 'time_bonus': 0.7}
}

def calculate_window_size(grid_size):
    """Calculate window dimensions based on grid size"""
    width = grid_size * (CARD_WIDTH + CARD_MARGIN) - CARD_MARGIN + 200
    height = grid_size * (CARD_HEIGHT + CARD_MARGIN) - CARD_MARGIN + 200
    return width, height

# WTW Color Palette for GUI
COLORS = {
    # Primary Ultraviolet as the main brand color
    'primary': (127, 53, 178),            # #7f35b2 - ultraviolet-key
    'primary_light': (193, 140, 222),     # #bd8cde - ultraviolet-350
    'primary_dark': (97, 30, 144),        # #611e90 - ultraviolet-700
    'primary_subtle': (241, 225, 253),    # #f1e1fd - ultraviolet-100

    # Background and surfaces
    'background': (42, 42, 43),           # #2a2a2b - grey-matter-800
    'surface_light': (242, 243, 244),     # #f2f3f4 - grey-matter-50
    'surface_moderate': (231, 232, 233),  # #e7e8e9 - grey-matter-100
    'surface_dark': (92, 93, 95),         # #5c5d5f - grey-matter-600

    # Card states
    'card_back': (127, 53, 178),          # Primary ultraviolet
    'card_front': (255, 255, 255),        # White
    'card_hover': (193, 140, 222),        # Lighter ultraviolet
    'card_matched': (0, 123, 46),         # #007b2e - success-key
    'card_border': (65, 66, 68),          # #414244 - grey-matter-700

    # Interactive elements
    'stratosphere': (50, 127, 239),       # #327fef - stratosphere-key
    'stratosphere_light': (121, 177, 251), # #79b1fb - stratosphere-300

    # Status colors
    'success': (0, 123, 46),              # #007b2e - success-key
    'success_light': (111, 191, 138),     # #6fbf8a - success-300
    'error': (212, 12, 12),               # #d40c0c - error-key
    'warning': (254, 121, 0),             # #fe7900 - warning-key
    'info': (7, 124, 192),                # #077cc0 - information-key

    # Accent colors
    'fireworks': (201, 0, 172),           # #c900ac - fireworks-key
    'coral': (246, 81, 127),              # #f6517f - coral-reef-key
    'infinity': (58, 220, 201),           # #3adcc9 - infinity-key

    # Text colors
    'text_primary': (255, 255, 255),      # White for dark backgrounds
    'text_secondary': (202, 203, 205),    # #cacbcd - grey-matter-200
    'text_accent': (127, 53, 178),        # Primary ultraviolet
    'text_contrast': (23, 23, 24),        # #171718 - grey-matter-900

    # Particles and effects
    'particle': (246, 81, 127),           # Coral reef for particles
    'particle_alt': (201, 0, 172),        # Fireworks for variety
}

# Animation constants
FLIP_DURATION = 300  # milliseconds
MATCH_HIGHLIGHT_DURATION = 800
PARTICLE_LIFETIME = 1000

class Particle:
    """Particle effect for celebrations"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, -1)
        self.lifetime = PARTICLE_LIFETIME
        self.age = 0
        self.size = random.randint(3, 8)
        # Use WTW accent colors for particles
        self.color = random.choice([COLORS['particle'], COLORS['particle_alt'], COLORS['fireworks']])

    def update(self, dt):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # gravity
        self.age += dt

    def draw(self, screen):
        alpha = max(0, 1 - self.age / self.lifetime)
        if alpha > 0:
            size = max(1, int(self.size * alpha))
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)

    def is_alive(self):
        return self.age < self.lifetime

class Card:
    def __init__(self, character_data: Dict, x: int, y: int):
        self.character_data = character_data
        self.target_x = x
        self.target_y = y
        self.x = x
        self.y = y
        self.width = CARD_WIDTH
        self.height = CARD_HEIGHT
        self.is_flipped = False
        self.is_matched = False
        self.is_hovered = False
        self.image = None
        self.has_image = False  # Track whether we have a real image or text fallback
        self.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)

        # Animation properties
        self.flip_progress = 0.0
        self.flip_target = 0.0
        self.scale = 1.0
        self.target_scale = 1.0
        self.match_highlight_timer = 0
        self.bounce_offset = 0

    def load_image(self):
        """Load character image from URL with caching, create text fallback if image fails"""
        try:
            if 'image' in self.character_data and self.character_data['image']:
                response = urlopen(self.character_data['image'])
                image_data = response.read()
                
                # Check if we actually got image data
                if len(image_data) < 100:  # Very small file, likely not a real image
                    raise Exception(f"Image file too small ({len(image_data)} bytes)")
                
                image_surface = pygame.image.load(io.BytesIO(image_data))
                
                # Check if image is too small (likely a placeholder or broken)
                if image_surface.get_width() < 50 or image_surface.get_height() < 50:
                    raise Exception(f"Image dimensions too small ({image_surface.get_width()}x{image_surface.get_height()})")
                
                # Better scaling with anti-aliasing
                self.image = pygame.transform.smoothscale(image_surface, (CARD_WIDTH - 20, CARD_HEIGHT - 40))
                self.has_image = True
            else:
                self.create_text_image()
        except Exception as e:
            print(f"Creating text fallback for {self.character_data.get('name', 'Unknown')}: {e}")
            self.create_text_image()
    
    def create_text_image(self):
        """Create a text-based image for characters without valid images"""
        self.has_image = False
        # Create a surface for the text-based character card
        text_surface = pygame.Surface((CARD_WIDTH - 20, CARD_HEIGHT - 40), pygame.SRCALPHA)
        
        # Use character name
        name = self.character_data.get('name', 'Unknown')
        
        # Create font for Star Wars style text (bold and larger)
        try:
            # Try to use a bold system font that looks more like Star Wars
            font_large = pygame.font.Font(None, 24)
            font_large.set_bold(True)
            font_medium = pygame.font.Font(None, 18)
            font_medium.set_bold(True)
        except:
            font_large = pygame.font.Font(None, 24)
            font_medium = pygame.font.Font(None, 18)
        
        # Split name into lines if too long
        words = name.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if font_medium.size(test_line)[0] < (CARD_WIDTH - 30):
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        
        # Limit to 3 lines maximum
        if len(lines) > 3:
            lines = lines[:2]
            lines.append("...")
        
        # Calculate total text height
        line_height = font_medium.get_height()
        total_height = len(lines) * line_height
        start_y = (CARD_HEIGHT - 60 - total_height) // 2
        
        # Draw background with gradient effect
        gradient_color = COLORS['primary_light']
        pygame.draw.rect(text_surface, gradient_color, text_surface.get_rect(), border_radius=8)
        
        # Draw border
        pygame.draw.rect(text_surface, COLORS['primary'], text_surface.get_rect(), width=2, border_radius=8)
        
        # Draw text lines
        for i, line in enumerate(lines):
            # Use different colors for Star Wars feel
            text_color = COLORS['text_contrast']
            if i == 0:  # First line in primary color
                text_color = COLORS['primary_dark']
            
            text_render = font_medium.render(line, True, text_color)
            text_rect = text_render.get_rect()
            text_rect.centerx = text_surface.get_width() // 2
            text_rect.y = start_y + i * line_height
            text_surface.blit(text_render, text_rect)
        
        # Add decorative elements for Star Wars theme
        star_color = COLORS['fireworks']
        star_size = 8
        
        # Draw small stars in corners
        pygame.draw.circle(text_surface, star_color, (star_size, star_size), 3)
        pygame.draw.circle(text_surface, star_color, (text_surface.get_width() - star_size, star_size), 3)
        pygame.draw.circle(text_surface, star_color, (star_size, text_surface.get_height() - star_size), 3)
        pygame.draw.circle(text_surface, star_color, (text_surface.get_width() - star_size, text_surface.get_height() - star_size), 3)
        
        self.image = text_surface

    def update(self, dt, mouse_pos=None):
        """Update card animations"""
        # Smooth flip animation
        if self.flip_progress != self.flip_target:
            flip_speed = 0.01 * dt
            if abs(self.flip_target - self.flip_progress) < flip_speed:
                self.flip_progress = self.flip_target
            else:
                self.flip_progress += flip_speed if self.flip_target > self.flip_progress else -flip_speed

        # Scale animation for hover effect
        if self.scale != self.target_scale:
            scale_speed = 0.008 * dt
            if abs(self.target_scale - self.scale) < scale_speed:
                self.scale = self.target_scale
            else:
                self.scale += scale_speed if self.target_scale > self.scale else -scale_speed

        # Hover detection
        if mouse_pos and not self.is_matched and not self.is_flipped:
            self.is_hovered = self.rect.collidepoint(mouse_pos)
            self.target_scale = 1.05 if self.is_hovered else 1.0
        else:
            self.is_hovered = False
            self.target_scale = 1.0

        # Match highlight timer
        if self.match_highlight_timer > 0:
            self.match_highlight_timer -= dt
            self.bounce_offset = math.sin(self.match_highlight_timer * 0.02) * 5
        else:
            self.bounce_offset = 0

        # Update rect for collision detection
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        scaled_width = int(self.width * self.scale)
        scaled_height = int(self.height * self.scale)
        self.rect = pygame.Rect(
            center_x - scaled_width // 2,
            center_y - scaled_height // 2 + self.bounce_offset,
            scaled_width,
            scaled_height
        )

    def flip(self):
        """Trigger flip animation"""
        self.flip_target = 1.0 if not self.is_flipped else 0.0
        self.is_flipped = not self.is_flipped

    def set_matched(self):
        """Mark card as matched with celebration effect"""
        self.is_matched = True
        self.match_highlight_timer = MATCH_HIGHLIGHT_DURATION

    def draw(self, screen, font, small_font):
        """Draw the card with smooth animations"""
        # Calculate scaled dimensions
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2 + self.bounce_offset

        # Flip effect: scale width based on flip progress
        flip_scale = abs(math.cos(self.flip_progress * math.pi))
        scaled_width = max(5, int(self.width * self.scale * flip_scale))
        scaled_height = int(self.height * self.scale)

        card_rect = pygame.Rect(
            center_x - scaled_width // 2,
            center_y - scaled_height // 2,
            scaled_width,
            scaled_height
        )

        # Determine which side to show
        show_front = self.flip_progress > 0.5

        # Choose colors based on state
        if self.is_matched:
            border_color = COLORS['card_matched']
            card_color = COLORS['card_front']
        elif show_front:
            border_color = COLORS['card_border']
            card_color = COLORS['card_front']
        else:
            border_color = COLORS['card_hover'] if self.is_hovered else COLORS['card_border']
            card_color = COLORS['card_hover'] if self.is_hovered else COLORS['card_back']

        # Add glow effect for matched cards
        if self.is_matched and self.match_highlight_timer > 0:
            glow_radius = int(10 + math.sin(self.match_highlight_timer * 0.02) * 5)
            glow_rect = card_rect.inflate(glow_radius * 2, glow_radius * 2)
            pygame.draw.rect(screen, COLORS['success'], glow_rect, border_radius=12)

        # Draw card with rounded corners effect
        pygame.draw.rect(screen, card_color, card_rect, border_radius=8)
        pygame.draw.rect(screen, border_color, card_rect, width=3, border_radius=8)

        if show_front and scaled_width > 20:
            # Draw character image (either real image or text-based fallback)
            if self.image:
                image_width = max(10, int((CARD_WIDTH - 20) * self.scale * flip_scale))
                image_height = max(10, int((CARD_HEIGHT - 40) * self.scale))

                if image_width > 5 and image_height > 5:
                    scaled_image = pygame.transform.smoothscale(self.image, (image_width, image_height))
                    image_rect = scaled_image.get_rect()
                    image_rect.centerx = center_x
                    image_rect.y = center_y - scaled_height // 2 + 8
                    screen.blit(scaled_image, image_rect)

            # Only draw character name text if we have a real image (not text-based fallback)
            if self.has_image and self.image:
                name = self.character_data.get('name', 'Unknown')
                if len(name) > 10:
                    name = name[:10] + "..."

                text_color = COLORS['text_primary'] if not self.is_matched else COLORS['success']
                text = small_font.render(name, True, text_color)
                text_rect = text.get_rect()
                text_rect.centerx = center_x
                text_rect.bottom = center_y + scaled_height // 2 - 5

                if scaled_width > text_rect.width:
                    screen.blit(text, text_rect)

        elif not show_front and scaled_width > 20:
            # Draw card back with Star Wars branding
            star_color = COLORS['fireworks'] if self.is_hovered else COLORS['text_primary']

            # Draw "STAR" text
            star_text = font.render("STAR", True, star_color)
            star_rect = star_text.get_rect()
            star_rect.centerx = center_x
            star_rect.centery = center_y - 8
            if scaled_width > star_rect.width:
                screen.blit(star_text, star_rect)

            # Draw "WARS" text
            wars_text = font.render("WARS", True, star_color)
            wars_rect = wars_text.get_rect()
            wars_rect.centerx = center_x
            wars_rect.centery = center_y + 8
            if scaled_width > wars_rect.width:
                screen.blit(wars_text, wars_rect)

    def is_clicked(self, pos: Tuple[int, int]) -> bool:
        """Check if the card was clicked"""
        return self.rect.collidepoint(pos)

class LoadingScreen:
    """Smooth loading screen with progress indication"""
    def __init__(self, screen, font, title_font):
        self.screen = screen
        self.font = font
        self.title_font = title_font
        self.progress = 0
        self.max_progress = 100
        self.dots = 0
        self.dot_timer = 0

    def update(self, dt):
        self.dot_timer += dt
        if self.dot_timer > 500:  # Change dots every 500ms
            self.dots = (self.dots + 1) % 4
            self.dot_timer = 0

    def set_progress(self, current, total, message="Loading"):
        self.progress = int((current / total) * 100)
        self.current_message = message

    def draw(self, message="Loading Star Wars characters"):
        self.screen.fill(COLORS['background'])

        # Title
        title = self.title_font.render("Star Wars Memory Game", True, COLORS['fireworks'])
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
        self.screen.blit(title, title_rect)

        # Loading message with animated dots
        dots = "." * self.dots
        loading_text = f"{message}{dots}"
        text = self.font.render(loading_text, True, COLORS['text_primary'])
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
        self.screen.blit(text, text_rect)

        # Progress bar
        bar_width = 300
        bar_height = 20
        bar_x = (WINDOW_WIDTH - bar_width) // 2
        bar_y = WINDOW_HEIGHT // 2 + 20

        # Background bar
        pygame.draw.rect(self.screen, COLORS['card_border'],
                        (bar_x, bar_y, bar_width, bar_height), border_radius=10)

        # Progress fill
        fill_width = int((self.progress / 100) * bar_width)
        if fill_width > 0:
            pygame.draw.rect(self.screen, COLORS['fireworks'],
                            (bar_x, bar_y, fill_width, bar_height), border_radius=10)

        # Progress text
        progress_text = f"{self.progress}%"
        progress_surface = self.font.render(progress_text, True, COLORS['text_secondary'])
        progress_rect = progress_surface.get_rect(center=(WINDOW_WIDTH // 2, bar_y + bar_height + 30))
        self.screen.blit(progress_surface, progress_rect)

        pygame.display.flip()

class MemoryGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Star Wars Memory Game - Enhanced Edition")
        self.clock = pygame.time.Clock()

        # Enhanced fonts
        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 20)
        self.title_font = pygame.font.Font(None, 42)
        self.large_font = pygame.font.Font(None, 64)

        # Game state
        self.cards: List[Card] = []
        self.flipped_cards: List[Card] = []
        self.matches_found = 0
        self.total_pairs = (GRID_SIZE * GRID_SIZE) // 2
        self.game_won = False
        self.moves = 0
        self.start_time = time.time()
        self.game_time = 0

        # Effects
        self.particles: List[Particle] = []
        self.screen_shake = 0
        self.combo_count = 0
        self.last_match_time = 0

        # UI state
        self.mouse_pos = (0, 0)
        self.loading_screen = LoadingScreen(self.screen, self.font, self.title_font)

        # Load game data
        self.load_characters()
        self.create_cards()

    def load_characters(self):
        """Load characters with enhanced loading screen"""
        self.loading_screen.draw("Loading Star Wars characters")
        pygame.display.flip()

        try:
            response = requests.get("https://akabab.github.io/starwars-api/api/all.json")
            if response.status_code == 200:
                all_characters = response.json()
                characters_with_images = [char for char in all_characters if char.get('image')]

                if len(characters_with_images) >= self.total_pairs:
                    self.characters = random.sample(characters_with_images, self.total_pairs)
                else:
                    self.characters = characters_with_images

                print(f"Loaded {len(self.characters)} characters")
            else:
                self.use_fallback_characters()
        except Exception as e:
            print(f"Error loading characters: {e}")
            self.use_fallback_characters()

    def use_fallback_characters(self):
        """Use fallback character data"""
        fallback_names = [
            "Luke Skywalker", "Princess Leia", "Han Solo", "Chewbacca", "Obi-Wan Kenobi",
            "Darth Vader", "Yoda", "R2-D2", "C-3PO", "Emperor Palpatine",
            "Anakin Skywalker", "Padmé Amidala", "Mace Windu", "Qui-Gon Jinn",
            "Jar Jar Binks", "Boba Fett", "Jango Fett", "Rey"
        ]

        self.characters = []
        for i in range(min(self.total_pairs, len(fallback_names))):
            self.characters.append({
                'id': i + 1,
                'name': fallback_names[i],
                'image': None
            })

    def create_cards(self):
        """Create cards with loading progress"""
        # Create pairs
        all_cards_data = []
        for character in self.characters:
            all_cards_data.extend([character, character])

        random.shuffle(all_cards_data)

        # Create card objects
        self.cards = []
        start_x = (WINDOW_WIDTH - (GRID_SIZE * (CARD_WIDTH + CARD_MARGIN) - CARD_MARGIN)) // 2
        start_y = 120

        card_index = 0
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if card_index < len(all_cards_data):
                    x = start_x + col * (CARD_WIDTH + CARD_MARGIN)
                    y = start_y + row * (CARD_HEIGHT + CARD_MARGIN)
                    card = Card(all_cards_data[card_index], x, y)
                    self.cards.append(card)
                    card_index += 1

        # Load images with progress
        for i, card in enumerate(self.cards):
            self.loading_screen.set_progress(i, len(self.cards), "Loading character images")
            self.loading_screen.update(50)
            self.loading_screen.draw("Loading character images")
            card.load_image()

        print("All images loaded!")

    def create_celebration_particles(self, x, y, count=15):
        """Create particle effects for celebrations"""
        for _ in range(count):
            self.particles.append(Particle(x, y))

    def handle_card_click(self, pos: Tuple[int, int]):
        """Enhanced card click handling with smooth animations"""
        if self.game_won or len(self.flipped_cards) >= 2:
            return

        clicked_card = None
        for card in self.cards:
            if card.is_clicked(pos) and not card.is_flipped and not card.is_matched:
                clicked_card = card
                break

        if clicked_card:
            clicked_card.flip()
            self.flipped_cards.append(clicked_card)

            if len(self.flipped_cards) == 2:
                self.moves += 1
                pygame.time.set_timer(pygame.USEREVENT + 1, 1000)  # Check match after 1 second

    def check_match(self):
        """Enhanced match checking with combo system"""
        if len(self.flipped_cards) != 2:
            return

        card1, card2 = self.flipped_cards
        current_time = time.time()

        if card1.character_data['id'] == card2.character_data['id']:
            # Match found!
            card1.set_matched()
            card2.set_matched()
            self.matches_found += 1

            # Combo system
            if current_time - self.last_match_time < 3.0:  # 3 seconds for combo
                self.combo_count += 1
            else:
                self.combo_count = 1

            self.last_match_time = current_time

            # Celebration effects
            self.create_celebration_particles(card1.x + card1.width // 2, card1.y + card1.height // 2)
            self.create_celebration_particles(card2.x + card2.width // 2, card2.y + card2.height // 2)
            self.screen_shake = 200  # Screen shake duration

            # Check win condition
            if self.matches_found == self.total_pairs:
                self.game_won = True
                self.game_time = time.time() - self.start_time
                # Final celebration
                center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
                self.create_celebration_particles(center_x, center_y, 30)

        else:
            # No match - flip back after delay
            pygame.time.set_timer(pygame.USEREVENT + 2, 1200)

        # Clear flipped cards reference (but keep them visually flipped for now)
        self.flipped_cards = []

    def flip_back_non_matches(self):
        """Flip back non-matching cards with animation"""
        for card in self.cards:
            if card.is_flipped and not card.is_matched:
                # Only flip back if this card is not part of a current match
                should_flip_back = True
                for flipped in self.flipped_cards:
                    if flipped == card:
                        should_flip_back = False
                        break

                if should_flip_back:
                    card.flip()

    def update_effects(self, dt):
        """Update visual effects"""
        # Update particles
        self.particles = [p for p in self.particles if p.is_alive()]
        for particle in self.particles:
            particle.update(dt)

        # Update screen shake
        if self.screen_shake > 0:
            self.screen_shake -= dt

    def draw_enhanced_ui(self):
        """Draw enhanced UI with better typography and layout"""
        # Calculate shake offset
        shake_x = shake_y = 0
        if self.screen_shake > 0:
            shake_intensity = min(5, self.screen_shake / 40)
            shake_x = random.uniform(-shake_intensity, shake_intensity)
            shake_y = random.uniform(-shake_intensity, shake_intensity)

        # Apply shake to screen
        shake_offset = (int(shake_x), int(shake_y))

        # Background with gradient effect
        self.screen.fill(COLORS['background'])

        # Title with glow effect
        title_text = self.title_font.render("Star Wars Memory Game", True, COLORS['fireworks'])
        title_rect = title_text.get_rect()
        title_rect.centerx = WINDOW_WIDTH // 2 + shake_offset[0]
        title_rect.y = 20 + shake_offset[1]

        # Glow effect for title
        glow_text = self.title_font.render("Star Wars Memory Game", True, (255, 215, 0, 100))
        for offset in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
            glow_rect = title_rect.copy()
            glow_rect.x += offset[0]
            glow_rect.y += offset[1]
            self.screen.blit(glow_text, glow_rect)

        self.screen.blit(title_text, title_rect)

        # Game stats in a nice panel
        current_time = time.time() - self.start_time if not self.game_won else self.game_time
        minutes = int(current_time // 60)
        seconds = int(current_time % 60)

        stats_y = 70 + shake_offset[1]

        # Moves counter
        moves_text = f"Moves: {self.moves}"
        moves_surface = self.font.render(moves_text, True, COLORS['text_primary'])
        moves_rect = moves_surface.get_rect()
        moves_rect.x = 50 + shake_offset[0]
        moves_rect.y = stats_y
        self.screen.blit(moves_surface, moves_rect)

        # Matches counter
        matches_text = f"Matches: {self.matches_found}/{self.total_pairs}"
        matches_surface = self.font.render(matches_text, True, COLORS['text_primary'])
        matches_rect = matches_surface.get_rect()
        matches_rect.centerx = WINDOW_WIDTH // 2 + shake_offset[0]
        matches_rect.y = stats_y
        self.screen.blit(matches_surface, matches_rect)

        # Timer
        time_text = f"Time: {minutes:02d}:{seconds:02d}"
        time_surface = self.font.render(time_text, True, COLORS['text_primary'])
        time_rect = time_surface.get_rect()
        time_rect.right = WINDOW_WIDTH - 50 + shake_offset[0]
        time_rect.y = stats_y
        self.screen.blit(time_surface, time_rect)

        # Combo indicator
        if self.combo_count > 1:
            combo_text = f"COMBO x{self.combo_count}!"
            combo_color = COLORS['fireworks'] if self.combo_count < 5 else COLORS['success']
            combo_surface = self.font.render(combo_text, True, combo_color)
            combo_rect = combo_surface.get_rect()
            combo_rect.centerx = WINDOW_WIDTH // 2 + shake_offset[0]
            combo_rect.y = stats_y + 30
            self.screen.blit(combo_surface, combo_rect)

    def draw_win_screen(self):
        """Enhanced win screen with statistics"""
        if not self.game_won:
            return

        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Win message
        win_text = self.large_font.render("Victory!", True, COLORS['fireworks'])
        win_rect = win_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80))
        self.screen.blit(win_text, win_rect)

        # Statistics
        minutes = int(self.game_time // 60)
        seconds = int(self.game_time % 60)

        stats = [
            f"Time: {minutes:02d}:{seconds:02d}",
            f"Moves: {self.moves}",
            f"Best Combo: x{max(1, self.combo_count)}"
        ]

        for i, stat in enumerate(stats):
            stat_surface = self.font.render(stat, True, COLORS['text_primary'])
            stat_rect = stat_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20 + i * 30))
            self.screen.blit(stat_surface, stat_rect)

        # Instructions
        restart_text = self.font.render("Press R to restart or ESC to exit", True, COLORS['text_secondary'])
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
        self.screen.blit(restart_text, restart_rect)

    def draw(self):
        """Enhanced main draw function"""
        dt = self.clock.get_time()

        # Update effects
        self.update_effects(dt)

        # Draw UI
        self.draw_enhanced_ui()

        # Update and draw cards
        for card in self.cards:
            card.update(dt, self.mouse_pos)
            card.draw(self.screen, self.font, self.small_font)

        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)

        # Draw win screen if game is won
        self.draw_win_screen()

        pygame.display.flip()

    def restart_game(self):
        """Restart with smooth transitions"""
        self.__init__()

    def run(self):
        """Enhanced main game loop"""
        running = True

        while running:
            dt = self.clock.get_time()

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
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_pos = event.pos
                elif event.type == pygame.USEREVENT + 1:
                    # Check for match
                    pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Cancel timer
                    self.check_match()
                elif event.type == pygame.USEREVENT + 2:
                    # Flip back non-matching cards
                    pygame.time.set_timer(pygame.USEREVENT + 2, 0)  # Cancel timer
                    self.flip_back_non_matches()

            self.draw()
            self.clock.tick(60)  # 60 FPS for smooth animations

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    print("Starting Enhanced Star Wars Memory Game...")
    game = MemoryGame()
    game.run()
