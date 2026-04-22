# importing libraries
import pygame
import time
import random
snake_speed = 5
# Window size
window_x = 720
window_y = 480

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialising pygame
pygame.init()
level=1
fruit_count=0
# Initialise game window
pygame.display.set_caption('Snake')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# defining snake default position
snake_position = [100, 50]

# defining first 4 blocks of snake body
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]
              ]
# fruit position
fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                  random.randrange(1, (window_y // 10)) * 10]

fruit_spawn = True
purple_fruit_position = [0, 0]
purple_fruit_spawn = False
purple_fruit_start_time = 0
purple_fruit_duration = random.randint(10, 20)
# setting default snake direction towards
# right
direction = 'RIGHT'
change_to = direction

# initial score
score = 0


# displaying Score function
def show_text(choice, color, value, font,pos, size):
    # creating font object score_font
    text_font = pygame.font.SysFont(font, size)

    # create the display surface object
    # score_surface
    text_surface = text_font.render(f'{choice} : {str(value)}', True, color)
    # create a rectangular object for the text
    # surface object
    text_rect = text_surface.get_rect()
    text_rect.midtop=(pos,10)
    # displaying text
    game_window.blit(text_surface, text_rect)


# game over function
def game_over():
    # creating font object my_font
    my_font = pygame.font.SysFont('times new roman', 50)

    # creating a text surface on which text
    # will be drawn
    game_over_surface = my_font.render(f'Game Over; Score : {str(score)}', True, red)

    # create a rectangular object for the text
    # surface object
    game_over_rect = game_over_surface.get_rect()

    # setting position of the text
    game_over_rect.midtop = (window_x / 2, window_y / 4)

    # blit will draw the text on screen
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    # after 2 seconds we will quit the program
    time.sleep(2)

    # deactivating pygame library
    pygame.quit()

    # quit the program
    quit()


# Main Function
while True:

    # handling key events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # If two keys pressed simultaneously
    # we don't want snake to move into two
    # directions simultaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10
    # Snake body growing mechanism
    snake_body.insert(0, list(snake_position))
    ate=False
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += random.choice([5,10,15])
        fruit_count+=1
        fruit_spawn = False
        ate=True
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                          random.randrange(1, (window_y // 10)) * 10]

    if snake_position[0] == purple_fruit_position[0] and snake_position[1] == purple_fruit_position[1]:
        score += 25
        fruit_count += 1
        purple_fruit_spawn = False
        ate=True
    if not ate:
        snake_body.pop()

    fruit_spawn = True
    current_time = time.time()

    # Random chance to spawn purple fruit
    if not purple_fruit_spawn and random.randint(1, 200) == 1:
        while True:
            new_pos = [random.randrange(1, (window_x // 10)) * 10,
                       random.randrange(1, (window_y // 10)) * 10]
            if new_pos not in snake_body:
                purple_fruit_position = new_pos
                break

        purple_fruit_spawn = True
        purple_fruit_start_time = current_time
        purple_fruit_duration = random.randint(10, 20)

    if purple_fruit_spawn and current_time - purple_fruit_start_time > purple_fruit_duration:
        purple_fruit_spawn = False

    game_window.fill(black)
    level=fruit_count//3+1
    snake_speed=5*level
    for pos in snake_body:
        pygame.draw.rect(game_window, green,
                         pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, red, pygame.Rect(
        fruit_position[0], fruit_position[1], 10, 10))
    if purple_fruit_spawn:
        pygame.draw.rect(game_window, pygame.Color(255, 0, 255),
                         pygame.Rect(purple_fruit_position[0], purple_fruit_position[1], 10, 10))

    # Game Over conditions
    if snake_position[0] < 0 or snake_position[0] > window_x - 10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y - 10:
        game_over()

    # Touching the snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    # displaying score continuously
    show_text("Score", white,score, 'times new roman',100, 20)
    show_text("Level", white, level, 'times new roman', window_x-100, 20)
    # Refresh game screen
    pygame.display.flip()

    # Frame Per Second /Refresh Rate
    fps.tick(snake_speed)