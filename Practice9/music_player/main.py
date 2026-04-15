import pygame
from player import MusicPlayer

pygame.init()

size = width, height = 600, 400
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Music Player")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
player = MusicPlayer()
running = True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_p:
                player.play()
            elif event.key==pygame.K_s:
                player.stop()
            elif event.key==pygame.K_n:
                player.next()
            elif event.key==pygame.K_b:
                player.previous()
            elif event.key==pygame.K_q:
                running=False
    screen.fill((200, 230, 255))
    track_text = font.render(
        f"Track: {player.get_current_track()}",
        True,
        (0, 70, 140)
    )
    pos_seconds = player.get_position() // 1000
    time_text = font.render(
        f"Position: {pos_seconds}s",
        True,
        (50, 120, 200)
    )
    controls_text = font.render(
        "P=Play S=Stop N=Next B=Back Q=Quit",
        True,
        (80, 100, 140)
    )
    screen.blit(track_text, (50, 100))
    screen.blit(time_text, (50, 150))
    screen.blit(controls_text, (50, 250))
    pygame.display.flip()
    clock.tick(30)
pygame.quit()