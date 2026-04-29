import pygame, random, time
from persistence import add_score, load_settings

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

class Game:

    def __init__(self, screen, username):

        self.screen = screen
        self.username = username

        self.speed = 5
        self.score = 0
        self.coins = 0
        self.distance = 0

        settings = load_settings()

        self.sound = settings["sound"]
        self.difficulty = settings["difficulty"]
        self.car_color = settings["car_color"]
        if self.difficulty == "easy":
            self.speed = 4

        elif self.difficulty == "normal":
            self.speed = 6

        elif self.difficulty == "hard":
            self.speed = 8
        self.active_power = None
        self.power_timer = 0
        self.shield = False

        self.background = pygame.image.load("assets/AnimatedStreet.png")

        self.player = Player(self.car_color)
        self.enemies = pygame.sprite.Group()
        self.coins_g = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()

        self.enemies.add(Enemy())

        self.font = pygame.font.SysFont("Verdana",20)

    def run(self):

        clock = pygame.time.Clock()

        SPAWN_COIN = pygame.USEREVENT+1
        SPAWN_POWER = pygame.USEREVENT+2
        SPAWN_OBS = pygame.USEREVENT+3

        pygame.time.set_timer(SPAWN_COIN,1500)
        pygame.time.set_timer(SPAWN_POWER,5000)
        pygame.time.set_timer(SPAWN_OBS,2000)

        while True:

            for e in pygame.event.get():

                if e.type == pygame.QUIT:
                    return

                if e.type == SPAWN_COIN:
                    self.coins_g.add(Coin())

                if e.type == SPAWN_POWER:
                    self.powerups.add(Power())

                if e.type == SPAWN_OBS:
                    self.obstacles.add(Obstacle())

            self.screen.blit(self.background,(0,0))

            self.player.move()

            for g in [self.enemies,self.coins_g,self.powerups,self.obstacles]:
                for obj in g:
                    obj.move(self.speed)
                    self.screen.blit(obj.image,obj.rect)

            self.screen.blit(self.player.image,self.player.rect)

            self.check_collisions()
            self.update_power()
            self.draw_ui()

            pygame.display.update()
            clock.tick(60)

    def check_collisions(self):

        # coins
        for c in pygame.sprite.spritecollide(self.player, self.coins_g, True):
            self.coins += c.value
        for p in pygame.sprite.spritecollide(self.player, self.powerups, True):

            self.active_power = p.type
            self.power_timer = pygame.time.get_ticks()

            if p.type == "shield":
                self.shield = True

            if p.type == "nitro":
                self.speed *= 2

            if p.type == "repair":
                self.score += 5
        if pygame.sprite.spritecollideany(self.player, self.enemies):

            if self.shield:
                self.shield = False
            else:
                self.game_over()
        if pygame.sprite.spritecollideany(self.player, self.obstacles):

            if self.shield:
                self.shield = False
            else:
                self.game_over()

    def update_power(self):

        if self.active_power=="nitro":
            if pygame.time.get_ticks()-self.power_timer>4000:
                self.speed/=2
                self.active_power=None

        self.distance+=self.speed*0.1
        self.score=self.coins*10+int(self.distance)

    def draw_ui(self):

        t1=self.font.render(f"Score:{self.score}",True,(0,0,0))
        t2=self.font.render(f"Coins:{self.coins}",True,(0,0,0))
        t3=self.font.render(f"Dist:{int(self.distance)}",True,(0,0,0))

        self.screen.blit(t1,(10,10))
        self.screen.blit(t2,(10,30))
        self.screen.blit(t3,(10,50))

        if self.active_power:
            t4=self.font.render(self.active_power,True,(255,0,0))
            self.screen.blit(t4,(250,10))

    def game_over(self):

        add_score(self.username,self.score,int(self.distance))

        pygame.time.delay(1500)
        raise SystemExit



class Player(pygame.sprite.Sprite):

    def __init__(self, color="red"):
        super().__init__()

        self.image=pygame.image.load(f"assets/player_{color}.png")
        self.image=pygame.transform.scale(self.image,(30,60))
        self.rect=self.image.get_rect(center=(200,500))

    def move(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: self.rect.x-=5
        if keys[pygame.K_RIGHT]: self.rect.x+=5
        if keys[pygame.K_UP]: self.rect.y-=5
        if keys[pygame.K_DOWN]: self.rect.y+=5


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("assets/Enemy.png")
        self.image=pygame.transform.scale(self.image,(30,60))
        self.rect=self.image.get_rect(center=(random.randint(40,360),-60))

    def move(self,speed):
        self.rect.y+=speed

        if self.rect.top>600:
            self.rect.center=(random.randint(40,360),-60)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.value=random.randint(1,5)
        self.image=pygame.image.load("assets/coin.png")
        self.image=pygame.transform.scale(self.image,(25,25))
        self.rect=self.image.get_rect(center=(random.randint(40,360),0))

    def move(self,speed):
        self.rect.y+=speed


class Power(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.type=random.choice(["nitro","shield","repair"])

        self.image=pygame.image.load(f"assets/{self.type}.png")
        self.image=pygame.transform.scale(self.image,(30,30))
        self.rect=self.image.get_rect(center=(random.randint(40,360),0))

    def move(self,speed):
        self.rect.y+=speed


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        img=random.choice(["oil_spill","traffic_car","speed_bump"])
        self.image=pygame.image.load(f"assets/{img}.png")
        self.image=pygame.transform.scale(self.image,(30,30))
        self.rect=self.image.get_rect(center=(random.randint(40,360),0))

    def move(self,speed):
        self.rect.y+=speed