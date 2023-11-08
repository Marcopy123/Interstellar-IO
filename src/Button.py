import pygame as pg

GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

class Button:
    def __init__(self, x, y, width, height, on_click):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.on_click = on_click

    def handle_event(self, event: pg.event.Event):
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if self.x < mouse_x and mouse_x < self.x + self.w and self.y < mouse_y and mouse_y < self.y + self.h:
                self.on_click()

    def draw(self, screen: pg.Surface, enabled):
        pg.draw.rect(screen, GREEN if enabled else RED, (self.x, self.y, self.w, self.h))
        circle_color = WHITE
        circle_pos = (self.x + self.h // 2, self.y + self.h // 2) if not enabled else (self.x + self.w - self.h // 2, self.y + self.h // 2)
        pg.draw.circle(screen, circle_color, circle_pos, self.h // 2 - 5)