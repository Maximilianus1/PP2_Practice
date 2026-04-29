import pygame
from persistence import load_leaderboard, save_settings, load_settings

WHITE = (255,255,255)
BLACK = (0,0,0)

def settings_screen(screen):

    settings = load_settings()

    while True:

        screen.fill((0,0,0))

        font = pygame.font.SysFont("Verdana",20)

        # TEXT
        sound = font.render(f"Sound: {settings['sound']}", True, WHITE)
        diff = font.render(f"Difficulty: {settings['difficulty']}", True, WHITE)
        car = font.render(f"Car color: {settings['car_color']}", True, WHITE)

        screen.blit(sound,(120,200))
        screen.blit(diff,(120,250))
        screen.blit(car,(120,300))

        back = button(screen,"BACK",120,400,160,40)

        pygame.display.update()

        for e in pygame.event.get():

            if e.type == pygame.QUIT:
                return

            if e.type == pygame.MOUSEBUTTONDOWN:

                x,y = e.pos

                # toggle sound
                if 120 < x < 280 and 200 < y < 230:
                    settings["sound"] = not settings["sound"]

                # difficulty
                if 120 < x < 280 and 250 < y < 280:

                    if settings["difficulty"] == "easy":
                        settings["difficulty"] = "normal"

                    elif settings["difficulty"] == "normal":
                        settings["difficulty"] = "hard"

                    else:
                        settings["difficulty"] = "easy"

                # car color
                if 120 < x < 280 and 300 < y < 330:

                    if settings["car_color"] == "red":
                        settings["car_color"] = "blue"

                    elif settings["car_color"] == "blue":
                        settings["car_color"] = "green"

                    else:
                        settings["car_color"] = "red"

                if back.collidepoint(e.pos):
                    save_settings(settings)
                    return
def draw_text(screen, text, size, x, y):
    font = pygame.font.SysFont("Verdana", size)
    render = font.render(text, True, WHITE)
    rect = render.get_rect(center=(x,y))
    screen.blit(render, rect)

def button(screen, text, x, y, w, h):
    rect = pygame.Rect(x,y,w,h)
    pygame.draw.rect(screen, (50,50,50), rect)
    draw_text(screen,text,20,x+w//2,y+h//2)
    return rect

def main_menu(screen):
    while True:
        screen.fill((0,0,0))

        play = button(screen,"PLAY",120,200,160,40)
        lead = button(screen,"LEADERBOARD",120,260,160,40)
        sett = button(screen,"SETTINGS",120,320,160,40)
        quitb = button(screen,"QUIT",120,380,160,40)

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"

            if e.type == pygame.MOUSEBUTTONDOWN:
                if play.collidepoint(e.pos): return "play"
                if lead.collidepoint(e.pos): return "leader"
                if sett.collidepoint(e.pos): return "settings"
                if quitb.collidepoint(e.pos): return "quit"


def leaderboard_screen(screen):
    data = load_leaderboard()

    while True:
        screen.fill((0,0,0))
        draw_text(screen,"LEADERBOARD",30,200,60)

        y = 120
        for i,d in enumerate(data):
            txt = f"{i+1}. {d['name']}  {d['score']}  {d['distance']}"
            draw_text(screen,txt,18,200,y)
            y+=30

        back = button(screen,"BACK",120,500,160,40)
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.MOUSEBUTTONDOWN:
                if back.collidepoint(e.pos):
                    return