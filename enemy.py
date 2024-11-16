import pygame
from pygame.sprite import Sprite
import random
import math  # Add this for the sine function



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
            self.image = pygame.image.load('C:\\Users\\mhspi\\Desktop\\PYgame\\grunt.png')
        elif self.enemy_type == 'scout':
            self.image = pygame.image.load('C:\\Users\\mhspi\\Desktop\\PYgame\\scout.png')
        elif self.enemy_type == 'bruiser':
            self.image = pygame.image.load('C:\\Users\\mhspi\\Desktop\\PYgame\\bruiser.png')

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
            # Initialize local direction for this grunt if not already set
            if not hasattr(self, 'direction'):
                self.direction = 1  # Start moving to the right

            # Update horizontal position with local direction
            self.x += (self.speed_x * self.direction)

            # Reverse direction locally at edges
            if self.rect.right >= self.screen.get_width() or self.rect.left <= 0:
                self.direction *= -1  # Reverse this grunt's direction
                self.x += self.speed_x * self.direction  # Prevent overlap

            # Update the rectangle's x position
            self.rect.x = self.x


        elif self.enemy_type == 'scout':
            # Update both horizontal and vertical positions
            self.x += self.speed_x
            self.rect.x = self.x
            self.rect.y += self.speed_y

            # Bounce off edges
            if self.rect.right >= self.screen.get_width() or self.rect.left <= 0:
                print("DEBUG: Scout hit horizontal edge. Reversing x-direction.")
                self.speed_x *= -1  # Reverse horizontal direction
            if self.rect.bottom >= self.screen.get_height() or self.rect.top <= 0:
                print("DEBUG: Scout hit vertical edge. Reversing y-direction.")
                self.speed_y *= -1  # Reverse vertical direction


    def update(self):
        """Update the enemy's position."""
        if self.enemy_type == 'grunt':
            # Update horizontal position with local direction reversal
            self.x += (self.speed_x * self.settings.enemy_direction)
            
            # Reverse direction locally at edges
            if self.rect.right >= self.screen.get_width() or self.rect.left <= 0:
                self.settings.enemy_direction *= -1
                self.x += self.speed_x * self.settings.enemy_direction  # Prevent overlap
            
            # Create unique base_y for each grunt
            if not hasattr(self, "base_y"):
                self.base_y = self.rect.y  # Set the grunt's initial y-position as its base

            # Add vertical oscillation
            oscillation_amplitude = 15  # How high/low the wave goes
            self.rect.y = self.base_y + int(oscillation_amplitude * math.sin(self.x / 50))

            # Update the rectangle's x position
            self.rect.x = self.x

        elif self.enemy_type == 'scout':
            # Update both horizontal and vertical positions
            self.x += self.speed_x
            self.rect.x = self.x
            self.rect.y += self.speed_y

            # Bounce off edges
            if self.rect.right >= self.screen.get_width() or self.rect.left <= 0:
                print("DEBUG: Scout hit horizontal edge. Reversing x-direction.")
                self.speed_x *= -1  # Reverse horizontal direction
            if self.rect.bottom >= self.screen.get_height() or self.rect.top <= 0:
                print("DEBUG: Scout hit vertical edge. Reversing y-direction.")
                self.speed_y *= -1  # Reverse vertical direction

        elif self.enemy_type == 'bruiser':
            # Move vertically
            self.rect.y += self.speed_y

            # Reset position if it goes off-screen
            if self.rect.top > self.screen.get_height():  # If it moves off the bottom
                print("DEBUG: Bruiser moved off-screen. Resetting position.")
                self.rect.y = -self.rect.height  # Reset to just above the screen
                self.rect.x = random.randint(0, self.screen.get_width() - self.rect.width)  # Randomize x-position

    def check_edges(self):
        """Return True if the enemy is at the edge of the screen."""
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0



    def blitme(self):
        """Draw the enemy at its current location."""
        self.screen.blit(self.image, self.rect)
