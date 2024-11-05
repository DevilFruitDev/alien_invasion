# game_state.py
class GameStateManager:
    def __init__(self):
        self.state = "main_menu"  # Possible states: "playing", "paused", "game_over"
    
    def handle_events(self, event):
        if self.state == "main_menu" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.state = "playing"
