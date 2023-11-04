import numpy as np
import pygame as pg

class Camera:
    def __init__(self, follow_obj, screen) -> None:
        self.obj = follow_obj
        self.screen = screen
        self.init_pos = follow_obj.pos
        self.offset = np.array([0, 0])
        
    def update(self):
        """
        Update camera position according to the player
        """
        print(self.init_pos)
        self.offset = self.obj.pos - self.init_pos
        
    def draw(self, objs):
        pg.draw.circle(self.screen, (0, 0, 0), (self.screen.get_size()[0]/2, self.screen.get_size()[1]/2), self.obj.radius)
        for i in objs:
            if i != self.obj:
                pg.draw.circle(self.screen, (0, 0, 0), (i.pos[0] + self.offset[0], i.pos[1] - self.offset[1]), i.radius)
            
        