import pygame
from states.base_state import BaseState
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, BLUE, YELLOW, SPACE_BLUE, FONT_PATH
from utils.asset_loader import load_image

class MenuState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.title_font = pygame.font.Font(FONT_PATH, 64)
        self.text_font = pygame.font.Font(FONT_PATH, 32)
        self.small_font = pygame.font.Font(FONT_PATH, 24)
        
        # Opciones del menú
        self.options = ["Nivel 1 - Fácil", "Nivel 2 - Medio", "Nivel 3 - Difícil"]
        self.selected_option = 0
        
        # Historia del juego
        self.story_text = [
            "La nave espacial en la que viajaba nuestro robot se destruyó",
            "frente a la luna y quedó atrapado en una lluvia de asteroides.",
            "El robot debe sobrevivir y recolectar engranajes para reparar",
            "la nave y escapar de este peligroso entorno."
        ]
        
        # Intentar cargar la imagen de fondo
        try:
            self.background = load_image("Fondo.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.background = None
    
    def init(self):
        # Preseleccionar el nivel guardado
        self.selected_option = self.game.selected_level - 1
    
    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    # Guardar el nivel seleccionado
                    self.game.selected_level = self.selected_option + 1
                    # Cambiar al estado del juego
                    self.game.change_state('game')
    
    def draw(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(SPACE_BLUE)
        
        title_text = self.title_font.render("SALTO ORBITAL", True, WHITE)
        title_rect = title_text.get_rect(centerx=SCREEN_WIDTH//2, y=50)
        screen.blit(title_text, title_rect)
        
        story_y = 150
        for line in self.story_text:
            text = self.small_font.render(line, True, WHITE)
            rect = text.get_rect(centerx=SCREEN_WIDTH//2, y=story_y)
            screen.blit(text, rect)
            story_y += 30
        
        menu_y = 300
        for i, option in enumerate(self.options):
            if i == self.selected_option:
                color = YELLOW
                indicator = "➤ "
            else:
                color = WHITE
                indicator = "  "
            
            text = self.text_font.render(indicator + option, True, color)
            rect = text.get_rect(centerx=SCREEN_WIDTH//2, y=menu_y)
            screen.blit(text, rect)
            menu_y += 50
        
        instructions = "Usa las flechas ↑↓ para seleccionar y Enter para jugar"
        inst_text = self.small_font.render(instructions, True, WHITE)
        inst_rect = inst_text.get_rect(centerx=SCREEN_WIDTH//2, bottom=SCREEN_HEIGHT-20)
        screen.blit(inst_text, inst_rect)
    
    def reset(self):
        pass