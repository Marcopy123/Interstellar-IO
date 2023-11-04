import numpy as np
import pygame as pg
import math

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
NUM_OF_PARTICLES = 250
MAP_WIDTH = 3000
MAP_HEIGHT = 3000
some_mass_to_zoom_scaling_factor = 100

class Camera:
    def __init__(self, follow_obj, screen) -> None:
        self.obj = follow_obj
        self.screen = screen
        self.init_pos = follow_obj.pos.copy() + np.array([self.screen.get_size()[0]/2 - self.obj.pos[0], self.screen.get_size()[1]/2 - self.obj.pos[1]])
        self.zoom = 0.6
        self.offset = np.array([0.0, 0])
        self.sensitivity = 0.1

    def calculate_zoom_based_on_mass(self):
        # Example calculation, needs tuning to fit the game's feel and scale
        # The '-1' ensures that when mass is at a base level, the zoom is neutral (1)
        return 1 / self.obj.mass

    def update(self, target_zoom):
        """
        Update camera parameters according to the player input
        """
        self.offset = self.obj.pos - self.init_pos
        # self.zoom += (0.01 if self.zoom < target_zoom else 0.0)
        # if self.zoom < target_zoom:
        #     print("a")


    def zoom_dist(self, objs):
        """_summary_
        return
        Args:
            objs (list): list of objects
        """
    def draw(self, objs):
        for i in objs:
            if True:
                #pg.draw.circle(self.screen, (0, 0, 0), (draw_pos[0] - self.offset[0], draw_pos[1] - self.offset[1]), i.radius)
                x_pos = (i.pos[0] - self.offset[0] - self.screen.get_size()[0] / 2) * self.zoom + self.screen.get_size()[0] / 2
                y_pos = (i.pos[1] - self.offset[1] - self.screen.get_size()[1] / 2) * self.zoom + self.screen.get_size()[1] / 2
                pg.draw.circle(self.screen, (0, 0, 0), (x_pos, y_pos), i.radius * self.zoom)
            
        