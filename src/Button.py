import pygame as pg

GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, onClick):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.onClick = onClick

    def handle_event(self, event: pg.event.Event):
        if event.type == pg.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            if self.x < mouseX and mouseX < self.x + self.w and self.y < mouseY and mouseY < self.y + self.h:
                self.onClick()

    def draw(self, win: pg.Surface, enabled: bool):
        pg.draw.rect(win, GREEN if enabled else RED, (self.x, self.y, self.w, self.h))
        circle_color = WHITE
        circle_pos = (self.x + self.h // 2, self.y + self.h // 2) if not enabled else (self.x + self.w - self.h // 2, self.y + self.h // 2)
        pg.draw.circle(win, circle_color, circle_pos, self.h // 2 - 5)