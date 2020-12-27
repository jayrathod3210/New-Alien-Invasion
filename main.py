import pygame
import random
import sys
import math
from pygame import mixer
import os

# Initialization pygame
pygame.init()

# create screen

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 750

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bigfont = pygame.font.Font(None, 80)
smallfont = pygame.font.Font(None, 45)

# Title and Icon
pygame.display.set_caption('Alien Invasion')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# background Image
background = pygame.image.load('main_background.jpg')

# background Music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Player
playerImg = pygame.image.load('space-invaders .png')
playerX = 470
playerY = 610
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

number_of_enemies = 15
for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load('space-enemy.png'))
    enemyX.append(random.randint(0, 1027))
    enemyY.append(random.randint(140, 230))
    enemyX_change.append(3)
    enemyY_change.append(40)

# bullet
# Ready - you can't see bullet on screen
# Fire - the bullet currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 610
bulletX_change = 0
bulletY_change = 5
bullet_state = 'ready'

# score

score_value = 0
font = pygame.font.Font('Hardigan.otf', 32)

textX = 10
testY = 10

# game over
over_font = pygame.font.Font('Hardigan.otf', 70)

# staring def function
# first page to play game page

play_background = pygame.image.load('background.jpg')


def play_game():
    text = bigfont.render('PLAY', ' ', 13, (255, 255, 255))
    textx = SCREEN_WIDTH / 2 - text.get_width() / 2
    texty = SCREEN_HEIGHT / 2 - text.get_height() / 2
    textx_size = text.get_width()
    texty_size = text.get_height()
    pygame.draw.rect(screen, (255, 255, 255), ((textx - 5, texty - 5),
                                               (textx_size + 10, texty_size +
                                                10)))
    screen.blit(play_background, (0, 0))
    screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2,
                       SCREEN_HEIGHT / 2 - text.get_height() / 2))

    pygame.display.flip()
    in_main_menu = True
    while in_main_menu:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_main_menu = False
                pygame.display.quit()
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if x >= textx - 5 and x <= textx + textx_size + 5:
                    if y >= texty - 5 and y <= texty + texty_size + 5:
                        in_main_menu = False
                        break
play_game()

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 6))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2))
    if distance < 32:
        return True
    else:
        return False


def show_score(x, y):
    score = font.render('score:' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render('GAME OVER ', '', True, (255, 255, 255))
    screen.blit(over_text, (370, 250))


def Quit():
    text = bigfont.render('Quit', 13, (0, 0, 0))
    textx = SCREEN_WIDTH / 2 - text.get_width() / 2
    texty = SCREEN_HEIGHT / 2 - text.get_height() / 2
    textx_size = text.get_width()
    texty_size = text.get_height()
    pygame.draw.rect(screen, (255, 255, 255), ((textx - 5, texty - 5),
                                               (textx_size + 10, texty_size +
                                                10)))

    screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2,
                       SCREEN_HEIGHT / 2 - text.get_height() / 2))


    pygame.display.flip()
    in_main_menu = True
    while in_main_menu:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_main_menu = False
                pygame.display.quit()
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if x >= textx - 5 and x <= textx + textx_size + 5:
                    if y >= texty - 5 and y <= texty + texty_size + 5:
                        in_main_menu = False



# Game loop

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If key stroke is pressed check whether its left or right

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                play_game()

            if event.key == pygame.K_LEFT:
                playerX_change -= 2

            if event.key == pygame.K_RIGHT:
                playerX_change += 2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    # Get the current x co_ordinate of spaceship
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            playerX_change = 0

    # RGB red,green,blue
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # player movement

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    if playerX >= 1030:
        playerX = 1030

    # Enemy movement

    for i in range(number_of_enemies):

        # Game over
        if enemyY[i] > 588:
            for j in range(number_of_enemies):
                enemyY[j] = 2000

            game_over_text()
            show_score(textX, testY)
            Quit()
            pygame.quit()
            quit()

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1.9
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 1027:
            enemyX_change[i] = -1.9
            enemyY[i] += enemyY_change[i]

        # Collision

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()

            bulletY = 610
            bullet_state = 'ready'
            score_value += 2

            enemyX[i] = random.randint(0, 1027)
            enemyY[i] = random.randint(40, 130)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 610
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Update of screen
    player(playerX, playerY)
    show_score(textX, testY)

    pygame.display.update()
