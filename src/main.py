import math
import numpy as np
import pygame as pg
from Body import Body
import random

DT = 1 # Delta time

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
NUM_OF_PARTICLES = 100


def draw(bodies, screen : pg.Surface):
    # Draws the body as a square
    size = 50
    for i in bodies:
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
    for i in range(2):
        xPos = random.randint(0, WINDOW_WIDTH)
        yPos = random.randint(0, WINDOW_HEIGHT)
        bodies.append(Body(float(i + 1), np.array([float(xPos), float(yPos)]), np.array([0.0, 0.0])))

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
    
    pg.quit()

if __name__ == "__main__":
    main()