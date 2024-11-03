import pygame
from pygame.sprite import Sprite

class Enemy(Sprite):
    """A class to represent a single enemy in the fleet."""

    def __init__(self, ai_game):
        """Initialize the enemy and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the enemy image and resize it
        self.image = pygame.image.load('Flyingsaucer.png')
        self.image = pygame.transform.scale(self.image, (50, 50))  # Adjust size as needed
        self.rect = self.image.get_rect()

        # Start each new enemy near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the enemy's exact horizontal position
        self.x = float(self.rect.x)

    def update(self):
        """Move the enemy left or right."""
        self.x += (self.settings.enemy_speed * self.settings.enemy_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Return True if enemy is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def blitme(self):
        """Draw the enemy at its current location."""
        self.screen.blit(self.image, self.rect)
