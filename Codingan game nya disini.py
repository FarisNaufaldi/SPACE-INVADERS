import random
import math

import pygame
from pygame import mixer


pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('.vscode/spaceship.png')
pygame.display.set_icon(icon)

background = pygame.image.load('.vscode/starry-night-sky.jpg')

mixer.music.load('.vscode/background.wav')
mixer.music.play(-1)


playerImg = pygame.image.load('.vscode/001-spaceship.png')
playerX = 360
playerY = 480
playerX_change = 0

num_of_enemies = 7

# Daftar gambar musuh yang berbeda
enemyImgs = [
    pygame.image.load('.vscode/2.png'),
    pygame.image.load('.vscode/001-alien.png'),
    pygame.image.load('.vscode/001-alien2.png')
]

# Inisialisasi daftar untuk musuh
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

for i in range(num_of_enemies):
    # Pilih gambar musuh secara acak dari daftar
    selected_enemy_img = random.choice(enemyImgs)
    enemyImg.append(selected_enemy_img)
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1.5)
    enemyY_change.append(70)

bulletImg = pygame.image.load('.vscode/bullet (1).png')
bulletX = 0
bulletY = 480
bulletY_change = 3.5
bullet_state = "ready"

#Skor permainan

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# ... (Bagian kodingan sebelumnya)
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200, 250))
   

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX,2)) + (math.pow(enemyY - bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

# Loop utama permainan
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ... (Bagian kodingan untuk menggerakkan pemain, menembakkan peluru, dsb.)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                playerX_change = -2.5
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerX_change = 2.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('.vscode/laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):
        # Cek kondisi Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            gameover_Sound = mixer.Sound('.vscode/mixkit-arcade-retro-game-over-213.wav')
            gameover_Sound.play(-1)
            mixer.music.stop()
            game_over_text()
            break

        # Gerakkan musuh
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        # Deteksi Collision dan tindakan setelah Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('.vscode/explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            enemyImg[i] = random.choice(enemyImgs)  # Pilih gambar musuh baru secara acak

        enemy(enemyX[i], enemyY[i], i)

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()