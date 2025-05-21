import pygame
import math
from utils.asset_loader import load_image

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, image_name, size=(30, 30)):
        super().__init__()
        
        # Cargar imagen
        try:
            self.image = load_image(image_name, size)
        except:
            # Si no se puede cargar la imagen, crear un círculo
            self.image = pygame.Surface(size, pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 255, 0), (size[0]//2, size[1]//2), size[0]//2)
        
        # Crear rectángulo de colisión
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Variables para animación flotante
        self.float_offset = 0
        self.original_y = y
        self.float_speed = 0.05
        self.float_range = 5
    
    def update(self):
        # Animación flotante
        self.float_offset += self.float_speed
        self.rect.y = self.original_y + math.sin(self.float_offset) * self.float_range

class Energy(Collectible):
    def __init__(self, x, y):
        super().__init__(x, y, "Punto_vida.png", (30, 30))
        
        # Efecto de brillo
        self.glow_timer = 0
        self.glow_speed = 0.1
        self.original_image = self.image.copy()
    
    def update(self):
        super().update()
        
        self.glow_timer += self.glow_speed
        glow_factor = abs(math.sin(self.glow_timer)) * 0.3 + 0.7
        
        # # Aplicar brillo a la imagen
        # self.image = self.original_image.copy()
        # if hasattr(self.image, 'fill'):
        #     self.image.fill((255, 255, 255, int(glow_factor * 255)), special_flags=pygame.BLEND_RGB_ADD)

class Gear(Collectible):
    def __init__(self, x, y):
        super().__init__(x, y, "Escombros.png", (25, 25))
        
        # Rotación
        self.angle = 0
        self.rotation_speed = 1
        self.original_image = self.image.copy()
    
    def update(self):
        super().update()
        
        # Rotación
        self.angle = (self.angle + self.rotation_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        
        # Mantener la posición del centro
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center