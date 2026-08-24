import random
import cv2

class Particle:
    def __init__(self, x, y):
        #x and y are the current particles on the screen
        self.x = x
        self.y = y
        #randomize the particle color
        self.color = color

        angle = random.uniform(0, 2 *3.14159)
        speed = random.uniform(3,8)
        #particle movement
        self.velocity_x = speed * random.uniform(-1, 1)
        self.velocity_y = speed * random.uniform(-3, -1)

        #gravity for each particle
        self.gravity = 0.3
        self.radius = random.randint(3, 6)
        #how many frames the particle last
        self.lifespan = random.randint(20, 40)

    #updating and applying the gravity to the particle
    def update(self):
        self.velocity_y += self.gravity
        self.velocity_x += self.velocity_x
        self.velocity_y += self.velocity_y
        self.lifespan -= 1
    
    def is_alive(self):
        return self.lifespan > 0
    
    def draw(self, frame):
        cv2.circle(frame, (int(self.x), int(self.y)), self.radius, self.color, -1)

class ParticleSystem:
    def __init__(self):
        #holding every current live particle
        self.particles = []
    
    #spawing partilces when the gesture is called
    def emit(self, x, y, color, count=30):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))
    
    #advancing the particle
    def update(self):
        for particle in self.particles:
            particle.update()
        self.particles = [p for p in self.partilces if p.is_alive()]
    
    #drawing all the particles
    def draw(self, frame):
        for particle in self.partilces:
            particle.draw(frame)