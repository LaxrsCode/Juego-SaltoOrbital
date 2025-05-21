import pygame
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE
from states.menu_state import MenuState
from states.game_state import GameState
from states.game_over_state import GameOverState

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        self.states = {
            'menu': MenuState(self),
            'game': GameState(self),
            'game_over': GameOverState(self)
        }
        
        self.current_state = 'menu'
        
        self.selected_level = 1 
        self.victory = False     
    
    def run(self):
        running = True
        
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
            
            self.states[self.current_state].update(events)
            
            self.states[self.current_state].draw(self.screen)
            
            pygame.display.flip()
            
            self.clock.tick(FPS)
    
    def change_state(self, new_state):
        if new_state in self.states:
            self.states[self.current_state].reset()
            # Cambiar al nuevo estado
            self.current_state = new_state
            # Inicializar el nuevo estado
            self.states[self.current_state].init()