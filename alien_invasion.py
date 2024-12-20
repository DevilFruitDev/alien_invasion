import random
import pygame
import sys
from settings import Settings
from ui import UI
from ship import Ship
from bullet import Bullet
from enemy import Enemy
from enemy_bullet import EnemyBullet
from powerup import PowerUp

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Initialize game elements
        self.ui = UI()
        self.enemy_count = 0  # Add this counter
        self.ship = Ship(self)
        self.clock = pygame.time.Clock()
        self.start_ticks = pygame.time.get_ticks()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()

        self.debug_mode = False  # Debug mode state
        self.game_over = False

        self._create_fleet()

    def run_game(self):
        """Main game loop."""
        while True:
            if not self.game_over:
                self._process_input()
                self._update_game()
                self._render()
            else:
                self._display_game_over_screen()
            pygame.display.flip()

    def _process_input(self):
        """Handle all user inputs or events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _update_game(self):
        """Update all game mechanics."""
        seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
        self.ship.update()
        self._update_bullets()
        if not self.debug_mode:
            self._update_enemies()
        self.powerups.update()
        self.enemy_bullets.update()
        self._check_collisions()
        self.ui.show_time(self.screen, seconds)
        self.clock.tick(self.settings.fps)

    def _render(self):
        """Render all game elements."""
        self.screen.fill(self.settings.bg_color)
        # Instead of self.ship.blitme(), use this:
        self.screen.blit(self.ship.image, self.ship.rect)  # Draw the ship
        self.bullets.draw(self.screen)
        self.enemies.draw(self.screen)
        self.enemy_bullets.draw(self.screen)
        self.powerups.draw(self.screen)
        self.ui.draw(self.screen, self.ship)

    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_d:
            self.toggle_debug_mode()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self.screen, self.ship)
            self.bullets.add(new_bullet)

    def _fire_enemy_bullet(self):
        """Randomly fire a bullet from an enemy."""
        if self.enemies and random.randint(1, 100) == 10:
            firing_enemy = random.choice(self.enemies.sprites())
            new_bullet = EnemyBullet(firing_enemy.rect.centerx, firing_enemy.rect.bottom, self.screen)
            self.enemy_bullets.add(new_bullet)

    def _update_bullets(self):
        """Update the position of bullets and handle collisions."""
        self.bullets.update()

        # Remove bullets that have gone off screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Handle bullet collisions
        collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        if collisions:
            for enemies_hit in collisions.values():
                self.ui.update_score(len(enemies_hit) * 10)

    def _update_enemies(self):
        """Update the positions of all enemies in the fleet."""
        if not self.debug_mode:
            self._check_fleet_edges()
            self.enemies.update()
            
            # Look for enemies hitting the bottom
            screen_rect = self.screen.get_rect()
            for enemy in self.enemies.sprites():
                if enemy.rect.bottom >= screen_rect.bottom:
                    # Treat this the same as if the ship got hit
                    self.game_over = True
                    break

    def _create_fleet(self):
        """Create the fleet of enemies."""
        if not self.debug_mode:
            # Create an enemy and calculate how many fit in a row
            enemy = Enemy(self)
            enemy_width, enemy_height = enemy.rect.size
            available_space_x = self.settings.screen_width - (2 * enemy_width)
            number_enemies_x = int(available_space_x // (2 * enemy_width))

            # Determine number of rows that fit on screen
            ship_height = self.ship.rect.height
            available_space_y = (self.settings.screen_height - 
                            (3 * enemy_height) - ship_height)
            number_rows = int(available_space_y // (2 * enemy_height))

            # Create the fleet
            for row_number in range(number_rows):
                for enemy_number in range(number_enemies_x):
                    self._create_enemy(enemy_number, row_number)
                    
            print(f"Created fleet with {len(self.enemies)} enemies")

    def _create_enemy(self, enemy_number, row_number):
        """Create an enemy and place it in the row."""
        enemy = Enemy(self)
        enemy_width, enemy_height = enemy.rect.size
        
        # Calculate position
        enemy.x = enemy_width + 2 * enemy_width * enemy_number
        enemy.rect.x = enemy.x
        enemy.rect.y = enemy_height + 2 * enemy_height * row_number
        
        self.enemies.add(enemy)

    def _check_fleet_edges(self):
        """Respond appropriately if any enemies have reached an edge."""
        for enemy in self.enemies.sprites():
            if enemy.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for enemy in self.enemies.sprites():
            enemy.rect.y += self.settings.enemy_drop_speed
        self.settings.enemy_direction *= -1


    def _spawn_powerup(self):
        """Spawn a random power-up."""
        x = random.randint(20, self.settings.screen_width - 20)
        y = 0
        power_type = random.choice(['extra_life', 'fast_fire'])
        powerup = PowerUp(self.screen, x, y, power_type)
        self.powerups.add(powerup)

    def _check_collisions(self):
        """Handle all collision detection."""
        if not self.debug_mode:
            # Ship-enemy bullet collisions
            if pygame.sprite.spritecollideany(self.ship, self.enemy_bullets):
                if self.ship.take_damage(10):
                    if self.ship.current_health <= 0:
                        self.game_over = True

            # Ship-enemy collisions
            enemy_collision = pygame.sprite.spritecollideany(self.ship, self.enemies)
            if enemy_collision:
                damage = {
                    'grunt': 15,
                    'scout': 20,
                    'bruiser': 30
                }.get(enemy_collision.enemy_type, 15)
                
                if self.ship.take_damage(damage):
                    if self.ship.current_health <= 0:
                        self.game_over = True

        # Power-up collisions
        powerup_collision = pygame.sprite.spritecollideany(self.ship, self.powerups)
        if powerup_collision:
            if powerup_collision.power_type == 'extra_life':
                self.ship.heal(30)
            elif powerup_collision.power_type == 'fast_fire':
                pass  # Implement fast-fire logic
            powerup_collision.kill()

    def toggle_debug_mode(self):
        """Toggle debug mode."""
        self.debug_mode = not self.debug_mode
        
        if self.debug_mode:
            self.ship.image.fill((0, 255, 0), special_flags=pygame.BLEND_RGB_ADD)
            print("Debug mode ON - Invulnerability activated")
        else:
            # Make sure this path matches your actual file structure
            try:
                self.ship.image = pygame.image.load('C:\\Users\\mhspi\\Desktop\\PYgame\\assets\\PNG_Parts&Spriter_Animation\\Ship1\\Ship1.png').convert_alpha()
                self.ship.image = pygame.transform.scale(self.ship.image, (64, 64))
            except FileNotFoundError:
                print("Warning: Could not load ship sprite, using default")
                # Create a default colored rectangle if sprite can't be loaded
                self.ship.image = pygame.Surface((64, 64))
                self.ship.image.fill((0, 255, 0))
            print("Debug mode OFF - Normal gameplay resumed")
        
        if self.debug_mode:
            self.enemies.empty()
        else:
            self._create_fleet()

    def _display_game_over_screen(self):
        """Show game over screen."""
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, (255, 0, 0))
        restart_text = pygame.font.Font(None, 36).render(
            "Press R to Restart or Q to Quit", True, (255, 255, 255))
        
        self.screen.blit(text, (self.settings.screen_width // 2 - text.get_width() // 2,
                               self.settings.screen_height // 3))
        self.screen.blit(restart_text, (self.settings.screen_width // 2 - restart_text.get_width() // 2,
                                      self.settings.screen_height // 2))
        pygame.display.flip()

        while self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self._restart_game()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

    def _restart_game(self):
        """Reset the game state."""
        self.game_over = False
        self.ui = UI()
        self.enemies.empty()
        self.bullets.empty()
        self.powerups.empty()
        self.enemy_bullets.empty()
        self._create_fleet()
        self.ship = Ship(self)
        self.ship.moving_right = False
        self.ship.moving_left = False

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()