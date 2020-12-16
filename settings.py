class Settings: 
	"""A class to store all the settings for alien invasion"""

	def __init__(self):
		"""initialize the game´s settings"""
		#screen settings
		self.screen_width = 800
		self.screen_height = 600
		self.bg_color= (230,230,230)

		#Ship Settings
		self.ship_speed = 1.5

		#bullets settings
		self.bullet_speed  =1.0
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color =(60,60,60)
		self.bullets_allowed = 3