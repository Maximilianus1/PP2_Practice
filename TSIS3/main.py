import pygame
from ui import main_menu, leaderboard_screen, settings_screen
from racer import Game

pygame.init()
screen = pygame.display.set_mode((400,600))
pygame.display.set_caption("Racer")

def get_name():

    name=""
    font=pygame.font.SysFont("Verdana",30)

    while True:
        screen.fill((0,0,0))

        txt=font.render("Enter Name:"+name,True,(255,255,255))
        screen.blit(txt,(50,300))

        pygame.display.update()

        for e in pygame.event.get():

            if e.type==pygame.QUIT:
                return "Player"

            if e.type==pygame.KEYDOWN:

                if e.key==pygame.K_RETURN:
                    return name

                elif e.key==pygame.K_BACKSPACE:
                    name=name[:-1]

                else:
                    name+=e.unicode


while True:

    action = main_menu(screen)

    if action=="quit":
        break

    if action=="leader":
        leaderboard_screen(screen)
    if action == "settings":
        settings_screen(screen)
    if action=="play":
        name=get_name()
        Game(screen,name).run()