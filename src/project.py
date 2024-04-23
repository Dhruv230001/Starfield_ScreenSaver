import random
import pygame
import math

# Define Particle class
class Particle:
    def __init__(self, pos=(0, 0), size=2, life=1000, color=None):
        self.pos = list(pos)  
        self.size = size
        if color is None:
            self.color = pygame.Color(255, 255, 255)
        else:
            self.color = color
        self.age = 1  
        self.life = life 
        self.dead = False
        self.alpha = 255
        self.surface = self.update_surface()

    def update(self, dt, mouse_pos):
        self.age += dt
        if self.age > self.life:
            self.dead = True
        self.alpha = 255 * (1 - (self.age / self.life))
        self.avoid_mouse(mouse_pos)

    def avoid_mouse(self, mouse_pos):
        distance = math.sqrt((self.pos[0] - mouse_pos[0]) ** 2 + (self.pos[1] - mouse_pos[1]) ** 2)

        if distance < 100:  
            direction = [self.pos[0] - mouse_pos[0], self.pos[1] - mouse_pos[1]]
            length = math.sqrt(direction[0] ** 2 + direction[1] ** 2)

            direction = [d / length for d in direction]

            self.pos[0] += direction[0] * 10
            self.pos[1] += direction[1] * 10

    def update_surface(self):
        surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(surface, self.color, (self.size // 2, self.size // 2), self.size // 2)
        return surface
    
    def draw(self, surface):
        if self.dead:
            return
        self.surface.set_alpha(self.alpha)
        surface.blit(self.surface, self.pos)

class Comet(Particle):
    def __init__(self, pos=(0, 0), size=5, life=2000, color=None, speed=5):
        super().__init__(pos, size, life, color)
        self.speed = speed
        self.surface = self.update_surface()
        self.direction = random.choice(['left', 'right', 'up', 'down'])
        self.radius = random.randint(50, 200) 
        self.angle = random.uniform(0, 2 * math.pi)  

    def update(self, dt, mouse_pos):
        self.age += dt
        if self.age > self.life:
            self.dead = True
        self.alpha = 255 * (1 - (self.age / self.life))

        if self.direction == 'curve':
            self.pos[0] = self.radius * math.cos(self.angle)
            self.pos[1] = self.radius * math.sin(self.angle)
            self.angle += self.speed / self.radius  
        
        if self.direction == 'left':
            self.pos[0] -= self.speed
        elif self.direction == 'right':
            self.pos[0] += self.speed
        elif self.direction == 'up':
            self.pos[1] -= self.speed
        elif self.direction == 'down':
            self.pos[1] += self.speed

        self.avoid_mouse(mouse_pos)


if __name__ == "__main__":
    main()