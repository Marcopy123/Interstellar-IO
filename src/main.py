import math
import numpy as np
import pygame as pg

BIG_G = 1 # Gravitational constant

class Body:
    def __init__(self, mass, pos, vel):
        self.mass = mass
        self.pos = pos
        self.vel = vel
        return


def gravitational_force(first, second):
    # print("First: " + first.vel)
    distance_squared = sum(x**2 for x in (second.pos - first.pos))
    return BIG_G * first.mass * second.mass / distance_squared


def main():
    print("interstellarIO")

    bodies = []
    for i in range(5):
        bodies.append(Body(i, np.array([i, i]), np.array([i, i]))) # Random stuff

    for i in bodies:
        net_force = np.array([0, 0])

        for j in bodies:
            # TODO do probably need to check if i == j otherwise there will be a division by zero
            # TODO optimize (like reuse the result of (i, j) for (j, i))
            force = gravitational_force(i, j)

            # TODO vectorize this scalar and add to net_force
            # TODO maybe reuse calculated second.pos - first.pos with gravitational_force


if __name__ == "__main__":
    main()