import random
import pygame
import  sys
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
        while True:
            if not self.game_over:
                self._process_input()
                self._update_game()
                self._render()
            else:
                self._display_game_over_screen()
            pygame.display.flip()

    def _process_input(self):
        """ Handle all user inputs or events. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _update_game(self):
        """ Update all game mechanics. """
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
        """ Render all game elements. """
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self.bullets.draw(self.screen)
        self.enemies.draw(self.screen)
        self.enemy_bullets.draw(self.screen)
        self.powerups.draw(self.screen)
        self.ui.draw(self.screen, self.ship)  # Modified this line to pass the ship

    def toggle_debug_mode(self):
        """Enhanced toggle debug mode with visual indicator."""
        self.debug_mode = not self.debug_mode
        
        # Visual feedback for debug mode
        if self.debug_mode:
            # Change ship color or add visual indicator
            self.ship.image.fill((0, 255, 0), special_flags=pygame.BLEND_RGB_ADD)
            print("Debug mode ON - Invulnerability activated")
        else:
            # Restore original ship appearance
            self.ship.image = pygame.image.load('C:\\Users\\mhspi\\Desktop\\PYgame\\Game Assets\\ship.bmp.png')
            self.ship.image = pygame.transform.scale(self.ship.image, (50, 50))
            print("Debug mode OFF - Normal gameplay resumed")
        
        # Reset enemy fleet when toggling debug mode
        if self.debug_mode:
            self.enemies.empty()
        else:
            self._create_fleet()

    def _display_game_over_screen(self):
        """Display Game Over screen with options to restart or quit."""
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, (255, 0, 0))
        self.screen.blit(text, (self.settings.screen_width // 2 - text.get_width() // 2,
                                self.settings.screen_height // 3))
        font_small = pygame.font.Font(None, 36)
        restart_text = font_small.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
        self.screen.blit(restart_text, (self.settings.screen_width // 2 - restart_text.get_width() // 2,
                                        self.settings.screen_height // 2))
        pygame.display.flip()

        while self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type is pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self._restart_game()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

    def _restart_game(self):
        """Reset the game to start fresh."""
        self.game_over = False
        self.ui = UI()
        self.enemies.empty()
        self.bullets.empty()
        self.powerups.empty()
        self.enemy_bullets.empty()
        self._create_fleet()
        self.ship = Ship(self)  # Reinitialize the ship and reset movement flags
        self.ship.moving_right = False
        self.ship.moving_left = False

    # In alien_invasion.py, update the _check_collisions method:
    def _check_collisions(self):
        """Handle all collision detections and reactions."""
        if not self.debug_mode:
            # Check for collisions between enemy bullets and the ship
            if pygame.sprite.spritecollideany(self.ship, self.enemy_bullets):
                if self.ship.take_damage(10):  # Regular bullet damage
                    if self.ship.current_health <= 0:
                        self.game_over = True

            # Check for collisions between enemies and the ship
            enemy_collision = pygame.sprite.spritecollideany(self.ship, self.enemies)
            if enemy_collision:
                # Different damage for different enemy types
                damage = {
                    'grunt': 15,
                    'scout': 20,
                    'bruiser': 30
                }.get(enemy_collision.enemy_type, 15)
                
                if self.ship.take_damage(damage):
                    if self.ship.current_health <= 0:
                        self.game_over = True

        # Always check for power-up collisions
        powerup_collision = pygame.sprite.spritecollideany(self.ship, self.powerups)
        if powerup_collision:
            if powerup_collision.power_type == 'extra_life':
                self.ship.heal(30)  # Heal 30 health points
            elif powerup_collision.power_type == 'fast_fire':
                # Implement fast-firing logic here
                pass
            powerup_collision.kill()

        # Check for bullet-enemy collisions
        collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        if collisions:
            for enemies_hit in collisions.values():
                self.ui.update_score(len(enemies_hit) * 10)



    def _fire_enemy_bullet(self):
        """Randomly fire a bullet from an enemy."""
        if self.enemies and random.randint(1, 100) == 10:  # Adjust probability for firing
            firing_enemy = random.choice(self.enemies.sprites())
            new_bullet = EnemyBullet(firing_enemy.rect.centerx, firing_enemy.rect.bottom, self.screen)
            self.enemy_bullets.add(new_bullet)

    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self.bullets.draw(self.screen)         # This replaces your bullet for loop
        self.enemies.draw(self.screen)
        self.enemy_bullets.draw(self.screen)   # This replaces your enemy bullet for loop
        self.powerups.draw(self.screen)        # This replaces your powerup for loop
        
        # Update UI with ship health
        self.ui.draw(self.screen, self.ship)
        
        pygame.display.flip()


  #update completed till today. 

    def _spawn_powerup(self):
        """Randomly spawn a power-up at a specified location."""
        x = random.randint(20, self.settings.screen_width - 20)
        y = 0  # Start from the top of the screen
        power_type = random.choice(['extra_life', 'fast_fire'])  # Add different power-up types
        powerup = PowerUp(self.screen, x, y, power_type)  # Only pass four arguments
        self.powerups.add(powerup)




    def _update_bullets(self):
        """Update the position of the bullets and get rid of the old ones."""
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        if collisions:
            for enemies_hit in collisions.values():
                self.ui.update_score(len(enemies_hit) * 10)  # Example: 10 points per enemy

    def _update_enemies(self):
        """Update the position of all enemies in the fleet, unless in debug mode."""
        if not self.debug_mode:  # Only update enemies if not in debug mode
            self.enemies.update()
            self._check_fleet_edges()


    def _check_fleet_edges(self):
        """Respond if any Grunts have reached an edge."""
        for enemy in self.enemies.sprites():
            if enemy.enemy_type == 'grunt' and enemy.check_edges():
                self._change_fleet_direction()
                break



    def _change_fleet_direction(self):
        """Drop the entire fleet and change their direction."""
        for enemy in self.enemies.sprites():
            if enemy.enemy_type == 'grunt':  # Only affect Grunts
                enemy.rect.y += 20
        self.settings.enemy_direction *= -1


    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _increase_speed(self):
        """Increase the speed of the fleet after each wave or significant event."""
        self.settings.enemy_speed *= 1.1  # Adjust this multiplier as needed for difficulty


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

    def _create_fleet(self):
        """Create a fleet of enemies only if not in debug mode."""
        if not self.debug_mode:  # Check if debug mode is active
            # Calculate the number of enemies in a row and rows of enemies
            enemy = Enemy(self, 'grunt')  # Temporary instance to get dimensions
            enemy_width, enemy_height = enemy.rect.size
            available_space_x = self.settings.screen_width - (1.5 * enemy_width)
            number_enemies_x = int(available_space_x // (1.5 * enemy_width))

            ship_height = self.ship.rect.height
            available_space_y = (self.settings.screen_height - (2 * enemy_height) - ship_height)
            number_rows = int(available_space_y // (1.5 * enemy_height))

            # Create the full fleet of enemies
            for row_number in range(number_rows):
                for enemy_number in range(number_enemies_x):
                    self._create_enemy(enemy_number, row_number)
                    print(f"Row: {row_number}, Enemy: {enemy_number}")
                    print(f"DEBUG: Total enemies in fleet: {len(self.enemies)}")

    def _create_enemy(self, enemy_number, row_number):
        """Create an enemy and place it in the row."""
        enemy_type = random.choice(['grunt', 'scout', 'bruiser'])
        print(f"DEBUG: Creating enemy of type {enemy_type} at Row: {row_number}, Enemy: {enemy_number}")
        enemy = Enemy(
            ai_game=self,
            enemy_type=enemy_type
        )
        # Position the enemy
        enemy.rect.x = 50 + enemy_number * (enemy.rect.width + 10)
        enemy.rect.y = 50 + row_number * (enemy.rect.height + 10)
        self.enemies.add(enemy)


        # Position the enemy based on its number and row
        enemy.rect.x = 50 + enemy_number * (enemy.rect.width + 10)
        enemy.rect.y = 50 + row_number * (enemy.rect.height + 10)

        # Add the enemy to the group
        self.enemies.add(enemy)

        print(f"Created {enemy_type} at ({enemy.rect.x}, {enemy.rect.y})")

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()