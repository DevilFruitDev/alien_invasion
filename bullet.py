# bullet.py
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, screen, ship):
        super().__init__()
        self.screen = screen
        self.color = (60, 60, 60)
        self.speed = 5
        
        # Create the bullet at the ship's current position
        self.rect = pygame.Rect(0, 0, 3, 15)  # Bullet dimensions
        self.rect.midtop = ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
