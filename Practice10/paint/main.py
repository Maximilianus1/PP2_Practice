import pygame
import math

pygame.init()
WIDTH, HEIGHT = 1200, 600
TOOLBAR_HEIGHT = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)
current_tool = "brush"
current_color = (0, 0, 255)
drawing = False
start_pos = None
canvas = []
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
fill_mode = False

#кнопки
buttons = [
    Button(10, 10, 80, 40, "Brush", "brush"),
    Button(100, 10, 80, 40, "Rect", "rectangle"),
    Button(190, 10, 80, 40, "Circle", "circle"),
    Button(280, 10, 80, 40, "Square", "square"),
    Button(370, 10, 80, 40, "R.Tri", "right_triangle"),
    Button(460, 10, 80, 40, "E.Tri", "equilateral_triangle"),
    Button(550, 10, 80, 40, "Rhomb", "rhombus"),
    Button(640, 10, 80, 40, "Erase", "eraser"),
    Button(750, 10, 80, 40, "Fill", "toggle_fill"),
]
r,g,b = 0, 0, 255
slider_dragging = None
current_color = (r, g, b)
def draw_shape(surface, tool, start, end, color, fill):
    x1, y1 = start
    x2, y2 = end
    width = 0 if fill else 2
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
    elif tool == "brush":
        pygame.draw.line(surface, color, start, end, 3)
    elif tool == "eraser":
        pygame.draw.line(surface, (255, 255, 255), start, end, 10)
running = True
preview_shape = None  # временная фигура
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            # кнопки
            for btn in buttons:
                if btn.clicked(pos):
                    if btn.action == "toggle_fill":
                        fill_mode = not fill_mode
                    else:
                        current_tool = btn.action
            # ckfqlths
            mx, my = pos
            if 10 <= mx <= 210:
                if 80 <= my <= 90:
                    slider_dragging = "r"
                elif 110 <= my <= 120:
                    slider_dragging = "g"
                elif 140 <= my <= 150:
                    slider_dragging = "b"
            # рисуй где положено
            if pos[1] > TOOLBAR_HEIGHT:
                drawing = True
                start_pos = pos
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            slider_dragging = None
            if preview_shape:
                canvas.append(preview_shape)
                preview_shape = None
        elif event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            if slider_dragging:
                val = max(0, min(255, (mx - 10) * 255 // 200))
                if slider_dragging == "r":
                    r = val
                elif slider_dragging == "g":
                    g = val
                elif slider_dragging == "b":
                    b = val
                current_color = (r, g, b)
            # рисование
            elif drawing:
                if my <= TOOLBAR_HEIGHT:
                    continue
                current_pos = event.pos
                if current_tool == "brush":
                    canvas.append(("brush", start_pos, current_pos, current_color, fill_mode))
                    start_pos = current_pos
                elif current_tool == "eraser":
                    canvas.append(("eraser", start_pos, current_pos, current_color, fill_mode))
                    start_pos = current_pos
                else:
                    preview_shape = (current_tool, start_pos, current_pos, current_color, fill_mode)



    screen.fill((255, 255, 255))
    for shape in canvas:
        draw_shape(screen, *shape)
    if preview_shape:
        draw_shape(screen, *preview_shape)
    pygame.draw.rect(screen, (20, 20, 20), (0, 0, WIDTH, TOOLBAR_HEIGHT))
    for btn in buttons:
        btn.draw(screen)
    draw_slider(screen, 10, 80, r, (255, 0, 0))
    draw_slider(screen, 10, 110, g, (0, 255, 0))
    draw_slider(screen, 10, 140, b, (0, 0, 255))
    pygame.draw.rect(screen, current_color, (230, 80, 60, 60))
    pygame.draw.rect(screen, (0, 0, 0), (230, 80, 60, 60), 2)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()