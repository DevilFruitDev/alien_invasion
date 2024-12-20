# spritesheet.py
import pygame

class SpriteSheet:
    def __init__(self, filename):
        """Load the sprite sheet."""
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)
    
    def get_sprite(self, x, y, width, height):
        """Get a single sprite from the sheet."""
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        return sprite
    
    def get_sprite_strip(self, x, y, width, height, frames):
        """Get multiple sprites for animation."""
        sprites = []
        for frame in range(frames):
            sprite = self.get_sprite(x + frame * width, y, width, height)
            sprites.append(sprite)
        return sprites