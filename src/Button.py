import pygame as pg

class Button:
    def __init__(self, x: int, y: int, w: int, h: int, onClick):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.onClick = onClick
        self.isPressed = False

    def draw(self, screen, color_idle, color_pressed):
        color = color_pressed if self.isPressed else color_idle
        pg.draw.rect(screen, color, [self.x, self.y, self.w, self.h])

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            if self.x < mouseX and mouseX < self.x + self.w and self.y < mouseY and mouseY < self.y + self.h and self.isPressed == False:
                self.isPressed = True
                self.onClick()
        elif event.type == pg.MOUSEBUTTONUP:
            self.isPressed = False