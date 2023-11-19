import math
import pygame as pg
import numpy as np
from Body import Body

def do_calculation(cell_size, cell_count, gravity_points: [Body], curve_spacetime, curve_all, camera, screen, gravity_force = 2000) -> np.ndarray:
    grid = []

    half_window = np.array(screen.get_size()) / 2
    lower_coordinates = camera.obj.pos - half_window / camera.zoom
    upper_coordinates = camera.obj.pos + half_window / camera.zoom

    for yi in range(cell_count):
        row = []
        for xi in range(cell_count):
            x = cell_size * xi - (cell_size * cell_count / 2) + screen.get_size()[0] / 2
            y = cell_size * yi - (cell_size * cell_count / 2) + screen.get_size()[1] / 2

            # Skip if not in field of view
            # We add/subtract 2*cell_size as a buffer (otherwise draw_grid sometimes performs an out-of-bounds operation as it needs a point we thought was out of camera)
            if x + 4*cell_size < lower_coordinates[0] or x - 4*cell_size > upper_coordinates[0]:
                continue
            if y + 4*cell_size < lower_coordinates[1] or y - 4*cell_size > upper_coordinates[1]:
                continue

            if not curve_spacetime:
                row.append([x, y])
                continue

            for body in gravity_points:
                if body.mass < 1000 and not curve_all:
                    continue
                px = (body.pos[0] - screen.get_size()[0] / 2) * camera.zoom + screen.get_size()[0] / 2
                py = (body.pos[1] - screen.get_size()[1] / 2) * camera.zoom + screen.get_size()[1] / 2
                dx = (px - x)
                dy = (py - y)
                d = dx**2 + dy**2
                if d < body.radius or d > 50 * body.radius:
                    continue
                if d > 0:
                    a = np.arctan2(dy, dx)
                    f = gravity_force / d * math.sqrt(body.mass / 5000)
                    f = f if f < d else d
                    f = min(f, 12)
                    x += np.cos(a) * f
                    y += np.sin(a) * f

            row.append([x, y])
        if len(row) > 0:
            grid.append(row)
    return np.array(grid)


def draw_grid(surface: pg.Surface, grid_color: (int, int, int), cell_size, cell_count, offset: np.ndarray[np.float64], gravity_points: [Body], curve_spacetime, curve_all, camera):
    """
    Draws a warped grid on the given surface with respect to gravity points.
    Args:
    - surface: The Pygame surface to draw on.
    - grid_color: The color of the grid lines.
    - cell_size: The size of each cell in the grid.
    - gravity_points: A list of tuples representing the positions of gravity points.
    """

    warped_grid = do_calculation(cell_size, cell_count, gravity_points, curve_spacetime, curve_all, camera, surface)

    half_screen_size = np.array(surface.get_size()) / 2

    # Draw the warped grid lines
    for yi in range(len(warped_grid) - 2):
        for xi in range(len(warped_grid[0]) - 3):
            start_pos = (warped_grid[yi, xi] - offset - half_screen_size) * camera.zoom + half_screen_size
            end_pos = (warped_grid[yi, xi + 1] - offset - half_screen_size) * camera.zoom + half_screen_size
            #start_pos = warped_grid[yi, xi] - offset
            #end_pos = warped_grid[yi, xi+1] - offset
            pg.draw.line(surface, grid_color, start_pos, end_pos)

            start_pos = (warped_grid[xi, yi] - offset - half_screen_size) * camera.zoom + half_screen_size
            end_pos = (warped_grid[xi + 1, yi] - offset - half_screen_size) * camera.zoom + half_screen_size
            #start_pos = warped_grid[xi, yi] - offset
            #end_pos = warped_grid[xi+1, yi] - offset
            pg.draw.line(surface, grid_color, start_pos, end_pos)