import math
import numpy as np
import pygame as pg
from Body import Body
import random

DT = 1 # Delta time

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
NUM_OF_PARTICLES = 20


def draw(bodies: [], screen: pg.Surface):
    # Draws the body as a square
    # TODO change to circle
    for i in bodies:
        size = i.radius
        body_rect = pg.Surface((size, size))
        screen.blit(body_rect, (i.pos[0] - size/2, i.pos[1] - size/2))


def main():
    print("interstellarIO")

    pg.init()
    window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pg.display.set_mode(window_size)

    pg.display.set_caption("Interstellar IO")

    screen = pg.display.set_mode(window_size)


    bodies = []
    #for i in range(NUM_OF_PARTICLES):
        #xPos = float(random.randint(0, WINDOW_WIDTH))
        #yPos = float(random.randint(0, WINDOW_HEIGHT))
        #xVel = float(random.randint(0, 3))
        #yVel = float(random.randint(0, 3))
        #bodies.append(Body(float(i + 1), np.array([xPos, yPos]), np.array([xVel, yVel])))

    sun = Body(2000, np.array([WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2]), np.array([0.0, 0.0]))
    earth = Body(50, np.array([WINDOW_WIDTH / 3, WINDOW_HEIGHT / 2]), np.array([0.0, 4.0]))
    bodies.append(sun)
    bodies.append(earth)

    clock = pg.time.Clock()

    running = True
    # pygame main loop
    while running:
        screen.fill((255, 255, 255))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            
        for i in bodies:
            i.update(DT, bodies)
        draw(bodies, screen)
        pg.display.flip()
        clock.tick(60)
    
    pg.quit()

if __name__ == "__main__":
    main()