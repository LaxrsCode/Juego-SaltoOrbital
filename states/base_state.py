
class BaseState:
    def __init__(self, game):
        self.game = game
    
    def init(self):
        pass
    
    def update(self, events):
        pass
    
    def draw(self, screen):
        pass
    
    def reset(self):
        pass