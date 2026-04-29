
import pygame
import math
import datetime
from tools import *

pygame.init()
WIDTH, HEIGHT = 1600, 800
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


def save_canvas(surface):
    filename = "canvas_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
    pygame.image.save(surface, filename)


fill_mode = False
brush_size = 2
# кнопки
buttons = [
    Button(10, 10, 80, 40, "Brush", "brush"),
    Button(100, 10, 80, 40, "Rect", "rectangle"),
    Button(190, 10, 80, 40, "Circle", "circle"),
    Button(280, 10, 80, 40, "Square", "square"),
    Button(370, 10, 80, 40, "R.Tri", "right_triangle"),
    Button(460, 10, 80, 40, "E.Tri", "equilateral_triangle"),
    Button(550, 10, 80, 40, "Rhomb", "rhombus"),
    Button(640, 10, 80, 40, "Erase", "eraser"),
    Button(730, 10, 80, 40, "Line", "line"),
    Button(820, 10, 80, 40, "Togl Fill", "toggle_fill"),
    Button(910, 10, 80, 40, "Save", "save"),
    Button(1000, 10, 80, 40, "Small", "small_brush"),
    Button(1090, 10, 80, 40, "Medium", "medium_brush"),
    Button(1180, 10, 80, 40, "Large", "large_brush"),
    Button(1270, 10, 80, 40, "Filler", "flood_fill"),
    Button(1360, 10, 80, 40, "Text", "text"),
]
r, g, b = 0, 0, 255
slider_dragging = None
current_color = (r, g, b)
colored_pixels = []

running = True
preview_shape = None  # временная фигура

text_mode = False
text_input = ""
text_pos = None



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if text_mode:
                if event.key == pygame.K_RETURN:
                    if text_input.strip():
                        canvas.append(("text", text_pos, text_input, current_color))
                    text_mode = False
                    text_input = ""

                elif event.key == pygame.K_ESCAPE:
                    text_mode = False
                    text_input = ""

                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]

                else:
                    text_input += event.unicode
            else:
                if event.key == pygame.K_1:
                    brush_size = 2
                elif event.key == pygame.K_2:
                    brush_size = 5
                elif event.key == pygame.K_3:
                    brush_size = 10
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if current_tool == "text":
                if pos[1] > TOOLBAR_HEIGHT:
                    text_mode = True
                    text_pos = pos
                    text_input = ""
            # кнопки
            for btn in buttons:
                if btn.clicked(pos):
                    if btn.action == "toggle_fill":
                        fill_mode = not fill_mode
                    elif btn.action == "save":
                        save_canvas(screen)
                    elif btn.action == "small_brush":
                        brush_size = 2
                    elif btn.action == "medium_brush":
                        brush_size = 5
                    elif btn.action == "large_brush":
                        brush_size = 10
                    else:
                        current_tool = btn.action
            if current_tool == "flood_fill":
                changed_pixels = flood_fill(screen, pos, current_color)
                colored_pixels.extend(changed_pixels)
            mx, my = pos
            if 10 <= mx <= 210:
                if 80 <= my <= 90:
                    slider_dragging = "r"
                elif 110 <= my <= 120:
                    slider_dragging = "g"
                elif 140 <= my <= 150:
                    slider_dragging = "b"
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
                    canvas.append(("brush", start_pos, current_pos, current_color, fill_mode, brush_size))
                    start_pos = current_pos
                elif current_tool == "eraser":
                    canvas.append(("eraser", start_pos, current_pos, current_color, fill_mode, brush_size))
                    start_pos = current_pos
                else:
                    preview_shape = (current_tool, start_pos, current_pos, current_color, fill_mode, brush_size)

    screen.fill((255, 255, 255))
    for x, y, color in colored_pixels:
        screen.set_at((x, y), color)
    for item in canvas:
        if item[0] == "text":
            _, pos, text, color = item
            text_surface = font.render(text, True, color)
            screen.blit(text_surface, pos)
        else:
            draw_shape(screen, *item)
    if preview_shape:
        draw_shape(screen, *preview_shape)
    if text_mode:
        preview = font.render(text_input, True, current_color)
        screen.blit(preview, text_pos)
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