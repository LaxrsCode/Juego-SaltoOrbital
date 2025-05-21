from utils.constants import PLAYER_GRAVITY

class Gravity:
    def __init__(self, strength=PLAYER_GRAVITY):
        self.strength = strength
    
    def apply(self, entity):
        if not entity.on_ground:
            entity.vel_y += self.strength
        entity.vel_y = min(entity.vel_y, 10)

class LunarMovement:
    def __init__(self, entity, gravity_strength=PLAYER_GRAVITY, air_control=0.7):
        self.entity = entity
        self.gravity = Gravity(gravity_strength)
        self.air_control = air_control
    
    def update(self, dx=0):
        self.gravity.apply(self.entity)
        
        if self.entity.on_ground:
            self.entity.vel_x = dx * self.entity.speed
        else:
            # Control reducido en el aire
            # Permite cierto control al saltar pero no tanto como en el suelo
            self.entity.vel_x += dx * self.entity.speed * self.air_control
            
            # Limitar la velocidad horizontal en el aire
            max_air_speed = self.entity.speed * 1.2
            self.entity.vel_x = max(-max_air_speed, min(self.entity.vel_x, max_air_speed))
            
            if dx == 0:
                self.entity.vel_x *= 0.98
        
        # Actualizar posición
        self.entity.rect.x += int(self.entity.vel_x)
        self.entity.rect.y += int(self.entity.vel_y)
    
    def jump(self, power):
        if self.entity.on_ground:
            self.entity.vel_y = -power
            self.entity.on_ground = False
            return True
        return False