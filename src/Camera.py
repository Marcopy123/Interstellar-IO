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
        self.zoom = 4
        self.offset = np.array([0.0, 0.0])
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

    def color_from_speed(self, speed):
        # the most cursed thing you'll ever see
        # TODO work in progress
        speed = int(speed / 10)
        color = [0, 0, 255]
        color[1] += speed
        speed -= 255
        if speed <= 0:
            color[1] = 255
            color[2] -= speed
            speed -= 255
            if speed <= 0:
                color[2] = 0
                color[0] += speed
                speed -= 255
                if speed <= 0:
                    color[1] = 0
                    color[0] = 255
        return pg.Color(color[0], color[1], color[2], a=0.5)


    def draw(self, objs, camera):
        for i in objs:
            # Draw trail
            if i.uid == camera.uid:
                continue
            trail_idx = 0
            for j in i.trail:
                x_pos = (j[0] - self.offset[0] - self.screen.get_size()[0] / 2) * self.zoom + self.screen.get_size()[0] / 2
                y_pos = (j[1] - self.offset[1] - self.screen.get_size()[1] / 2) * self.zoom + self.screen.get_size()[1] / 2
                pg.draw.circle(self.screen, pg.Color(128, 128, 128, a=0.5), (x_pos, y_pos), i.radius / 3 * self.zoom * (trail_idx + 1) / self.obj.max_trail)
                #pg.draw.circle(self.screen, self.color_from_speed(j[2]), (x_pos, y_pos), i.radius/3 * self.zoom * (trail_idx + 1)/self.obj.max_trail)
                trail_idx += 1
            
            # Draw object
            x_pos = (i.pos[0] - self.offset[0] - self.screen.get_size()[0] / 2) * self.zoom + self.screen.get_size()[0] / 2
            y_pos = (i.pos[1] - self.offset[1] - self.screen.get_size()[1] / 2) * self.zoom + self.screen.get_size()[1] / 2
            img = pg.transform.scale(i.image, (i.radius * self.zoom * 3, i.radius * self.zoom * 3))
            self.screen.blit(img, (x_pos - i.radius * self.zoom * 3/2 , y_pos - i.radius * self.zoom * 3/2))

        # Do camera
        trail_idx = 0
        for j in camera.trail:
            x_pos = (j[0] - self.offset[0] - self.screen.get_size()[0] / 2) * self.zoom + self.screen.get_size()[0] / 2
            y_pos = (j[1] - self.offset[1] - self.screen.get_size()[1] / 2) * self.zoom + self.screen.get_size()[1] / 2
            pg.draw.circle(self.screen, pg.Color(128, 128, 128, a=0.5), (x_pos, y_pos), camera.radius / 3 * self.zoom * (trail_idx + 1) / self.obj.max_trail)
            #pg.draw.circle(self.screen, self.color_from_speed(j[2]), (x_pos, y_pos), i.radius/3 * self.zoom * (trail_idx + 1)/self.obj.max_trail)
            trail_idx += 1
        
        # Draw object
        x_pos = (camera.pos[0] - self.offset[0] - self.screen.get_size()[0] / 2) * self.zoom + self.screen.get_size()[0] / 2
        y_pos = (camera.pos[1] - self.offset[1] - self.screen.get_size()[1] / 2) * self.zoom + self.screen.get_size()[1] / 2
        img = pg.transform.scale(camera.image, (camera.radius * self.zoom * 3, camera.radius * self.zoom * 3))
        self.screen.blit(img, (x_pos - camera.radius * self.zoom * 3/2 , y_pos - camera.radius * self.zoom * 3/2))