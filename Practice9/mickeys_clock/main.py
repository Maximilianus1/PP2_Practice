import pygame
from clock import MickeyClock

pygame.init()

size = width, height = 600, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Mickey Clock")
clock = pygame.time.Clock()
mickey_clock = MickeyClock(screen)
running = False
while not running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = True
    screen.fill((0, 0, 0))
    mickey_clock.draw()
    pygame.display.flip()
    clock.tick(1)