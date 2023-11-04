import math
import numpy as np
import pygame as pg
from Body import Body
import random
import Camera as Camera

DT = 1 # Delta time for the physics engine
UPDATES_PER_FRAME = 2 # Number of iterations of the physics engine for each frame

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
NUM_OF_PARTICLES = 20
MAP_WIDTH = 3000
MAP_HEIGHT = 3000

map_surface = pg.Surface((MAP_WIDTH, MAP_HEIGHT))
Camera = Camera(WINDOW_WIDTH, WINDOW_HEIGHT)



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
        xVel = float(random.randint(0, 3))
        yVel = float(random.randint(0, 3))
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
            for j in bodies:
                j.update(DT / UPDATES_PER_FRAME, bodies)

        pg.display.flip()
        clock.tick(60)
    
    pg.quit()

if __name__ == "__main__":
    main()