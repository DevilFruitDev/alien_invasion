import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and store original
        try:
            self.original_image = pygame.image.load(r'C:\Users\mhspi\Desktop\PYgame\assets\PNG_Parts&Spriter_Animation\Ship1\Ship1.png').convert_alpha()
            self.original_image = pygame.transform.scale(self.original_image, (64, 64))
            # Create rotated version
            self.image = pygame.transform.rotate(self.original_image, 90)
        except FileNotFoundError:
            print("Warning: Could not load ship sprite, using default")
            self.original_image = pygame.Surface((64, 64))
            self.original_image.fill((0, 255, 0))
            self.image = self.original_image
        
        # Get the ship's rect
        self.rect = self.image.get_rect()
        
        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        
        # Store a decimal value for the ship's horizontal position
        self.x = float(self.rect.x)

        # Movement flags
        self.moving_right = False
        self.moving_left = False

        # Health attributes
        self.max_health = 100
        self.current_health = self.max_health
        self.is_invulnerable = False
        self.invulnerable_timer = 0

    def update(self):
        """Update the ship's position based on movement flags."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update rect object from self.x
        self.rect.x = self.x

    def take_damage(self, amount):
        """Handle taking damage and invulnerability frames"""
        if not self.is_invulnerable:
            self.current_health -= amount
            self.is_invulnerable = True
            self.invulnerable_timer = pygame.time.get_ticks()
            return True
        return False

    def heal(self, amount):
        """Heal the ship"""
        self.current_health = min(self.current_health + amount, self.max_health)