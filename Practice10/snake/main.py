import pygame, sys
from pygame.locals import *
import random, time

pygame.init()
FPS = 60
FramePerSec = pygame.time.Clock()
# Predefined some colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# Screen information
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
SPEED = 5
SCORE = 0
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, WHITE)

background = pygame.image.load("AnimatedStreet.png")

COINS = 0
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.image = pygame.transform.scale(self.image,(25,50))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.image = pygame.transform.scale(self.image, (25, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Random coin value (weight)
        self.value = random.randint(1,5)
        self.image = pygame.image.load("coin.png")
        self.image = pygame.transform.scale(self.image, (25, 25))

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)

        # Remove coin if it leaves screen
        if (self.rect.top > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

P1 = Player()
E1 = Enemy()
enemies = pygame.sprite.Group()
enemies.add(E1)
coins =pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

#Adding a new User event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Increase speed over time
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Spawn coins randomly
SPAWN_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_COIN, 1500)
while True:
    # Cycles through all events occurring
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.2
        if event.type == SPAWN_COIN:
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    coins_text = font_small.render(f"Coins: {COINS}", True, BLACK)
    DISPLAYSURF.blit(coins_text, (280, 10))

    # Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    collected = pygame.sprite.spritecollide(P1, coins, True)
    for coin in collected:
        COINS += coin.value

        # Increase difficulty every N coins
        if COINS % 5 == 0:
            SPEED += 1

    # To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.mp3').play()
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)