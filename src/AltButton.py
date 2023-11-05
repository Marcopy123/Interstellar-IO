import pygame

GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

class AltButton:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.on = False

    def draw(self, win):
        pygame.draw.rect(win, GREEN if self.on else RED, (self.x, self.y, self.width, self.height))
        circle_color = WHITE
        circle_pos = (self.x + self.height // 2, self.y + self.height // 2) if not self.on else (self.x + self.width - self.height // 2, self.y + self.height // 2)
        pygame.draw.circle(win, circle_color, circle_pos, self.height // 2 - 5)

    def toggle(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            self.on = not self.on