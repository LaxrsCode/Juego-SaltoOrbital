import pygame
import random
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from utils.asset_loader import load_image
from physic.collision import is_on_screen

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        super().__init__() 
        size = random.randint(30, 60)

        try:
            self.image = load_image("Asteroide.png", (size, size))
        except:
            self.image = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (150, 150, 150), (size // 2, size // 2), size // 2)
        
        # Crear el rectángulo de colisión
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Velocidad
        self.dx = dx
        self.dy = dy
        
        # Rotación
        self.angle = 0
        self.rotation_speed = random.uniform(-3, 3)
        self.original_image = self.image.copy()
    
    def update(self):
        """
        Actualiza la posición y rotación del asteroide
        """
        # Actualizar posición
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        # Rotar el asteroide
        self.angle = (self.angle + self.rotation_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        
        # Mantener la posición del centro
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        
        # Eliminar si sale de la pantalla
        if not is_on_screen(self.rect, padding=100):
            self.kill()
