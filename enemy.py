import pygame
from pygame.sprite import Sprite

class Enemy(Sprite):
    """A class to represent a single enemy in the fleet."""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the enemy image
        try:
            self.image = pygame.image.load('C:\\Users\\mhspi\\Desktop\\PYgame\\grunt.png')
            self.image = pygame.transform.scale(self.image, (50, 50))
        except FileNotFoundError:
            print("Warning: Could not load enemy sprite, using default")
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))  # Red color for enemy

        self.rect = self.image.get_rect()

        # Start each new enemy near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the enemy's exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if enemy is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right or self.rect.left <= 0)

    def update(self):
        """Move the enemy right or left."""
        self.x += (self.settings.enemy_speed * self.settings.enemy_direction)
        self.rect.x = self.x