import pygame
import sys
from game import run_game
from db import get_top10, init_db
import json

pygame.init()
init_db()
WIDTH = 720
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 40)

state = "menu"
username = ""


def draw_menu():
    screen.fill((0,0,0))

    title = font.render("SNAKE", True, (255,255,255))
    screen.blit(title,(300,50))

    screen.blit(font.render("1 - Play",True,(255,255,255)),(300,150))
    screen.blit(font.render("2 - Leaderboard",True,(255,255,255)),(300,200))
    screen.blit(font.render("3 - Settings",True,(255,255,255)),(300,250))
    screen.blit(font.render("ESC - Quit",True,(255,255,255)),(300,300))


def draw_leaderboard():
    screen.fill((0,0,0))

    data = get_top10()

    y=50
    for i,row in enumerate(data):
        text=f"{i+1}. {row[0]}  {row[1]} lvl:{row[2]}"
        screen.blit(font.render(text,True,(255,255,255)),(100,y))
        y+=40


while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if state=="menu":

                if event.key==pygame.K_1:
                    state="username"

                if event.key==pygame.K_2:
                    state="leaderboard"
                if event.key == pygame.K_3:
                    state = "settings"

                if event.key==pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif state=="username":

                if event.key==pygame.K_RETURN:
                    run_game(screen, username)
                    state="menu"

                elif event.key==pygame.K_BACKSPACE:
                    username=username[:-1]

                else:
                    username+=event.unicode

            elif state=="leaderboard":

                if event.key==pygame.K_ESCAPE:
                    state="menu"


    if state=="menu":
        draw_menu()

    elif state=="leaderboard":
        draw_leaderboard()

    elif state=="username":
        screen.fill((0,0,0))
        text = font.render("Enter username:",True,(255,255,255))
        screen.blit(text,(200,150))
        name = font.render(username,True,(255,255,255))
        screen.blit(name,(200,200))

    pygame.display.flip()