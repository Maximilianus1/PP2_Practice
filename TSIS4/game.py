import pygame
import random
import time
import json
from db import save_result, get_best
from config import WIDTH, HEIGHT, CELL

def load_settings():
    with open("settings.json") as f:
        return json.load(f)


def run_game(screen, username):

    settings = load_settings()
    snake_color = settings["snake_color"]

    fps = pygame.time.Clock()

    snake_position = [100,50]
    snake_body = [[100,50],[90,50],[80,50]]

    fruit_position = [
        random.randrange(1,(WIDTH//CELL))*CELL,
        random.randrange(1,(HEIGHT//CELL))*CELL
    ]

    poison=None
    power=None
    shield=False

    direction="RIGHT"
    change_to=direction

    score=0
    level=1
    base_speed=5

    best = get_best(username)

    obstacles=[]
    fruit_types = [
        {"color": (255, 0, 0), "score": 5},
        {"color": (0, 0, 255), "score": 10},
        {"color": (255, 255, 255), "score": 15}
    ]
    fruit = random.choice(fruit_types)

    while True:

        for event in pygame.event.get():

            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

            if event.type==pygame.KEYDOWN:

                if event.key==pygame.K_UP:
                    change_to="UP"
                if event.key==pygame.K_DOWN:
                    change_to="DOWN"
                if event.key==pygame.K_LEFT:
                    change_to="LEFT"
                if event.key==pygame.K_RIGHT:
                    change_to="RIGHT"

        if change_to=="UP" and direction!="DOWN":
            direction="UP"
        if change_to=="DOWN" and direction!="UP":
            direction="DOWN"
        if change_to=="LEFT" and direction!="RIGHT":
            direction="LEFT"
        if change_to=="RIGHT" and direction!="LEFT":
            direction="RIGHT"

        if direction=="UP":
            snake_position[1]-=CELL
        if direction=="DOWN":
            snake_position[1]+=CELL
        if direction=="LEFT":
            snake_position[0]-=CELL
        if direction=="RIGHT":
            snake_position[0]+=CELL

        snake_body.insert(0,list(snake_position))

        if snake_position==fruit_position:
            score += fruit["score"]
            fruit = random.choice(fruit_types)
            fruit_position=[
                random.randrange(1,(WIDTH//CELL))*CELL,
                random.randrange(1,(HEIGHT//CELL))*CELL
            ]
        else:
            snake_body.pop()
        if power:
            if pygame.time.get_ticks() - power["time"] > 8000:
                power = None
        level = score//30 + 1
        base_speed = 5 + level*5

        if level>=3 and len(obstacles)<level:
            obstacles.append([
                random.randrange(1,(WIDTH//CELL))*CELL,
                random.randrange(1,(HEIGHT//CELL))*CELL
            ])

        if random.randint(1,200)==1:
            poison=[
                random.randrange(1,(WIDTH//CELL))*CELL,
                random.randrange(1,(HEIGHT//CELL))*CELL
            ]

        if poison and snake_position==poison:
            snake_body=snake_body[:-2]
            poison=None
            if len(snake_body)<=1:
                break

        if random.randint(1,300)==1:
            power={
                "pos":[
                    random.randrange(1,(WIDTH//CELL))*CELL,
                    random.randrange(1,(HEIGHT//CELL))*CELL
                ],
                "type":random.choice(["speed","slow","shield"]),
                "time":pygame.time.get_ticks()
            }

        if power and snake_position==power["pos"]:
            if power["type"] == "speed":
                base_speed += 5
            if power["type"] == "slow":
                base_speed = max(3, base_speed - 3)
            if power["type"]=="shield":
                shield=True

            power=None

        if snake_position[0]<0 or snake_position[0]>WIDTH-CELL:
            if shield:
                shield=False
            else:
                save_result(username, score, level)
                return

        if snake_position[1]<0 or snake_position[1]>HEIGHT-CELL:
            if shield:
                shield=False
            else:
                save_result(username, score, level)
                return

        for block in snake_body[1:]:
            if snake_position==block:
                if shield:
                    shield=False
                else:
                    save_result(username, score, level)
                    return

        for o in obstacles:
            if snake_position == o:
                save_result(username, score, level)
                return

        screen.fill((0,0,0))

        for pos in snake_body:
            pygame.draw.rect(
                screen,
                snake_color,
                pygame.Rect(pos[0],pos[1],CELL,CELL)
            )

        pygame.draw.rect(
            screen,
            fruit["color"],
            pygame.Rect(fruit_position[0], fruit_position[1], CELL, CELL)
        )

        if poison:
            pygame.draw.rect(
                screen,
                (150,0,0),
                pygame.Rect(poison[0],poison[1],CELL,CELL)
            )

        if power:
            color={
                "speed":(0,255,255),
                "slow":(255,255,0),
                "shield":(255,0,255)
            }[power["type"]]

            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(power["pos"][0],power["pos"][1],CELL,CELL)
            )

        for o in obstacles:
            pygame.draw.rect(
                screen,
                (100,100,100),
                pygame.Rect(o[0],o[1],CELL,CELL)
            )

        font=pygame.font.SysFont(None,30)

        screen.blit(font.render(f"Score: {score}",True,(255,255,255)),(10,10))
        screen.blit(font.render(f"Level: {level}",True,(255,255,255)),(10,40))
        screen.blit(font.render(f"Best: {best}",True,(255,255,255)),(10,70))

        pygame.display.flip()
        fps.tick(base_speed)

    save_result(username, score, level)