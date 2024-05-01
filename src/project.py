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
        
        if self.direction == 'left':
            self.pos[0] -= self.speed
        elif self.direction == 'right':
            self.pos[0] += self.speed
        elif self.direction == 'up':
            self.pos[1] -= self.speed
        elif self.direction == 'down':
            self.pos[1] += self.speed

        self.avoid_mouse(mouse_pos)

class Starfield:
    def __init__(self, screen_res):
        self.screen_res = screen_res
        self.particle_size = 2
        self.birth_rate = 5  
        self.comet_rate = 0.01  
        self.particles = []

    def update(self, dt, mouse_pos):
        self._birth_new_particles()
        self._update_particles(dt, mouse_pos)

    def _update_particles(self, dt, mouse_pos):
        for particle in self.particles[:]:
            particle.update(dt, mouse_pos)
            if particle.dead:
                self.particles.remove(particle)

    def _birth_new_particles(self):
        for count in range(self.birth_rate):
            x = random.randint(0, self.screen_res[0])
            y = random.randint(0, self.screen_res[1])
            pos = (x, y)
            life = random.randint(1000, 3000)
            color = random.choice([pygame.Color(255, 165, 0), pygame.Color(0, 255, 0)])  
            particle = Particle(pos, self.particle_size, life, color)
            self.particles.append(particle)
        
        if random.random() < self.comet_rate:
            x = self.screen_res[0]
            y = random.randint(0, self.screen_res[1])
            pos = (x, y)
            life = random.randint(2000, 4000)
            color = random.choice([pygame.Color(255, 165, 0), pygame.Color(0, 255, 0)])  
            comet = Comet(pos, size=8, life=life, color=color, speed=8)
            self.particles.append(comet)

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)

def main():
    pygame.init()
    pygame.display.set_caption("Starfield Screensaver")  
    clock = pygame.time.Clock()  
    dt = 0  
    resolution = (1920, 1080)  
    screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)  
    starfield = Starfield(resolution)  
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        mouse_pos = pygame.mouse.get_pos()
        starfield.update(dt, mouse_pos)
        black = pygame.Color(0, 0, 0)
        screen.fill(black)
        starfield.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60)



if __name__ == "__main__":
    main()