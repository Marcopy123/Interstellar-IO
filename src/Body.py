import numpy as np
import math

BIG_G = 1 # Gravitational constant
DENSITY = 25 # Units of mass per unit of area

class Body:
    def __init__(self, mass: float, pos: np.ndarray[np.float64], vel: np.ndarray[np.float64], uid: int) -> None:
        self.mass = mass
        self.pos = pos
        self.vel = vel
        self.uid = uid
        self.radius = math.sqrt(mass / DENSITY)
        self.net_force = np.array([0.0, 0.0])

    # Returns vector for gravitational pull of other Body acting on this Body
    def gravitational_force_from_other(self, other):
        d_pos = other.pos - self.pos
        distance_squared = sum(x**2 for x in d_pos)
        if distance_squared < (self.radius + other.radius)**2 / 2:
            return np.array([0.0])
        scalar_force = BIG_G * self.mass * other.mass / distance_squared
        unit_vec = d_pos / np.linalg.norm(d_pos)
        return scalar_force * unit_vec

    # Calculates net force on body and updates kinematic quantities
    # Returns an integer n:
    # If n is 0, no merges were done (no bodies)
    # Otherwise, the size of n is the number of merges that were made, i.e. the number of bodies deleted
    # Additionally, if n is negative, the self object has been merged AND deleted
    def update(self, dt: float, bodies: [], start: int):
        merges = []
        current = start
        body_count = len(bodies)
        while current < body_count:
            # TODO maybe reuse calculated second.pos - first.pos with gravitational_force
            other = bodies[current]
            force = self.gravitational_force_from_other(other)
            if force.size == 1:
                # Merge
                big = max(self, other, key=lambda x: x.radius)
                small = self if big == other else other

                # Conservation of momentum
                # TODO instead of changing vel, change net_force?? maybe
                big.vel = ((big.mass * big.vel) + (small.mass * small.vel)) / (big.mass + small.mass)
                big.mass += small.mass
                big.radius = math.sqrt(big.mass / DENSITY)
                bodies.remove(small)

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