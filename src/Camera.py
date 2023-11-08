import numpy as np
import pygame as pg
import math

from Body import MAX_TRAIL, TRAIL_THICC

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
NUM_OF_PARTICLES = 250
MAP_WIDTH = 3000
MAP_HEIGHT = 3000

class Camera:
    def __init__(self, follow_obj, screen: pg.Surface):
        self.obj = follow_obj
        self.screen = screen
        self.init_pos = follow_obj.pos.copy() + np.array([self.screen.get_size()[0]/2 - self.obj.pos[0], self.screen.get_size()[1]/2 - self.obj.pos[1]])
        self.zoom = 4.0
        self.offset = np.array([0.0, 0.0])
        self.sensitivity = 0.1
        self.fade_circle = False
        self.circle_duration = 0
        self.current_duration = 0


    def update(self) -> None:
        """
        Update camera parameters according to the player input
        """
        self.offset = self.obj.pos - self.init_pos


    def draw_fading_circle(self, surface: pg.Surface, pos, max_radius, duration, elapsed):
        center = (pos[0], pos[1])

        # A single frame
        alpha = max(0, 200 - (200 * (elapsed / duration)))
        radius = int(max_radius * (elapsed / duration))

        # Create a new surface with per-pixel alpha to draw the circle with alpha transparency
        pg.draw.circle(surface, (255, 255, 255, int(alpha)), center, radius)


    def color_from_speed(self, speed: float) -> pg.Color:
        # the most cursed thing you'll ever see
        # TODO work in progress
        speed = int(speed)
        color = [0, 0, 190]
        color[1] += speed
        speed -= 190
        if speed >= 0:
            color[1] = 190
            color[2] -= speed
            speed -= 190
            if speed >= 0:
                color[2] = 0
                color[0] += speed
                speed -= 190
                if speed >= 0:
                    color[0] = 190
                    color[1] -= speed
                    color[1] = max(color[1], 0)
        return pg.Color(color[0], color[1], color[2], a=0.3)


    def draw_object(self, obj):
        trail_idx = 0
        for j in obj.trail:
            x_pos = (j[0] - self.offset[0] - self.screen.get_size()[0] / 2) * self.zoom + self.screen.get_size()[0] / 2
            y_pos = (j[1] - self.offset[1] - self.screen.get_size()[1] / 2) * self.zoom + self.screen.get_size()[1] / 2
            pg.draw.circle(self.screen, self.color_from_speed(j[2] * 100), (x_pos, y_pos), obj.radius * TRAIL_THICC * self.zoom * (trail_idx + 1) / MAX_TRAIL)
            trail_idx += 1
        
        # Draw object
        x_pos = (obj.pos[0] - self.offset[0] - self.screen.get_size()[0] / 2) * self.zoom + self.screen.get_size()[0] / 2
        y_pos = (obj.pos[1] - self.offset[1] - self.screen.get_size()[1] / 2) * self.zoom + self.screen.get_size()[1] / 2
        img = pg.transform.scale(obj.image, (obj.radius * self.zoom * 3, obj.radius * self.zoom * 3))
        self.screen.blit(img, (x_pos - obj.radius * self.zoom * 3/2 , y_pos - obj.radius * self.zoom * 3/2))


    def draw(self, objs, fade_circle_surface: pg.Surface):
        for i in objs:
            # Draw trail
            if i.uid == self.obj.uid:
                continue
            self.draw_object(i)

        # Do camera
        self.draw_object(self.obj)

        if self.fade_circle:
            self.circle_duration = 100
            self.current_duration = 0
            self.fade_circle = False
        
        if self.current_duration < self.circle_duration:
            circle_x_pos = self.screen.get_size()[0] / 2
            circle_y_pos = self.screen.get_size()[1] / 2
            self.draw_fading_circle(fade_circle_surface, [circle_x_pos, circle_y_pos], self.screen.get_size()[0], self.circle_duration, self.current_duration)
            self.current_duration += 1
            if self.current_duration >= self.circle_duration:
                self.current_duration = 0
                self.circle_duration = 0