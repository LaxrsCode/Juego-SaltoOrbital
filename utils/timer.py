import pygame

class Timer:
    def __init__(self, duration):
        self.duration = duration  # Duración total en segundos
        self.time_left = duration  # Tiempo restante en segundos
        self.start_time = None
        self.running = False
        self.finished = False
    
    def start(self):
        self.start_time = pygame.time.get_ticks()
        self.running = True
        self.finished = False
    
    def pause(self):
        if self.running:
            self.time_left = self.get_time_left()
            self.running = False
    
    def resume(self):
        if not self.running and not self.finished:
            self.start_time = pygame.time.get_ticks()
            self.running = True
    
    def reset(self):
        self.time_left = self.duration
        self.running = False
        self.finished = False
    
    def update(self):
        if self.running and not self.finished:
            if self.get_time_left() <= 0:
                self.finished = True
                self.running = False
                self.time_left = 0
                return True
        return False
    
    def get_time_left(self):
        if not self.running:
            return self.time_left
        
        elapsed = (pygame.time.get_ticks() - self.start_time) / 1000  # Convertir a segundos
        remaining = self.time_left - elapsed
        
        # Asegurarse de que no sea negativo
        return max(0, remaining)
    
    def get_time_formatted(self):
        time_left = self.get_time_left()
        minutes = int(time_left // 60)
        seconds = int(time_left % 60)
        
        return f"{minutes:02d}:{seconds:02d}"
    
    def get_progress(self):
        return 1.0 - (self.get_time_left() / self.duration)