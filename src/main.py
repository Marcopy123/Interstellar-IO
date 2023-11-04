import math
import numpy as np
import pygame as pg
from Body import Body
import random
from Camera import Camera

DT = 0.5 # Delta time for the physics engine
UPDATES_PER_FRAME = 1 # Number of iterations of the physics engine for each frame

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
NUM_OF_PARTICLES = 15

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

    # sun = Body(2000, np.array([WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2]), np.array([0.0, 0.0]))
    # earth = Body(500, np.array([WINDOW_WIDTH / 3, WINDOW_HEIGHT / 2]), np.array([0.0, 8.5]))
    # earth2 = Body(1000, np.array([WINDOW_WIDTH / 4, WINDOW_HEIGHT / 2]), np.array([0.0, 4.0]))

    # bodies.append(sun)
    # bodies.append(earth)
    # bodies.append(earth2)
    clock = pg.time.Clock()
    camera = Camera(bodies[0], screen)

    running = True
    # pygame main loop
    while running:
        screen.fill((255, 255, 255))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                
            if event.type == pg.MOUSEWHEEL:
                sensitivity = 0.1
                if camera.zoom + event.y * sensitivity > 0.5 and camera.zoom + event.y * sensitivity < 10: 
                    camera.zoom += event.y * sensitivity
        
        for i in range(UPDATES_PER_FRAME):
            for j in bodies:
                 current = 0
            body_count = len(bodies)
            while current < body_count:
                merge_count = bodies[current].update(DT / UPDATES_PER_FRAME, bodies, current + 1)
                if len(merge_count) > 1:
                    # Self was deleted
                    if current == 0:
                        camera.obj = bodies[merge_count[1]]
                    # Self was deleted
                    current -= 1

                body_count -= merge_count[0]

                current += 1

        camera.update()
        camera.draw(bodies)
        pg.display.flip()
        clock.tick(60)
    
    pg.quit()

if __name__ == "__main__":
    main()