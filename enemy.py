import pygame
from pygame.sprite import Sprite

class Enemy(Sprite):
    """A class to represent a single enemy in the fleet."""

    def __init__(self, ai_game, enemy_type='grunt'):
        """Initialize the enemy and set its type and behavior."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.enemy_type = enemy_type

        # Load different images based on enemy type
        if self.enemy_type == 'grunt':
            self.image = pygame.image.load('')
        elif self.enemy_type == 'scout':
            self.image = pygame.image.load('')
        elif self.enemy_type == 'bruiser':
            self.image = pygame.image.load('')

        # Resize the image
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

        # Start position
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Movement attributes
        self.x = float(self.rect.x)
        self.speed_x = self.settings.enemy_speed
        self.speed_y = 0

        # Adjust attributes based on type
        if self.enemy_type == 'scout':
            self.speed_x = 2 * self.settings.enemy_speed
        elif self.enemy_type == 'bruiser':
            self.speed_x = 0
            self.speed_y = 1

    def update(self):
        """Update the enemy's position."""
        if self.enemy_type == 'grunt':
            self.x += (self.speed_x * self.settings.enemy_direction)
            self.rect.x = self.x
        elif self.enemy_type == 'scout':
            self.x += self.speed_x
            if self.rect.right >= self.screen.get_width() or self.rect.left <= 0:
                self.speed_x = -self.speed_x  # Reverse direction
            self.rect.x = self.x
        elif self.enemy_type == 'bruiser':
            self.rect.y += self.speed_y

    def check_edges(self):
        """Return True if the enemy is at the edge of the screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        return False


    def blitme(self):
        """Draw the enemy at its current location."""
        self.screen.blit(self.image, self.rect)
