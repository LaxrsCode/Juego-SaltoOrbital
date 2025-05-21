import pygame
import random
from states.base_state import BaseState
from utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, RED, GREEN, YELLOW, 
    SPACE_BLUE, LEVEL_EASY_TIME, LEVEL_MEDIUM_TIME, LEVEL_HARD_TIME,
    LEVEL_EASY_GEARS, LEVEL_MEDIUM_GEARS, LEVEL_HARD_GEARS
)
from utils.timer import Timer
from utils.asset_loader import load_image, load_sound
from entities.player import Player
from entities.platform import Platform
from entities.obstacle import Asteroid
from entities.collectible import Energy, Gear
from physic.collision import check_collision
from utils.constants import FONT_PATH

class GameState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        
        self.player = None
        
        self.timer = None
        
        self.current_level = 1
        
        self.gears_collected = 0
        self.gears_required = LEVEL_EASY_GEARS
        
        self.victory_sound = None
        self.defeat_sound = None
        
        self.show_instructions = False
        self.instruction_timer = 0
        
        self.background = None
        
        self.paused = False
    
    def init(self):
        self.all_sprites.empty()
        self.platforms.empty()
        self.obstacles.empty()
        self.collectibles.empty()
        
        self.current_level = self.game.selected_level
        
        self._setup_level(self.current_level)
        
        self.show_instructions = (self.current_level == 1)
        self.instruction_timer = 300 
        
        self.timer.start()
        
        self.victory_sound = load_sound("winner.mp3")
        self.defeat_sound = load_sound("game-over.mp3")
    
    def _setup_level(self, level):
        if level == 1:
            self.timer = Timer(LEVEL_EASY_TIME)
            self.gears_required = LEVEL_EASY_GEARS
            self.asteroid_directions = ["down"]
            try:
                self.background = load_image("Fondo.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
            except:
                self.background = None
        elif level == 2:
            self.timer = Timer(LEVEL_MEDIUM_TIME)
            self.gears_required = LEVEL_MEDIUM_GEARS
            self.asteroid_directions = ["down", "diagonal_right"]
            try:
                self.background = load_image("Fondo.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
            except:
                self.background = None
        else:  # level 3
            self.timer = Timer(LEVEL_HARD_TIME)
            self.gears_required = LEVEL_HARD_GEARS
            self.asteroid_directions = ["down", "diagonal_right", "diagonal_left"]
            try:
                self.background = load_image("Fondo.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
            except:
                self.background = None
        
        self.gears_collected = 0
        
        self._create_platforms()
        
        # Crear jugador en la primera plataforma
        first_platform = list(self.platforms)[0]
        player_x = first_platform.rect.centerx
        player_y = first_platform.rect.top - 40
        self.player = Player(player_x, player_y)
        self.all_sprites.add(self.player)
    
    def _create_platforms(self):
        # Crear 4 plataformas
        platform_width = SCREEN_WIDTH // 4  
        platform_positions = [
            # 1. Plataforma central abajo
            (SCREEN_WIDTH // 2 - platform_width // 2, SCREEN_HEIGHT - 100),
            # 2. Plataforma derecha
            (SCREEN_WIDTH - platform_width - 20, SCREEN_HEIGHT - 180),
            # 3. Plataforma izquierda
            (20, SCREEN_HEIGHT - 180),
            # 4. Plataforma central arriba (por encima de las laterales)
            (SCREEN_WIDTH // 2 - platform_width // 2, SCREEN_HEIGHT - 300)
        ]
        
        for pos in platform_positions:
            platform = Platform(pos[0], pos[1], platform_width)
            print(f"Plataforma: posición=({pos[0]}, {pos[1]}), tamaño={platform.rect.width}x{platform.rect.height}")
            self.platforms.add(platform)
            self.all_sprites.add(platform)
    
    def _spawn_asteroid(self):
        direction = random.choice(self.asteroid_directions)
        
        if direction == "down":
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = -50
            dx = 0
            dy = random.uniform(2, 4)
        elif direction == "diagonal_right":
            x = -50
            y = random.randint(50, SCREEN_HEIGHT // 2)
            dx = random.uniform(2, 4)
            dy = random.uniform(1, 3)
        else:  # diagonal_left
            x = SCREEN_WIDTH + 50
            y = random.randint(50, SCREEN_HEIGHT // 2)
            dx = -random.uniform(2, 4)
            dy = random.uniform(1, 3)
        
        # Ajustar velocidad según nivel
        speed_factor = 1.0 + (self.current_level - 1) * 0.3
        dx *= speed_factor
        dy *= speed_factor
        
        # Crear asteroide
        asteroid = Asteroid(x, y, dx, dy)
        self.obstacles.add(asteroid)
        self.all_sprites.add(asteroid)
    
    def _spawn_energy(self):
        if not self.platforms:
            return
        
        platform = random.choice(list(self.platforms))
        
        # Crear punto de energía en la plataforma
        x = random.randint(
            platform.rect.left + 20, 
            platform.rect.right - 20
        )
        y = platform.rect.top - 15
        
        energy = Energy(x, y)
        self.collectibles.add(energy)
        self.all_sprites.add(energy)
    
    def _spawn_gear(self):
        if not self.platforms or len(list(self.platforms)) < 2:
            return
        
        platforms = random.sample(list(self.platforms), 2)
        
        # Calcular una posición entre las dos plataformas
        x1, y1 = platforms[0].rect.center
        x2, y2 = platforms[1].rect.center
        
        # Añadir algo de variación a la posición
        t = random.random()
        x = int(x1 + t * (x2 - x1) + random.randint(-50, 50))
        y = int(y1 + t * (y2 - y1) + random.randint(-30, 30))
        
        # Mantener dentro de los límites de la pantalla
        x = max(30, min(x, SCREEN_WIDTH - 30))
        y = max(50, min(y, SCREEN_HEIGHT - 80))
        
        gear = Gear(x, y)
        self.collectibles.add(gear)
        self.all_sprites.add(gear)
    
    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Pausar/reanudar el juego
                    self.paused = not self.paused
                    if self.paused:
                        self.timer.pause()
                    else:
                        self.timer.resume()
                elif event.key == pygame.K_BACKSPACE:
                    self.game.change_state('menu')
        
        if self.paused:
            return
        
        if self.timer.update():
            self._check_level_completion()
        
        self.player.update(self.platforms)
        
        self.obstacles.update()
        self.collectibles.update()
        
        hits = pygame.sprite.spritecollide(self.player, self.obstacles, True)
        for hit in hits:
            self.player.take_damage()
            if self.player.health <= 0:
                self._game_over(False)  # False = derrota
        
        hits = pygame.sprite.spritecollide(self.player, self.collectibles, True)
        for hit in hits:
            if isinstance(hit, Energy):
                self.player.heal()
            elif isinstance(hit, Gear):
                self.gears_collected += 1
                gear_sound = load_sound("energia.mp3")
                if gear_sound:
                    gear_sound.play()
        
        if random.random() < 0.02:  # 2% de probabilidad por frame
            self._spawn_asteroid()
        
        if random.random() < 0.01:  # 1% de probabilidad por frame
            self._spawn_energy()
        
        # Generar engranajes si no hay suficientes en el nivel
        gears_on_screen = len([c for c in self.collectibles if isinstance(c, Gear)])
        if gears_on_screen < 2 and self.gears_collected < self.gears_required:
            if random.random() < 0.01:  # 1% de probabilidad por frame
                self._spawn_gear()
        
        if self.show_instructions:
            self.instruction_timer -= 1
            if self.instruction_timer <= 0:
                self.show_instructions = False
    
    def _check_level_completion(self):
        if self.gears_collected >= self.gears_required and self.player.health > 10:
            self._game_over(True)  # True = victoria
        else:
            self._game_over(False)  # False = derrota
    
    def _game_over(self, victory):
        self.game.victory = victory
        
        if victory and self.victory_sound:
            self.victory_sound.play()
        elif not victory and self.defeat_sound:
            self.defeat_sound.play()
        
        self.game.change_state('game_over')
    
    def draw(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(SPACE_BLUE)
        
        self.all_sprites.draw(screen)
        
        self._draw_hud(screen)
        
        if self.show_instructions:
            self._draw_instructions(screen)
        
        if self.paused:
            self._draw_pause_screen(screen)
    
    def _draw_hud(self, screen):
        pygame.draw.rect(screen, BLACK, (10, 10, 204, 24))
        pygame.draw.rect(screen, RED, (12, 12, 200 * (self.player.health / 100), 20))
        health_text = self.small_font.render(f"Vida: {self.player.health}", True, WHITE)
        screen.blit(health_text, (220, 12))
        
        gear_text = self.small_font.render(f"Engranajes: {self.gears_collected}/{self.gears_required}", True, WHITE)
        screen.blit(gear_text, (10, 40))
        
        time_text = self.small_font.render(f"Tiempo: {self.timer.get_time_formatted()}", True, WHITE)
        screen.blit(time_text, (SCREEN_WIDTH - time_text.get_width() - 10, 10))
        
        level_text = self.small_font.render(f"Nivel {self.current_level}", True, WHITE)
        screen.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 10, 40))
    
    def _draw_instructions(self, screen):
        instructions = [
            "Controles:",
            "Flechas < > para moverse",
            "Barra espaciadora para saltar",
            "ESC para pausar",
            "Backspace para volver al menú"
        ]
        
        instruction_surface = pygame.Surface((300, 150))
        instruction_surface.set_alpha(200)
        instruction_surface.fill(BLACK)
        
        screen.blit(instruction_surface, (SCREEN_WIDTH - 310, SCREEN_HEIGHT - 160))
        
        y_offset = SCREEN_HEIGHT - 150
        for line in instructions:
            text = self.small_font.render(line, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH - 300, y_offset))
            y_offset += 25
    
    def _draw_pause_screen(self, screen):
        pause_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        pause_surface.set_alpha(150)
        pause_surface.fill(BLACK)

        screen.blit(pause_surface, (0, 0))
        pause_text = self.font.render("PAUSA", True, WHITE)
        screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        
        instructions = "Presiona ESC para continuar o Backspace para volver al menú"
        inst_text = self.small_font.render(instructions, True, WHITE)
        screen.blit(inst_text, (SCREEN_WIDTH // 2 - inst_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
    
    def reset(self):
        """Resetea el estado del juego"""
        if self.timer:
            self.timer.pause()