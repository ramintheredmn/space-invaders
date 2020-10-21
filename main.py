#  space-invaders by Redmn(Ramin Rafiee)

import pygame
import random
from pygame import mixer
# initialition
pygame.init()
pygame.mixer.init()
# screen
screen = pygame.display.set_mode((800, 600))
# tilte
pygame.display.set_caption("Space invaders")

# background

bg = pygame.image.load("247.png")

# background song
pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1)

# score

score_valu = 0
redmnFont = pygame.font.Font('god.ttf', 25)
font = pygame.font.Font('god.ttf', 32)
texX = 10
texY = 10

# player

palyerimg = pygame.image.load("space-invaders.png")
playerx = 370
playery = 480
playerx_change = 0
# enemy List - every time the loop finishes an enemy goes here - visit line 47
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []

enemy_number = 6
# game over

over_font = pygame.font.Font('freesansbold.ttf', 70)
# enemy adding loop
for i in range(enemy_number):
    enemyimg.append(pygame.image.load("planet.png"))
    enemyx.append(random.randint(0, 735))
    enemyy.append(random.randint(30, 140))
    enemyx_change.append(6)
    enemyy_change.append(50)
# bullet - 0 > in this state bullet is in the ready mode and not shown on the screen | 1 > fire
bulletimg = pygame.image.load("bullet.png")
bulletx = 370
bullety = 480
bullety_change = 8
bullet_state = 0
# defining functions
# score and about
def showScore(x, y):
    score = font.render("Score : " + str(score_valu), True, (255, 255, 255))
    redmn = redmnFont.render("Space invaders by 'Ramin Rafiee'", True, (255, 51, 51))
    screen.blit(redmn, (250, 10))
    screen.blit(score, (x, y))

# game over func
def over():
    overimg = over_font.render(" GAME OVER ", True, (255, 255, 255))
    screen.blit(overimg, (180, 250))
    pygame.mixer.music.stop()


# the space
def player(x, y):
    screen.blit(palyerimg, (x, y))

# enemies
def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

# bullet - sets bullet mode to fire that can appeare on the screen
def bullet(x, y):
    global bullet_state
    bullet_state = 1
    screen.blit(bulletimg, (x + 16, y + 10))

# check if our bullet touched the enemies and save it in a bool | I used 'distance between two points' that we learned at school - (فاصله بین دو نقطه) -
# ریشه دوم مجموع مربعات تفاضل ایکس و ایگرگ دو شی
# I wanted not to use other libs and work with python built-in operators
# u can have this instead :
# import math
# math.sqrt(math.pow((enemyx - bulletx), 2) + math.pow((enemyy - bullety), 2))
def isColission(enemyx, enemyy, bulletx, bullety):
    distance = (((enemyx - bulletx) ** 2) + ((enemyy - bullety) ** 2)) ** (1 / 2)
    if distance < 27:
        return True
    else:
        return False


# game loop
runing = True
while runing:
    # RGB     red  green blue
    screen.fill((0, 0, 0))
    # background
    screen.blit(bg, (0, 0))
    # stop program when pressed exit
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            runing = False

        # if key stroke is pressed check whether its left or right
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_LEFT:
                playerx_change = -8
            if ev.key == pygame.K_RIGHT:
                playerx_change = 8
            if ev.key == pygame.K_SPACE:
                # check if bullet is on the screen
                if bullet_state == 0:
                    b_s = mixer.Sound('laser.wav')
                    b_s.play()
                    # get the space ship x value
                    bulletx = playerx
                    bullet(bulletx, bullety)
        # check in key is realesd
        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_LEFT or ev.key == pygame.K_RIGHT:
                playerx_change = 0

    playerx += playerx_change

    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736
    for i in range(enemy_number):
        # game over

        if enemyy[i] > 450:

            for j in range(enemy_number):
                enemyy[j] = 2000

            over()

            break

        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 0:
            enemyx[i] = 0
            enemyx_change[i] = 4
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx[i] = 736
            enemyy[i] += enemyy_change[i]
            enemyx_change[i] = -4
        collission = isColission(enemyx[i], enemyy[i], bulletx, bullety)
        if collission:
            e_s = mixer.Sound('explosion.wav')
            e_s.play()
            bullety = 480
            bullet_state = 0
            score_valu += 1

            enemyx[i] = random.randint(0, 800)
            enemyy[i] = random.randint(30, 140)

        enemy(enemyx[i], enemyy[i], i)

    if bullety <= 0:
        bullety = 480
        bullet_state = 0
    if bullet_state == 1:
        bullet(bulletx, bullety)
        bullety -= bullety_change
    #
    player(playerx, playery)
    showScore(texX, texY)
    #updates the screen
    pygame.display.update()
