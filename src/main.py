import math 
import numpy as np
import pygame as pg
from sys import argv
from Body import Body
import random
from Camera import Camera
from Spawner import Spawner
from GravitySlider import GravitySlider
import Body as BodyFile
from TimeSlider import TimeSlider
from ParticlesSlider import ParticlesSlider
from SpaceTimeButton import SpaceTimeButton
from AltButton import AltButton

DT = 0.3 # Delta time for the physics engine
UPDATES_PER_FRAME = 1 # Number of iterations of the physics engine for each frame

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
NUM_OF_PARTICLES = 50
MIN_ZOOM = 0.000000000001
MAX_ZOOM = 20
SLIDER_LENGTH = 200
SLIDER_HEIGHT = 5

pg.init()
FONT1 = pg.font.Font(None, 30)
FONT2 = pg.font.Font(None, 20)

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (60, 250, 60)

ALT_REND = False
CURVE_SPACETIME = False
SPAWN_SEED = -1



gravitySlider = GravitySlider(20, 20, SLIDER_LENGTH, SLIDER_HEIGHT, 0.1, 20, BodyFile.G)
timeSlider = TimeSlider(20, 50, SLIDER_LENGTH, SLIDER_HEIGHT, 0.01, 3, DT)
particlesSlider = ParticlesSlider(20, 80, SLIDER_LENGTH, SLIDER_HEIGHT, 1, 100, NUM_OF_PARTICLES)

def create_text_surface(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface

def do_calculation(width, height, grid_count, gravity_points, curve_spacetime: bool, curve_all: bool, gravity_force=2000):
    grid = []

    for yi in range(grid_count):
        row = []
        for xi in range(grid_count):
            x = (width / grid_count) * xi
            y = (height / grid_count) * yi

            if not curve_spacetime:
                row.append([x, y])
                continue

            for body in gravity_points:
                if body.mass < 1000 and not curve_all:
                    continue
                px = body.pos[0]
                py = body.pos[1]
                dx = px - x
                dy = py - y
                d = dx**2 + dy**2
                if d < body.radius:
                    continue
                if d > 0:
                    a = np.arctan2(dy, dx)
                    f = gravity_force / d * math.sqrt(body.mass / 1000)
                    f = f if f < d else d
                    f = min(f, 8)
                    x += np.cos(a) * f
                    y += np.sin(a) * f

            row.append([x, y])
        grid.append(row)
    return np.array(grid)

def draw_grid(surface, grid_color, cell_size, offset, gravity_points, curve_spacetime: bool, curve_all: bool):
    """
    Draws a warped grid on the given surface with respect to gravity points.
    Args:
    - surface: The Pygame surface to draw on.
    - grid_color: The color of the grid lines.
    - cell_size: The size of each cell in the grid.
    - gravity_points: A list of tuples representing the positions of gravity points.
    """
    width, height = 3000,3000
    grid_count = max(width, height) // cell_size  # Number of cells in the largest dimension

    warped_grid = do_calculation(width, height, grid_count, gravity_points, curve_spacetime, curve_all)

    # Draw the warped grid lines
    for yi in range(grid_count):
        for xi in range(grid_count - 1):
            start_pos = warped_grid[yi, xi] - np.array(offset)
            end_pos = warped_grid[yi, xi + 1] - np.array(offset)
            pg.draw.line(surface, grid_color, start_pos, end_pos)

            start_pos = warped_grid[xi, yi] - np.array(offset)
            end_pos = warped_grid[xi + 1, yi] - np.array(offset)
            pg.draw.line(surface, grid_color, start_pos, end_pos)

# Usage example within your game loop:
# Define your grid color and cell size
grid_color = (150, 150, 150)  # Light grey color for the grid lines
cell_size = 40  # Adjust the cell size as per your requirement
window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pg.display.set_mode(window_size)
# In your main game loop, before drawing anything else:

def set_gravitational_constant(value):
    global G
    BodyFile.G = value

def main(render_mode: int):
    global DT
    global NUM_OF_PARTICLES
    global ALT_REND
    global SPAWN_SEED
    global CURVE_SPACETIME
    print("interstellarIO")

    pg.init()
    
    AltRenderingButton = AltButton(585, 20, 40, 20)
    SpaceTimeButtonRender = SpaceTimeButton(585, 50, 40, 20)
    pg.display.set_caption("Interstellar IO")

    screen = pg.display.set_mode(window_size)

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
    targetZoom = camera.calculate_zoom_based_on_mass()
    spawner = Spawner(bodies[0], SPAWN_SEED)

    if render_mode == 0:
        # First round of spawning is anywhere around the player, not at the edge of the spawn circle
        for i in range(NUM_OF_PARTICLES - 1):
            bodies.append(spawner.spawnParticle(bodies[0], next_player_uid, True))
            next_player_uid += 1

    
    running = True
    # pygame main loop
    while running:
        screen.fill((0,0,42))
        for event in pg.event.get():
            pos = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                running = False
            gravitySlider.handle_event(event)
            timeSlider.handle_event(event)
            particlesSlider.handle_event(event)
            # altButton.handle_event(event)
            # spacetimeButton.handle_event(event)

            if event.type == pg.MOUSEBUTTONDOWN:
                AltRenderingButton.toggle(pos)
                SpaceTimeButtonRender.toggle(pos)
                ALT_REND = AltRenderingButton.on
                CURVE_SPACETIME = SpaceTimeButtonRender.on

            if event.type == pg.MOUSEWHEEL:
                sensitivity = 0.1
                if camera.zoom + event.y * sensitivity > MIN_ZOOM or event.y > 0:
                    camera.zoom += event.y * camera.zoom * sensitivity
                else:
                    camera.zoom -= camera.zoom * sensitivity
            elif event.type == pg.KEYDOWN and render_mode == 1:
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
            
        draw_grid(screen, grid_color, cell_size, camera.offset, bodies, CURVE_SPACETIME, (render_mode == 1))
        

        for i in range(UPDATES_PER_FRAME):
            for j in bodies:
                 current = 0
            body_count = len(bodies)
            while current < body_count:
                merges = bodies[current].update(DT / UPDATES_PER_FRAME, bodies, current + 1, (bodies[current].uid == camera.obj.uid), spawner.newRadius(camera.obj), ALT_REND)
                for m in merges:

                    if m[0] == -1:
                        # Self was deleted
                        current -= 1
                    if m[0] == camera.obj.uid:
                        # Camera needs change
                        
                        for b in bodies:
                            if b.uid == m[1]:
                                camera.obj = b
                                ntargetZoom = camera.calculate_zoom_based_on_mass()
                                #if ntargetZoom != targetZoom:
                                    #print("a")
                                break
                body_count -= len(merges)
                current += 1

        gValueText = create_text_surface(str(round(BodyFile.G, 2)), FONT1, WHITE)
        timeValueText = create_text_surface(str(round(DT, 2)), FONT1, WHITE)
        numParticlesText = create_text_surface(str(NUM_OF_PARTICLES), FONT1, WHITE)
        altButtonText = create_text_surface(f"Alternate simulation", FONT1, WHITE)
        spacetimeText = create_text_surface(f"Visualize spacetime", FONT1, WHITE)

        gText = create_text_surface("Gravitational Constant", FONT2, WHITE)
        timeFactor = create_text_surface("Time Factor", FONT2, WHITE)
        numParticles = create_text_surface("Number of particles", FONT2, WHITE)

        n_particles = len(bodies)
        for i in range(NUM_OF_PARTICLES - n_particles):
            bodies.append(spawner.spawnParticle(camera.obj, next_player_uid, False))
            next_player_uid += 1
        set_gravitational_constant(gravitySlider.get_value())
        DT = timeSlider.get_value()
        if render_mode != 1:
            NUM_OF_PARTICLES = int(particlesSlider.get_value())
        
        camera.update(targetZoom)
        camera.draw(bodies, camera.obj)
    
        numOfSolarMasses = camera.obj.mass / (195000)

        currentMassText = create_text_surface("Current mass: ~" + str(round(numOfSolarMasses, 6)) + "sol", FONT1, WHITE)
        
        currentStateText = create_text_surface("You currently have the mass of: " + str(camera.obj.state), FONT1, WHITE)
        screen.blit(currentMassText, (25, 630))
        screen.blit(currentStateText, (25, 660))
        screen.blit(gValueText, (230, 15))
        screen.blit(timeValueText, (230, 45))
        screen.blit(numParticlesText, (230, 75))
        
        screen.blit(gText, (60, 25))
        screen.blit(timeFactor, (90, 55))
        screen.blit(numParticles, (70, 90))
        screen.blit(altButtonText, (370, 20))
        screen.blit(spacetimeText, (370, 50))
        gravitySlider.draw(screen)
        timeSlider.draw(screen)
        particlesSlider.draw(screen)
        # altButton.draw(screen, WHITE, GREEN)
        # spacetimeButton.draw(screen, WHITE, GREEN)
        SpaceTimeButtonRender.draw(screen)
        AltRenderingButton.draw(screen)
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