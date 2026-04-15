import pygame
import datetime

class MickeyClock:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.center = (self.width // 2, self.height // 2)
        self.image_back = pygame.image.load('images/mickey_base.png')
        self.image_s = pygame.image.load('images/mickey_hand.png')
        self.image_m = pygame.image.load('images/mickey_hand_m.png')
        self.image_back = pygame.transform.scale(self.image_back, (600, 600))
        self.image_s = pygame.transform.scale(self.image_s, (300, 300))
        self.image_m = pygame.transform.scale(self.image_m, (300, 300))
    def draw(self):
        now = datetime.datetime.now()
        seconds = now.second
        minutes = now.minute
        seconds_angle = -(seconds * 6)
        minutes_angle = -(minutes * 6)
        seconds_hand = pygame.transform.rotate(self.image_s, seconds_angle)
        minutes_hand = pygame.transform.rotate(self.image_m, minutes_angle)
        sec_rect = seconds_hand.get_rect(center=self.center)
        min_rect = minutes_hand.get_rect(center=self.center)
        self.screen.blit(self.image_back, (0, 0))
        self.screen.blit(minutes_hand, min_rect)
        self.screen.blit(seconds_hand, sec_rect)