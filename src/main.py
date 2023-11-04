import math 
import numpy as np
import pygame as pg
from Body import Body
import random
from Camera import Camera
from Spawner import Spawner

DT = 0.2 # Delta time for the physics engine
UPDATES_PER_FRAME = 1 # Number of iterations of the physics engine for each frame

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
NUM_OF_PARTICLES = 50
MIN_ZOOM = 0.1
MAX_ZOOM = 20

def draw_grid(surface, grid_color, cell_size, offset):
    """
    Draws a grid on the given surface.
    Args:
    - surface: The Pygame surface to draw on.
    - grid_color: The color of the grid lines.
    - cell_size: The size of each cell in the grid.
    """
    width, height = surface.get_size()
    # Draw vertical lines
    for x in range(0, 64 * width, cell_size):
        pg.draw.line(surface, grid_color, (x - offset[0], 0), (x - offset[0], height))
    # Draw horizontal lines
    for y in range(0, 64 * height, cell_size):
        pg.draw.line(surface, grid_color, (0, y - offset[1]), (width, y - offset[1]))

# Usage example within your game loop:
# Define your grid color and cell size
grid_color = (200, 200, 200)  # Light grey color for the grid lines
cell_size = 40  # Adjust the cell size as per your requirement
window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pg.display.set_mode(window_size)
# In your main game loop, before drawing anything else:
screen.fill((0, 0, 0))  # Fill the screen with black or your desired background color

def main():
    print("interstellarIO")

    pg.init()
    
    pg.display.set_caption("Interstellar IO")

    screen = pg.display.set_mode(window_size)

    bodies = []

    first_player = Body(100, np.array([WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2]), np.array([0.0, 0.0]), 0)
    next_player_uid = 1

    bodies.append(first_player)
    
    clock = pg.time.Clock()
    camera = Camera(bodies[0], screen)
    targetZoom = camera.calculate_zoom_based_on_mass()
    spawner = Spawner(bodies[0])
    
    running = True
    # pygame main loop
    while running:
        screen.fill((255, 255, 255))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                
            if event.type == pg.MOUSEWHEEL:
                sensitivity = 0.1
                if camera.zoom + event.y * sensitivity > MIN_ZOOM and camera.zoom + event.y * sensitivity < MAX_ZOOM: 
                    camera.zoom += event.y * sensitivity
                    
            if pg.key.get_pressed()[pg.K_SPACE]:
                direction = np.array([pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]]) - np.array([WINDOW_WIDTH/2, WINDOW_HEIGHT/2])
                if np.linalg.norm(direction) != 0:
                    direction = direction / np.linalg.norm(direction)
                else:
                    direction = np.array([0.0, 0.0])
                ejectedMass = camera.obj.mass / 250
                relMassVelocity = 4 * math.sqrt(camera.obj.mass)
                camera.obj.mass -= ejectedMass
                dforce = camera.obj.mass * ejectedMass * relMassVelocity
                dforce /= (DT * (1 - ejectedMass))

                camera.obj.add_force(direction, dforce)
            
        
        for i in range(UPDATES_PER_FRAME):
            for j in bodies:
                 current = 0
            body_count = len(bodies)
            while current < body_count:
                merges = bodies[current].update(DT / UPDATES_PER_FRAME, bodies, current + 1, (bodies[current].uid == camera.obj.uid), spawner.newRadius(camera.obj))
                for m in merges:
                    if m[1] == -2:
                        # Was despawned
                        if m[0] == current:
                            current -= 1

                    if m[0] == -1:
                        # Self was deleted
                        current -= 1
                    if m[0] == camera.obj.uid:
                        # Camera needs change
                        
                        for b in bodies:
                            if b.uid == m[1]:
                                camera.obj = b
                                targetZoom = camera.calculate_zoom_based_on_mass()
                                break

                body_count -= len(merges)
                current += 1


        n_particles = len(bodies)
        for i in range(NUM_OF_PARTICLES - n_particles):
            bodies.append(spawner.spawnParticle(camera.obj, next_player_uid))
            next_player_uid += 1

        draw_grid(screen, grid_color, cell_size, camera.offset)
        camera.update(targetZoom)
        camera.draw(bodies)
        pg.display.flip()
        clock.tick(60)
    
    pg.quit()

if __name__ == "__main__":
    main()