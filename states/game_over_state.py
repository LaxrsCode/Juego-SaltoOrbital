
import pygame
from states.base_state import BaseState
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GREEN, RED, YELLOW, SPACE_BLUE
from utils.asset_loader import load_image

class GameOverState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.font_large = pygame.font.Font(None, 64)
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        try:
            self.victory_img = load_image("robot_victory.png", (100, 100))
        except:
            self.victory_img = None
        
        try:
            self.defeat_img = load_image("robot_dead.png", (100, 100))
        except:
            self.defeat_img = None
        
        # Temporizador para volver al menú automáticamente
        self.timer = 0
    
    def init(self):
        """Inicializa el estado de game over"""
        # Resetear el temporizador
        self.timer = 300  # 5 segundos en frames (60 fps)
    
    def update(self, events):
        """
        Actualiza el estado de game over
        
        Args:
            events: Lista de eventos de pygame
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    # Volver al menú
                    self.game.change_state('menu')
                elif event.key == pygame.K_r:
                    # Reiniciar el nivel
                    self.game.change_state('game')
        
        # Actualizar temporizador
        self.timer -= 1
        if self.timer <= 0:
            # Volver al menú automáticamente
            self.game.change_state('menu')
    
    def draw(self, screen):
        """
        Dibuja el estado de game over
        
        Args:
            screen: Superficie de pantalla donde dibujar
        """
        # Dibujar fondo
        screen.fill(SPACE_BLUE)
        
        # Determinar mensaje según victoria o derrota
        if self.game.victory:
            # Victoria
            message = "¡NIVEL COMPLETADO!"
            color = GREEN
            secondary_message = f"Has recolectado todos los engranajes del nivel {self.game.selected_level}"
            img = self.victory_img
        else:
            # Derrota
            message = "GAME OVER"
            color = RED
            secondary_message = "No has podido completar la misión"
            img = self.defeat_img
        
        # Dibujar mensaje principal
        text = self.font_large.render(message, True, color)
        text_rect = text.get_rect(centerx=SCREEN_WIDTH//2, centery=SCREEN_HEIGHT//3)
        screen.blit(text, text_rect)
        
        # Dibujar mensaje secundario
        sub_text = self.font.render(secondary_message, True, WHITE)
        sub_rect = sub_text.get_rect(centerx=SCREEN_WIDTH//2, centery=SCREEN_HEIGHT//3 + 60)
        screen.blit(sub_text, sub_rect)
        
        # Dibujar imagen si existe
        if img:
            img_rect = img.get_rect(centerx=SCREEN_WIDTH//2, centery=SCREEN_HEIGHT//2 + 20)
            screen.blit(img, img_rect)
        
        # Dibujar instrucciones
        instructions = [
            "Presiona ENTER para volver al menú",
            "Presiona R para reintentar el nivel",
            f"Volviendo al menú en {self.timer // 60 + 1} segundos..."
        ]
        
        y_pos = SCREEN_HEIGHT - 120
        for instruction in instructions:
            inst_text = self.small_font.render(instruction, True, YELLOW)
            inst_rect = inst_text.get_rect(centerx=SCREEN_WIDTH//2, y=y_pos)
            screen.blit(inst_text, inst_rect)
            y_pos += 30
    
    def reset(self):
        """Resetea el estado de game over"""
        pass