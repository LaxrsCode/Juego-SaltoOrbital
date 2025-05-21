import pygame
from utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, PLAYER_JUMP_POWER,
    PLAYER_MAX_HEALTH, PLAYER_DAMAGE
)
from utils.asset_loader import load_image, load_sound
from physic.gravity import LunarMovement
from physic.collision import check_platform_collision

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        self.images = {
            'idle': load_image("Jugador.png", (50, 70)),
            'idle_left': load_image("Jugador.png", (50, 70), flip_x=True),
            'jump': load_image("Jugador_saltando.png", (50, 70)),
            'jump_left': load_image("Jugador_saltando.png", (50, 70), flip_x=True),
            'life': load_image("Jugador_vida.png", (50, 70)),
            'life_left': load_image("Jugador_vida.png", (50, 70), flip_x=True),
            'dead': load_image("Jugador_caido.png", (50, 70))
        }
        
        self.image = self.images['idle']
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = PLAYER_SPEED
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True
        
        self.movement = LunarMovement(self)
        
        self.health = PLAYER_MAX_HEALTH
        
        self.is_hit = False
        self.hit_timer = 0
        self.is_dead = False
        
        
        self.jump_sound = load_sound("salto.mp3")
        self.hit_sound = load_sound("golpe.mp3")
        self.energy_sound = load_sound("energia.mp3")
    
    def update(self, platforms):
        if self.is_dead:
            return
        
        # Obtener input del teclado
        keys = pygame.key.get_pressed()
        dx = 0
        
        if keys[pygame.K_LEFT]:
            dx = -1
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            dx = 1
            self.facing_right = True
        
        if keys[pygame.K_SPACE] and self.on_ground:
            self._jump()
        
        self.movement.update(dx)
        
        self._check_platform_collisions(platforms)
        
        self._check_screen_bounds()
        
        self._update_animation()
        
        if self.is_hit:
            self.hit_timer -= 1
            if self.hit_timer <= 0:
                self.is_hit = False
    
    def _jump(self):
        if self.movement.jump(PLAYER_JUMP_POWER):
            # Reproducir sonido de salto
            if self.jump_sound:
                self.jump_sound.play()
    
    def _check_platform_collisions(self, platforms):
        was_on_ground = self.on_ground
        self.on_ground = False
        
        # Comprobar colisiones
        platform = check_platform_collision(self, platforms)
        if platform:
            # Colocar al jugador encima de la plataforma
            self.rect.bottom = platform.rect.top
            self.vel_y = 0
            self.on_ground = True
    
    def _check_screen_bounds(self):
        """Comprueba que el jugador no salga de la pantalla"""
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.vel_x = 0
        
        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.vel_y = 0
            self.on_ground = True  # Consideramos el fondo de la pantalla como suelo
    
    def _update_animation(self):
        if self.is_dead:
            self.image = self.images['dead']
        elif self.is_hit:
            self.image = self.images['dead'] if not self.facing_right else self.images['dead']
        elif not self.on_ground:
            self.image = self.images['jump_left'] if not self.facing_right else self.images['jump']
        else:
            self.image = self.images['idle_left'] if not self.facing_right else self.images['idle']
    
    def take_damage(self):
        if not self.is_hit and not self.is_dead:
            self.health -= PLAYER_DAMAGE
            self.is_hit = True
            self.hit_timer = 30  # 0.5 segundos a 60 fps
            
            # Reproducir sonido de impacto
            if self.hit_sound:
                self.hit_sound.play()
            
            # Comprobar si el jugador ha muerto
            if self.health <= 0:
                self.health = 0
                self.is_dead = True
    
    def heal(self, amount=20):
        self.health = min(self.health + amount, PLAYER_MAX_HEALTH)
        
        # Reproducir sonido de energía
        if self.energy_sound:
            self.energy_sound.play()