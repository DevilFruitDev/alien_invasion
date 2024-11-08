# enemy_bullet.py
import pygame
from pygame.sprite import Sprite

class EnemyBullet(Sprite):
    def __init__(self, x, y, screen):
        super().__init__()
        self.screen = screen
        self.color = (255, 0, 0)  # Red color for enemy bullets
        self.speed = 3  # Adjust as needed
        
        # Create the bullet rect at the enemy's position
        self.rect = pygame.Rect(0, 0, 3, 15)
        self.rect.midtop = (x, y)
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet down the screen."""
        self.y += self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
