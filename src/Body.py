import numpy as np
BIG_G = 1 # Gravitational constant

class Body:

    def __init__(self, mass: float, pos: np.ndarray[np.float64], vel: np.ndarray[np.float64]) -> None:
        self.mass = mass
        self.pos = pos
        self.vel = vel
        return

    # Returns vector for gravitational pull of other Body acting on this Body
    def gravitational_force_from_other(self, other):
        d_pos = other.pos - self.pos
        distance_squared = sum(x**2 for x in d_pos)
        scalar_force = BIG_G * self.mass * other.mass / distance_squared
        unit_vec = d_pos / np.linalg.norm(d_pos)
        return scalar_force * unit_vec

    def net_gravitational_force(self, bodies):
        net_force = 0.0
        for j in bodies:
            if self == j:
                continue

            # TODO optimize (like reuse the result of (i, j) for (j, i))
            # TODO maybe reuse calculated second.pos - first.pos with gravitational_force
            net_force += self.gravitational_force_from_other(j)

        return net_force

    def update(self, dt, bodies):
        acceleration = self.net_gravitational_force(bodies) / self.mass
        self.vel += acceleration * dt
        self.pos += self.vel * dt