# powerup.py
import pygame
from pygame.sprite import Sprite

class PowerUp(Sprite):
    def __init__(self, screen, x, y, power_type):
        """Initialize the power-up."""
        super().__init__()
        self.screen = screen
        self.power_type = power_type  # e.g., 'extra_life', 'fast_fire'
        self.image = pygame.Surface((20, 20))  # Create a simple square for the power-up
        
        # Set color based on power-up type
        if self.power_type == 'extra_life':
            self.image.fill((0, 255, 0))  # Green for extra life
        elif self.power_type == 'fast_fire':
            self.image.fill((255, 215, 0))  # Gold for faster firing

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 2  # Set the speed at which the power-up falls

    def update(self):
        """Move the power-up down the screen."""
        self.rect.y += self.speed
        if self.rect.top > self.screen.get_height():
            self.kill()  # Remove the power-up if it goes off the screen

    def draw(self):
        """Draw the power-up to the screen."""
        self.screen.blit(self.image, self.rect)
