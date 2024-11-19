class Settings: 
    """A class to store all the settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        #Game FPS
        self.fps = 30 #setting the frame rate. 

        # Ship settings
        self.ship_speed = 1.5

        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Enemy settings
        self.enemy_speed = 1.0
        self.enemy_direction = 1  # 1 represents right; -1 represents left
        self.enemy_drop_speed = 10 
