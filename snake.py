# This game is developed by Shivam Srivastava.

# Importing The Modules
import pygame
import random
import os

# Initialization
pygame.mixer.init()
pygame.init()

# colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
yellow = (255,255,0)

# Creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Background image
bgimg = pygame.image.load("images/Snake-background.png")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()
gameover_img = pygame.image.load("images/Game-Over.png")
gameover_img = pygame.transform.scale(gameover_img, (screen_width, screen_height)).convert_alpha()
front_img = pygame.image.load("images/Snake-With-Shivam.png")
front_img = pygame.transform.scale(front_img, (screen_width, screen_height)).convert_alpha()

# Game Tittle
pygame.display.set_caption("Snake With Shivam")
pygame.display.update()

# Variables For The Game
clock = pygame.time.Clock()
font = pygame.font.SysFont('Times New Roman', 30)

# game music
pygame.mixer.music.load('music/back.mp3')
pygame.mixer.music.play(100)
pygame.mixer.music.pause()
pygame.mixer.music.set_volume(.6)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

def plot_snake(game_window, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(game_window, color, [x, y, snake_size, snake_size])

# Welcome Screen
def welcome():
    exit_game = False
    pygame.mixer.music.load('music/back.mp3')
    pygame.mixer.music.play(100)
    pygame.mixer.music.set_volume(.6)
    while not exit_game:
        gameWindow.fill((233, 220, 229))
        gameWindow.blit(front_img, (0, 0))
        # text_screen("Welcome to Snake Game", black, 220, 195)
        # text_screen("Press Space Bar to play", black, 230, 350)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # pygame.mixer.music.load('music/background.mp3')
                    pygame.mixer.music.load('music/back.mp3')
                    pygame.mixer.music.play(100)
                    pygame.mixer.music.set_volume(.6)
                    game_loop()
                if event.key == pygame.K_q:
                    exit_game = True

        pygame.display.update()
        clock.tick(60)

# Creating a Game loop
def game_loop():
    # Game specific variable
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1

    # High Score building
    if not os.path.exists("hiScore.txt"):
        with open("hiScore.txt", "w") as f:
            f.write("0")
    with open("hiScore.txt", "r") as f:
        hiScore = f.read()

    # Food Varibables
    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)

    # Game Variables
    score = 0
    init_velocity = 5
    snake_size = 30
    fps = 60

    while not exit_game:
        if game_over:
            with open("hiScore.txt", "w") as f:
                f.write(str(hiScore))

            # GameOverScreen
            gameWindow.fill((100, 100, 100))
            gameWindow.blit(gameover_img, (0, 0))
            # text_screen("Game Over!! Press enter to continue", red, 100, 200)
            text_screen(f"    Score: {str(score)}          High Score: {str(hiScore)}", white, 215, 400)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.stop()
                        welcome()
                    if event.key == pygame.K_s:
                        pygame.mixer.music.stop()
                    if event.key == pygame.K_p:
                        pygame.mixer.music.play()
                    if event.key == pygame.K_q:
                        exit_game = True

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_a:
                        score += 10
                    if event.key == pygame.K_s:
                        pygame.mixer.music.stop()
                    if event.key == pygame.K_p:
                        pygame.mixer.music.play()
                    if event.key == pygame.K_q:
                        exit_game = True
                    if event.key == pygame.K_BACKSPACE:
                        welcome()

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 8 and abs(snake_y - food_y) < 8:
                score += 10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length += 5
                if score > int(hiScore):
                    hiScore = score

            gameWindow.fill((250, 225, 230))
            gameWindow.blit(bgimg, (0, 0))
            text_screen(f"      Score: {str(score)}    High Score: {str(hiScore)}", yellow, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if (len(snk_list) > snk_length):
                del snk_list[0]

                if head in snk_list[:-1]:
                    game_over = True
                    pygame.mixer.music.load('music/game_over.mp3')
                    pygame.mixer.music.play()
                    pygame.mixer.music.set_volume(.6)
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load('music/game_over.mp3')
                pygame.mixer.music.play()
                pygame.mixer.music.set_volume(.6)

            plot_snake(gameWindow, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()
