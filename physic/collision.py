import pygame

def check_collision(sprite1, sprite2):

    return pygame.sprite.collide_rect(sprite1, sprite2)

def check_platform_collision(entity, platforms):
    if entity.vel_y > 0:
        platform_hits = pygame.sprite.spritecollide(entity, platforms, False)
        
        for platform in platform_hits:
            if entity.rect.bottom >= platform.rect.top and entity.rect.bottom <= platform.rect.top + 10:
                return platform
    
    return None

def check_obstacle_collision(entity, obstacles):
    
    return pygame.sprite.spritecollide(entity, obstacles, False)

def check_collectible_collision(entity, collectibles):
    
    return pygame.sprite.spritecollide(entity, collectibles, False)

def is_on_screen(rect, padding=50):
    screen_rect = pygame.display.get_surface().get_rect()
    extended_rect = screen_rect.inflate(padding * 2, padding * 2)
    return extended_rect.colliderect(rect)