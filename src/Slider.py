import pygame as pg

COLOR_INACTIVE = (255, 255, 255)
COLOR_ACTIVE = (0, 255, 0)
HANDLE_RADIUS = 10

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, start_val):
        self.rect = pg.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.val = start_val
        self.handle_rect = pg.Rect(x + (start_val - min_val) / (max_val - min_val) * w, y - HANDLE_RADIUS, HANDLE_RADIUS * 2, HANDLE_RADIUS * 2)
        self.active = False


    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.active = True

        elif event.type == pg.MOUSEBUTTONUP:
            self.active = False

        elif event.type == pg.MOUSEMOTION:
            if self.active:
                mouse_x, _ = event.pos
                new_x = max(self.rect.left, min(mouse_x, self.rect.right))
                self.handle_rect.centerx = new_x
                self.val = self.min_val + (self.max_val - self.min_val) * ((new_x - self.rect.left) / self.rect.width)

    def draw(self, surface: pg.Surface) -> None:
        pg.draw.rect(surface, COLOR_INACTIVE if not self.active else COLOR_ACTIVE, self.rect)
        pg.draw.circle(surface, COLOR_INACTIVE if not self.active else COLOR_ACTIVE, self.handle_rect.center, HANDLE_RADIUS)

    def get_value(self):
        return self.val