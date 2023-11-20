import math 
import numpy as np
import pygame as pg
import random
from sys import argv
from time import time

from Body import Body
from Camera import Camera
from Spawner import Spawner
from Slider import Slider
from Button import Button
from Grid import draw_grid
import Body as BodyFile

DT = 0.3 # Delta time for the physics engine
UPDATES_PER_FRAME = 1 # Number of iterations of the physics engine for each frame

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
NUM_OF_PARTICLES = 50
MAX_ZOOM = 50
SLIDER_LENGTH = 200
SLIDER_HEIGHT = 5

# To set once pygame is initialized
FONT1 = None
FONT2 = None

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (60, 250, 60)

ALT_REND = False
CURVE_SPACETIME = False
SPAWN_SEED = -1


def toggle_alt_render():
    global ALT_REND
    ALT_REND = not ALT_REND


def toggle_spacetime():
    global CURVE_SPACETIME
    CURVE_SPACETIME = not CURVE_SPACETIME


def create_text_surface(text: str, font: pg.font.Font, color: pg.Color):
    text_surface = font.render(text, True, color)
    return text_surface


def set_gravitational_constant(value):
    BodyFile.BIG_G = value


def main(render_mode=0):
    global DT
    global NUM_OF_PARTICLES
    global ALT_REND
    global SPAWN_SEED
    global CURVE_SPACETIME
    global FONT1
    global FONT2
    print("singularIO")

    pg.init()

    FONT1 = pg.font.Font(None, 30)
    FONT2 = pg.font.Font(None, 20)
    
    gravitySlider = Slider(20, 20, SLIDER_LENGTH, SLIDER_HEIGHT, 0.1, 20, BodyFile.BIG_G)
    timeSlider = Slider(20, 50, SLIDER_LENGTH, SLIDER_HEIGHT, 0.000001, 3, 0.3)
    particlesSlider = Slider(20, 80, SLIDER_LENGTH, SLIDER_HEIGHT, 1, 100, NUM_OF_PARTICLES)

    altButton = Button(585, 20, 40, 20, toggle_alt_render)
    spacetimeButton = Button(585, 50, 40, 20, toggle_spacetime)

    pg.display.set_caption("Singulario")

    screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Grid parameters
    grid_color = (150, 150, 150) # Light grey
    cell_size = 40

    bodies = []

    if render_mode == 1:
        NUM_OF_PARTICLES = 1
        sun = Body(2000, np.array([WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2]), np.array([0.0, 0.0]), 0)
        moon = Body(200, np.array([WINDOW_WIDTH / 3, WINDOW_HEIGHT / 2]), np.array([0.0, 6.0]), 1)
        earth = Body(1000, np.array([WINDOW_WIDTH / 4.5, WINDOW_HEIGHT / 2]), np.array([0.0, 3.0]), 2)
        bodies.append(sun)
        bodies.append(earth)
        bodies.append(moon)
        next_player_uid = 3
    else:
        first_player = Body(100, np.array([WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2]), np.array([0.0, 0.0]), 0)
        next_player_uid = 1
        bodies.append(first_player)
    
    clock = pg.time.Clock()
    camera = Camera(bodies[0], screen)
    spawner = Spawner(bodies[0], SPAWN_SEED)

    fade_circle_surface = pg.Surface((screen.get_size()), pg.SRCALPHA)

    if render_mode == 0:
        # First round of spawning is anywhere around the player, not at the edge of the spawn circle
        for i in range(NUM_OF_PARTICLES - 1):
            bodies.append(spawner.spawn_particle(bodies[0], next_player_uid, True))
            next_player_uid += 1

    
    running = True
    start_time = time()

    # Main loop
    while running:
        if time() > start_time + 3600 * 24 * 365 * 1000000000:
            print("Hawking radiation. You die.")
            exit(0)

        screen.fill((0,0,42))
        for event in pg.event.get():
            pos = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                running = False
            gravitySlider.handle_event(event)
            timeSlider.handle_event(event)
            particlesSlider.handle_event(event)
            altButton.handle_event(event)
            spacetimeButton.handle_event(event)



            if event.type == pg.MOUSEWHEEL:
                sensitivity = 0.1
                new_zoom = camera.zoom + event.y * sensitivity
                if new_zoom < MAX_ZOOM:
                    camera.zoom += event.y * camera.zoom * sensitivity
                    print(camera.zoom)

            elif event.type == pg.KEYDOWN and render_mode == 1:
                if pg.key.get_pressed()[pg.K_RETURN]:
                    # Switch camera to next body
                    next_body = bodies.index(camera.obj) + 1
                    if next_body >= len(bodies):
                        next_body = 0
                    camera.obj = bodies[next_body]
                    
            if pg.key.get_pressed()[pg.K_SPACE]:
                
                direction = np.array([pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]]) - np.array([WINDOW_WIDTH/2, WINDOW_HEIGHT/2])
                if np.linalg.norm(direction) != 0:
                    direction = direction / np.linalg.norm(direction)
                else:
                    direction = np.array([0.0, 0.0])
                ejectedMass = camera.obj.mass / 500
                relMassVelocity = 6 * math.sqrt(camera.obj.mass)
                camera.obj.mass -= ejectedMass
                dforce = camera.obj.mass * ejectedMass * relMassVelocity
                dforce /= (DT * (1 - ejectedMass))

                camera.obj.add_force(direction, dforce)
        
        # grid_scaling is the closest power of 3 to camera.zoom (so the grid is divided/multiplied by 3 according to the camera zoom)
        log3n = math.floor(math.log(camera.zoom, 3))
        grid_scaling = 3 ** log3n
        if camera.zoom > grid_scaling * 2:
            grid_scaling *= 3

        draw_grid(screen, grid_color, int(cell_size / grid_scaling), camera.offset, bodies, CURVE_SPACETIME, (render_mode == 1), camera)

        for i in range(UPDATES_PER_FRAME):
            for j in bodies:
                current = 0
            body_count = len(bodies)
            while current < body_count:
                merges = bodies[current].update(DT / UPDATES_PER_FRAME, bodies, current + 1, (bodies[current].uid == camera.obj.uid), spawner.new_radius(camera.obj), ALT_REND, camera)
                for m in merges:
                    if m[0] == camera.obj.uid:
                        # Camera needs change
                        for b in bodies:
                            if b.uid == m[1]:
                                camera.obj = b
                                break
                body_count -= len(merges)
                current += 1

        gValueText = create_text_surface(str(round(BodyFile.BIG_G, 2)), FONT1, WHITE)
        timeValueText = create_text_surface(str(round(DT, 2)), FONT1, WHITE)
        numParticlesText = create_text_surface(str(NUM_OF_PARTICLES), FONT1, WHITE)
        altButtonText = create_text_surface(f"Alternate simulation", FONT1, WHITE)
        spacetimeText = create_text_surface(f"Visualize spacetime", FONT1, WHITE)

        gText = create_text_surface("Gravitational Constant", FONT2, WHITE)
        timeFactor = create_text_surface("Time Factor", FONT2, WHITE)
        numParticles = create_text_surface("Number of particles", FONT2, WHITE)

        n_particles = len(bodies)
        for i in range(NUM_OF_PARTICLES - n_particles):
            bodies.append(spawner.spawn_particle(camera.obj, next_player_uid, False))
            next_player_uid += 1
        set_gravitational_constant(gravitySlider.get_value())
        DT = timeSlider.get_value()
        if render_mode != 1:
            NUM_OF_PARTICLES = int(particlesSlider.get_value())
        
        camera.update()
        camera.draw(bodies, fade_circle_surface)
    
        numOfSolarMasses = camera.obj.mass / (195000)

        currentMassText = create_text_surface("Current mass: ~" + str(round(numOfSolarMasses, 6)) + "sol", FONT1, WHITE)
        
        currentStateText = create_text_surface("You currently have the mass of: " + str(camera.obj.state), FONT1, WHITE)
        screen.blit(currentMassText, (25, 630))
        screen.blit(currentStateText, (25, 660))
        screen.blit(gValueText, (230, 15))
        screen.blit(timeValueText, (230, 45))
        screen.blit(numParticlesText, (230, 75))

        screen.blit(fade_circle_surface, (0, 0))
        
        screen.blit(gText, (60, 25))
        screen.blit(timeFactor, (90, 55))
        screen.blit(numParticles, (70, 90))
        screen.blit(altButtonText, (370, 20))
        screen.blit(spacetimeText, (370, 50))

        gravitySlider.draw(screen)
        timeSlider.draw(screen)
        particlesSlider.draw(screen)
        altButton.draw(screen, ALT_REND)
        spacetimeButton.draw(screen, CURVE_SPACETIME)
        pg.display.flip()
        clock.tick(60)
    
    pg.quit()

if __name__ == "__main__":
    render_mode = 0
    if len(argv) == 2:
        if argv[1] == "solar":
            render_mode = 1
        elif argv[1].isdigit():
            SPAWN_SEED = int(argv[1])

        else:
            print("Unknown argument")
    main(render_mode)