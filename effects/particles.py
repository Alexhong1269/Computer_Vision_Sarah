import random
import cv2
import math
import colorsys
import numpy as np

def _heart_shape_points(scale=1.0, num_points=20):
    points = []
    for i in range(num_points):
        t = (2 * math.pi / num_points) * i
        hx = 16 * (math.sin(t) ** 3)
        hy = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        points.append((hx * scale, -hy * scale))
    #return
    return points

class HeartParticles:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        self.velocity_x = speed * math.cos(angle)
        self.velocity_y = speed * math.sin(angle) - 2

        self.gravity = 0.05
        self.scale = random.uniform(.4, .9)
        self.lifespan = random.randint(30, 50)
    
    def update(self):
        self.velocity_y += self.gravity
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.lifespan -= 1
    
    def is_alive(self):
        return self.lifespan > 0

    def draw(self, frame):
        offsets = _heart_shape_points(scale=self.scale)
        polygon = np.array(
            [[int(self.x + dx), int(self.y + dy)] for dx, dy in offsets],
            dtype=np.int32
        )
        cv2.fillPoly(frame, [polygon], self.color)

class Particle:
    def __init__(self, x, y, color):
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
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.lifespan -= 1
    
    def is_alive(self):
        return self.lifespan > 0
    
    def draw(self, frame):
        cv2.circle(frame, (int(self.x), int(self.y)), self.radius, self.color, -1)

class ParticleSystem:
    def __init__(self):
        #holding every current live particle
        self.particles = []
        #all live lasers
        self.lasers = []
    
    #spawing partilces when the gesture is called
    def emit(self, x, y, color, count=30):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))
    
    #advancing the particle
    def update(self):
        for particle in self.particles:
            particle.update()
        self.particles = [p for p in self.particles if p.is_alive()]

        for laser in self.lasers:
            laser.update()
        self.lasers = [l for l in self.lasers if l.is_alive()]
    
    #drawing all the particles
    def draw(self, frame):
        for particle in self.particles:
            particle.draw(frame)
        for laser in self.lasers:
            laser.draw(frame)
    
    #laser effect
    def emit_laser_burst(self, x, y, count=16):
        for i in range(count):
            angle = (2 * math.pi / count) * i
            hue = i / count
            r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
            color = (int(b * 255), int(g * 255), int(r * 255))
            self.lasers.append(Laser(x, y, angle, color))

class Laser:
    def __init__(self, x, y, angle, color, length=40, speed=25):
        self.x = x
        self.y = y
        self.angle = angle
        self.color = color
        self.length = length
        self.speed = speed
        self.lifespan = 15
    
    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.lifespan -= 1
    
    def is_alive(self):
        return self.lifespan > 0
    
    def draw(self, frame):
        end_x = self.x + math.cos(self.angle) * self.length
        end_y = self.y + math.sin(self.angle) * self.length
        cv2.line(
            frame,
            (int(self.x), int(self.y)),
            (int(end_x), int(end_y)),
            self.color, 3
        )
        