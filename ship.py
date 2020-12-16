import pygame

class Ship:
	"""a class that manages the ship"""
	def __init__(self, ai_game):
		"""initialize the ship and set it to a starting position"""
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = ai_game.screen.get_rect()

		#load the image  and its rect. 
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()

		#Start each new ship at the bottom of the screen
		self.rect.midbottom = self.screen_rect.midbottom

		#Store a decimal value for the ships horizontal positions 
		self.x = float(self.rect.x)
		#self.y = float(self.rect.y)

		#movement flag
		self.moving_right = False
		self.moving_left  = False
		#self.moving_up = False
		#self.moving_down = False

	def update(self):
		"""update the ship right position based on the movement of the flag"""
		#update the ships x value not the rect. 
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.settings.ship_speed
			#moving left
		if self.moving_left and self.rect.left > 0:
			self.x -= self.settings.ship_speed
			#moving up
		#if self.moving_up and self.rect.top > 0:
		#	self.y -= self.settings.ship_speed
			#moving down
		#if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
		#	self.y += self.settings.ship_speed


		#update rect object from self.x 
		self.rect.x = self.x
		#self.rect.y = self.y

	def blitme(self):
		"""draw the ship at its current location"""
		self.screen.blit(self.image, self.rect)