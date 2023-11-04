import numpy as np
import pygame as pg


WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
NUM_OF_PARTICLES = 20
MAP_WIDTH = 3000
MAP_HEIGHT = 3000

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)

        # Keep the camera within the map boundaries
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - window_width), x)
        y = max(-(self.height - window_height), y)

        self.camera = pg.Rect(x, y, self.width, self.height)
        