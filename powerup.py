# powerup.py
import pygame

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, screen):
        super().__init__()
        self.screen = screen  # Store the screen reference
        self.image = pygame.Surface((20, 20))  # Simple block for now
        self.image.fill((0, 255, 0))  # Green power-up
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > self.screen.get_height():
            self.kill()

    def draw(self):
        self.screen.blit(self.image, self.rect)
