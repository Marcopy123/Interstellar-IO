import numpy as np
import math

BIG_G = 3 # Gravitational constant
DENSITY = 0.25 # Units of mass per unit of area

class Body:

    def __init__(self, mass, pos, vel):
        self.mass = mass
        self.pos = pos
        self.vel = vel
        self.radius = math.sqrt(mass / DENSITY)
        return

    # Returns vector for gravitational pull of other Body acting on this Body. Returns an empty array with a single -1.0 if the bodies collide
    def gravitational_force_from_other(self, other):
        # TODO check if they collide
        d_pos = other.pos - self.pos
        distance_squared = sum(x**2 for x in d_pos)
        if distance_squared < (self.radius + other.radius)**2:
            return np.array([0.0])
        scalar_force = BIG_G * self.mass * other.mass / distance_squared
        unit_vec = d_pos / np.linalg.norm(d_pos)
        return scalar_force * unit_vec

    def net_gravitational_force(self, bodies: []):
        net_force = 0.0
        for j in bodies:
            if self == j:
                continue

            # TODO optimize (like reuse the result of (i, j) for (j, i))
            # TODO maybe reuse calculated second.pos - first.pos with gravitational_force
            force = self.gravitational_force_from_other(j)
            if force.size == 1:
                # Merge
                biggest = max(self, j, key=lambda x: x.radius)
                smallest = j if biggest == self else self

                # TODO update velocity (collision)
                biggest.mass += smallest.mass
                biggest.radius = math.sqrt(biggest.mass / DENSITY)
                bodies.remove(smallest)

                continue
            
            net_force += force

        return net_force

    def update(self, dt: float, bodies: []):
        acceleration = self.net_gravitational_force(bodies) / self.mass
        self.vel += acceleration * dt
        self.pos += self.vel * dt