import pygame
import sys
from game import Game

def main():
    pygame.init()
    pygame.mixer.init()
    sonido_fondo = pygame.mixer.Sound("sounds/halo.mp3") 
    sonido_fondo.play()
    
    game = Game()
    
    game.run()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()