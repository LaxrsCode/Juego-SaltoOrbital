import pygame
import os
from utils.constants import IMAGES_PATH, SOUNDS_PATH

images = {}
sounds = {}

def load_image(name, scale=None, flip_x=False):
    cache_key = f"{name}_{scale}_{flip_x}"
    
    if cache_key in images:
        return images[cache_key]
    
    # Cargar la imagen
    try:
        fullname = os.path.join(IMAGES_PATH, name)
        image = pygame.image.load(fullname).convert_alpha()
        
        # Escalar si es necesario
        if scale:
            image = pygame.transform.scale(image, scale)
        
        # Voltear si es necesario
        if flip_x:
            image = pygame.transform.flip(image, True, False)
        
        # Almacenar en caché
        images[cache_key] = image
        return image
    except pygame.error as e:
        print(f"Error al cargar la imagen {name}: {e}")
        # Devolver una superficie de error (cuadrado rojo)
        error_surface = pygame.Surface((50, 50))
        error_surface.fill((255, 0, 0))
        return error_surface

def load_sound(name):
    # Verificar si ya está en caché
    if name in sounds:
        return sounds[name]
    
    # Cargar el sonido
    try:
        fullname = os.path.join(SOUNDS_PATH, name)
        sound = pygame.mixer.Sound(fullname)
        
        # Almacenar en caché
        sounds[name] = sound
        return sound
    except pygame.error as e:
        print(f"Error al cargar el sonido {name}: {e}")
        return None

def preload_assets():
    images_to_load = [
        "Jugador.png",
        "Jugador_saltando.png",
        "Jugador_caminando.png",
        "Jugador_caido.png",
        "Jugador_vida.png",#Sprite para el jugador cuando pase por un punto de vida
        "Plataforma-1.png",
        "Asteroide.png",
        "Punto_vida.png",
        "Escombros.png",
        "Fondo.png",
    ]
    
    sounds_to_load = [
        "energia.mp3", # tambien para cuando recoge un engranaje
        "golpe.mp3",
        "salto.mp3",
        "winner.mp3",
        "game_over.mp3",
    ]
    
    # Precargar imágenes
    for img in images_to_load:
        try:
            load_image(img)
            # También precargar la versión volteada para el movimiento del robot
            if img.startswith("robot_"):
                load_image(img, flip_x=True)
        except Exception as e:
            print(f"No se pudo precargar la imagen {img}: {e}")
    
    # Precargar sonidos
    for snd in sounds_to_load:
        try:
            load_sound(snd)
        except Exception as e:
            print(f"No se pudo precargar el sonido {snd}: {e}")