import math
import numpy as np
import pygame as pg
from Body import Body

BIG_G = 1 # Gravitational constant

pg.init()
window_size = (1200, 800)
screen = pg.display.set_mode(window_size)
pg.display.set_caption("Yo mama simulation")
screen = pg.display.set_mode(window_size)

def gravitational_force(first, second):
    distance_squared = sum(x**2 for x in (second.pos - first.pos))
    return BIG_G * first.mass * second.mass / distance_squared


def main():
    print("interstellarIO")

    bodies = []
    for i in range(5):
        bodies.append(Body(i, [i, i], [i, i])) # Random stuff

    running = True
    # pygame main loop
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            
        for i in bodies:
            net_force = np.array([0, 0])

            for j in bodies:
                # TODO do probably need to check if i == j otherwise there will be a division by zero
                # TODO optimize (like reuse the result of (i, j) for (j, i))
                force = gravitational_force(i, j)

                # TODO vectorize this scalar and add to net_force
                # TODO maybe reuse calculated second.pos - first.pos with gravitational_force

        pg.display.flip()
    
    pg.quit()
        
def draw(bodies, screen : pg.Surface):
    # Draws the body as a square
    size = 50
    for i in bodies:
        body_rect = pg.Surface((size, size))
        screen.blit(i, (i.pos[0] - size/2, i.pos[1] - size/2))
        

if __name__ == "__main__":
    main()
    