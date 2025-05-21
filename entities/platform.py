import pygame
from utils.constants import PLATFORM_HEIGHT, GRAY
from utils.asset_loader import load_image

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        
        try:
            self.image = load_image("Plataforma-1-1-2.png", (width, 40))
        except:
            self.image = pygame.Surface((width, PLATFORM_HEIGHT))
            self.image.fill(GRAY)
        
        # Crear el rectángulo de colisión
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        pass