import math
import numpy as np
import pygame as pg

BIG_G = 1 # Gravitational constant

class Body:
    def __init__(self, mass, pos, vel):
        self.mass = mass
        self.mass = mass
        self.pos = pos
        self.vel = vel
        return

# Returns vector for gravitational pull of second Body acting on first Body
def gravitational_force(first, second):
    d_pos = second.pos - first.pos
    distance_squared = sum(x**2 for x in d_pos)
    scalar_force = BIG_G * first.mass * second.mass / distance_squared
    unit_vec = d_pos / np.linalg.norm(d_pos)
    return scalar_force * unit_vec


def main():
    print("interstellarIO")

    bodies = []
    for i in range(5):
        bodies.append(Body(i+1, np.array([float(i), float(i)]), np.array([float(i), float(i)]))) # Random stuff

    for i in bodies:
        net_force = np.array([0.0, 0.0])

        for j in bodies:
            if i == j:
                continue

            # TODO optimize (like reuse the result of (i, j) for (j, i))
            net_force += gravitational_force(i, j)

            # TODO maybe reuse calculated second.pos - first.pos with gravitational_force

        acceleration = net_force / i.mass
        i.vel += acceleration
        i.pos += i.vel


if __name__ == "__main__":
    main()