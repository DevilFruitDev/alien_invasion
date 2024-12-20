import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, screen, ship):
        super().__init__()
        self.screen = screen
        self.speed = 7  # Adjusted speed for better gameplay
        
        # Load the bullet sprite
        try:
            # Load and store original image - using raw string for path
            self.original_image = pygame.image.load(r'C:\Users\mhspi\Desktop\PYgame\assets\PNG_Parts&Spriter_Animation\Shots\Shot1\shot1_1.png').convert_alpha()
            # Scale the bullet (adjust size as needed)
            bullet_scale = 0.5  # Adjust this value to change bullet size
            original_size = self.original_image.get_rect().size
            new_size = (int(original_size[0] * bullet_scale), int(original_size[1] * bullet_scale))
            self.image = pygame.transform.scale(self.original_image, new_size)
            # Rotate to face upward
            self.image = pygame.transform.rotate(self.image, 90)
        except FileNotFoundError:
            # Fallback if image not found
            self.image = pygame.Surface((4, 16))
            self.image.fill((0, 255, 0))  # Green fallback bullet
        
        # Get the bullet's rect
        self.rect = self.image.get_rect()
        
        # Position the bullet at the ship's position
        self.rect.midtop = ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        self.y -= self.speed
        self.rect.y = self.y