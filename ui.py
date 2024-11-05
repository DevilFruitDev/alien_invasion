# ui.py
import pygame

class UI:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)  # Default font
        self.score = 0
        self.lives = 3

    def update_score(self, points):
        self.score += points

    def update_lives(self, change):
        self.lives += change

    def draw(self, screen):  # Pass the screen as a parameter here
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        lives_text = self.font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (screen.get_width() - 100, 10))
