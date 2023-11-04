import math
import numpy as np
import pygame as pg
from Body import Body
import random

DT = 1 # Delta time for the physics engine
UPDATES_PER_FRAME = 1 # Number of iterations of the physics engine for each frame

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
NUM_OF_PARTICLES = 15


def draw(bodies: [], screen: pg.Surface):
    # Draws the body as a square
    for i in bodies:
        pg.draw.circle(screen, (0, 0, 0), (i.pos[0], i.pos[1]), i.radius)


def main():
    print("interstellarIO")

    pg.init()
    window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pg.display.set_mode(window_size)

    pg.display.set_caption("Interstellar IO")

    screen = pg.display.set_mode(window_size)


    bodies = []
    for i in range(NUM_OF_PARTICLES):
        xPos = float(random.randint(0, WINDOW_WIDTH))
        yPos = float(random.randint(0, WINDOW_HEIGHT))
        xVel = random.random() * 2.0
        yVel = random.random() * 2.0
        mass = random.randint(100, 1000)
        bodies.append(Body(mass, np.array([xPos, yPos]), np.array([xVel, yVel])))

    clock = pg.time.Clock()

    running = True
    # pygame main loop
    while running:
        screen.fill((255, 255, 255))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
        for i in range(UPDATES_PER_FRAME):
            current = 0
            body_count = len(bodies)
            while current < body_count:
                merge_count = bodies[current].update(DT / UPDATES_PER_FRAME, bodies, current + 1)
                if merge_count < 0:
                    # Self was deleted
                    current -= 1
                    merge_count *= -1

                body_count -= merge_count

                current += 1


        draw(bodies, screen)
        pg.display.flip()
        clock.tick(60)
    
    pg.quit()

if __name__ == "__main__":
    main()