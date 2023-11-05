import numpy as np
import math
import random
import pygame as pg

G = 1 # Gravitational constant
DENSITY = 15 # Units of mass per unit of area
DESPAWN_RADIUS = 350

class Body:
    def __init__(self, mass: float, pos: np.ndarray[np.float64], vel: np.ndarray[np.float64], uid: int) -> None:
        self.mass = mass
        self.pos = pos
        self.vel = vel
        self.uid = uid
        self.radius = math.sqrt(mass / DENSITY)
        self.target_radius = self.radius
        self.net_force = np.array([0.0, 0.0])
        
        self.trail = []
        self.max_trail = 30
        self.trail_density = 0.25
        self.id = 0
        
        self.state = ""
        self.image = None
        self.update_form()
        
        
    # Returns vector for gravitational pull of other Body acting on this Body
    def gravitational_force_from_other(self, other, alt_rendering: bool):
        d_pos = other.pos - self.pos
        distance_squared = sum(x**2 for x in d_pos)
        if distance_squared < (self.radius + other.radius)**2:
            return np.array([0.0])
        if alt_rendering:
            scalar_force = G * self.mass * other.mass / math.sqrt(distance_squared)
        else:
            scalar_force = G * self.mass * other.mass / distance_squared
        d_pos_magnitude = np.linalg.norm(d_pos)
        unit_vec = d_pos / d_pos_magnitude
        return [scalar_force * unit_vec, d_pos_magnitude]

    # Calculates net force on body and updates kinematic quantities
    # Returns an integer n:
    # If n is 0, no merges were done (no bodies)
    # Otherwise, the size of n is the number of merges that were made, i.e. the number of bodies deleted
    # Additionally, if n is negative, the self object has been merged AND deleted
    def update(self, dt: float, bodies: [], start: int, check_despawn: bool, spawn_radius: float, alt_rendering: bool):
            
        if self.id % (1 / self.trail_density) == 0:
            if len(self.trail) < self.max_trail:
                self.trail.append([self.pos[0], self.pos[1], np.linalg.norm(self.vel)])
            else:
                self.trail = self.trail[1:]
                self.trail.append([self.pos[0], self.pos[1], np.linalg.norm(self.vel)])

                
        self.id += 1
        
        merges = []
        current = start
        body_count = len(bodies)

        if self.target_radius > self.radius:
            self.radius += 0.2

        while current < body_count:
            # TODO maybe reuse calculated second.pos - first.pos with gravitational_force
            other = bodies[current]
            result = self.gravitational_force_from_other(other, alt_rendering)
            if check_despawn and len(result) > 1:
                if result[1] > DESPAWN_RADIUS + spawn_radius:
                    merges.append([current, -2])
                    bodies.pop(current)
                    body_count -= 1
                    continue
            force = result[0]
            if force.size == 1:
                # Merge
                big = max(self, other, key=lambda x: x.radius)
                small = self if big == other else other

                # Conservation of momentum
                # TODO instead of changing vel, change net_force?? maybe
                big.vel = ((big.mass * big.vel) + (small.mass * small.vel)) / (big.mass + small.mass)
                big.mass += small.mass
                big.target_radius = int(5 * math.sqrt(big.mass / DENSITY)) / 5
                bodies.remove(small)
                big.update_form()

                merges.append([small.uid, big.uid])
                
                if small == self:
                    return merges
                
                body_count -= 1
                continue
            
            self.net_force += force
            # The force from i to j is the opposite of that of j to i, which is why we have a start variable
            other.net_force -= force
            current += 1
        acceleration = self.net_force / self.mass
        self.vel += acceleration * dt
        self.pos += self.vel * dt

        self.net_force = np.array([0.0, 0.0])
        return merges
    
    def update_form(self):
        old_state = self.state
        
        self.state = "Asteroids"
        if(self.mass > 10 ** 3 and self.mass <= 10 ** 4):
            self.state = "Protoplanets"
        elif(self.mass > 10 ** 4 and self.mass <= 10 ** 5):
            self.state = "JovianPlanets"
        elif(self.mass > 10 ** 5 and self.mass <= 10 ** 6):
            self.state = "BrownDwarfs"
        elif(self.mass > 10 ** 6 and self.mass <= 10 ** 7):
            self.state = "YellowDwarfs"
        elif(self.mass > 10 ** 7 and self.mass <= 10 ** 8):
            self.state = "RedGiant"
        elif(self.mass > 10 ** 8 and self.mass <= 10 ** 9):
            self.state = "SuperGiant"
        elif(self.mass > 10 ** 9 and self.mass <= 10 ** 10):
            self.state = "BlackHoles"
        
        # choose a random image to assign if there is a phase change
        if self.state != old_state:
            idx = random.randint(1,4)
            self.image = pg.image.load(f"Images/{self.state}/{idx}.png")
        
    def add_force(self, direction : np.ndarray, force):
        self.net_force = direction * force / self.mass