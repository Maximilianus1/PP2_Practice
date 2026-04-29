import pygame
import math
pygame.font.init()
font = pygame.font.SysFont("Arial", 16)
WIDTH, HEIGHT = 1600, 800
TOOLBAR_HEIGHT = 60
class Button:
    def __init__(self, x, y, w, h, text, action):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action
    def draw(self, surface):
        pygame.draw.rect(surface, (50, 50, 50), self.rect)
        pygame.draw.rect(surface, (200, 200, 200), self.rect, 2)
        label = font.render(self.text, True, (255, 255, 255))
        surface.blit(label, (self.rect.x + 5, self.rect.y + 20))
    def clicked(self, pos):
        return self.rect.collidepoint(pos)
def draw_slider(screen, x, y, value, color):
    pygame.draw.rect(screen, (60, 60, 60), (x, y, 200, 10))
    pygame.draw.rect(screen, color, (x, y, value * 200 // 255, 10))
    handle_x = x + value * 200 // 255
    pygame.draw.circle(screen, (255, 255, 255), (handle_x, y + 5), 8)
def draw_shape(surface, tool, start, end, color, fill, brush_size):
    x1, y1 = start
    x2, y2 = end
    width = 0 if fill else brush_size
    if tool == "rectangle":
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        pygame.draw.rect(surface, color, rect, width)
    elif tool == "circle":
        radius = int(math.hypot(x2 - x1, y2 - y1))
        pygame.draw.circle(surface, color, start, radius, width)
    elif tool == "square":
        size = min(abs(x2 - x1), abs(y2 - y1))
        rect = pygame.Rect(x1, y1, size, size)
        pygame.draw.rect(surface, color, rect, width)
    elif tool == "right_triangle":
        points = [start, (x1, y2), end]
        pygame.draw.polygon(surface, color, points, width)
    elif tool == "equilateral_triangle":
        side = abs(x2 - x1)
        height = side * (math.sqrt(3) / 2)
        p1 = (x1, y1)
        p2 = (x1 + side, y1)
        p3 = (x1 + side / 2, y1 - height)
        pygame.draw.polygon(surface, color, [p1, p2, p3], width)
    elif tool == "rhombus":
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
        pygame.draw.polygon(surface, color, points, width)
    elif tool == "line":
        pygame.draw.line(surface, color, start, end, width)
    elif tool == "brush":
        pygame.draw.line(surface, color, start, end, width)
    elif tool == "eraser":
        pygame.draw.line(surface, (255, 255, 255), start, end, width)


def flood_fill(surface, pos, fill_color):
    start_color = surface.get_at(pos)
    if start_color == fill_color:
        return []

    queue = [pos]
    changed_pixels = []

    while queue:
        x, y = queue.pop()
        if surface.get_at((x, y)) == start_color:
            surface.set_at((x, y), fill_color)
            changed_pixels.append((x, y, fill_color))
            if x > 0: queue.append((x - 1, y))
            if x < surface.get_width() - 1: queue.append((x + 1, y))
            if y > 0: queue.append((x, y - 1))
            if y < surface.get_height() - 1: queue.append((x, y + 1))

    return changed_pixels



