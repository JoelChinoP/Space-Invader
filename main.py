import math
import random
import pygame
from pygame import mixer

# Initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (800, 600))

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space Invaders - 2 Players")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player 1
playerImg = pygame.image.load('player.png')
playerX = 320
playerY = 480
playerX_change = 0

# Player 2 - NUEVO
player2Img = pygame.image.load('player.png')
player2X = 420  # Posición inicial diferente
player2Y = 520  # Más abajo que jugador 1
player2X_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 8  # Más enemigos para 2 jugadores

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1.5)  # Enemigos más rápidos
    enemyY_change.append(40)

# Bullet Player 1
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Bullet Player 2 - NUEVO
bullet2Img = pygame.image.load('bullet.png')
bullet2X = 0
bullet2Y = 520
bullet2X_change = 0
bullet2Y_change = 10
bullet2_state = "ready"

# Scores - MODIFICADO para 2 jugadores
score_value = 0
score2_value = 0  # NUEVO: Puntuación jugador 2
font = pygame.font.Font('freesansbold.ttf', 28)  # Fuente más pequeña
textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

# NUEVA función para mostrar ambas puntuaciones
def show_scores():
    score1 = font.render("P1: " + str(score_value), True, (0, 255, 0))
    score2 = font.render("P2: " + str(score2_value), True, (0, 255, 255))
    screen.blit(score1, (10, 10))
    screen.blit(score2, (10, 45))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))
    # Mostrar puntuaciones finales
    final1 = font.render("Player 1 Final Score: " + str(score_value), True, (0, 255, 0))
    final2 = font.render("Player 2 Final Score: " + str(score2_value), True, (0, 255, 255))
    screen.blit(final1, (200, 320))
    screen.blit(final2, (200, 350))

def player(x, y):
    screen.blit(playerImg, (x, y))

# NUEVA función para jugador 2
def player2(x, y):
    screen.blit(player2Img, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# NUEVA función para bala del jugador 2
def fire_bullet2(x, y):
    global bullet2_state
    bullet2_state = "fire"
    screen.blit(bullet2Img, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # CONTROLES MODIFICADOS - Ambos jugadores
        if event.type == pygame.KEYDOWN:
            # Player 1 controls - Flechas y ESPACIO
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            
            # Player 2 controls - A/D y SHIFT IZQUIERDO
            if event.key == pygame.K_a:
                player2X_change = -5
            if event.key == pygame.K_d:
                player2X_change = 5
            if event.key == pygame.K_LSHIFT:
                if bullet2_state == "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bullet2X = player2X
                    fire_bullet2(bullet2X, bullet2Y)

        if event.type == pygame.KEYUP:
            # Player 1
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            # Player 2
            if event.key == pygame.K_a or event.key == pygame.K_d:
                player2X_change = 0

    # LÍMITES MODIFICADOS - Para ambos jugadores
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    player2X += player2X_change
    if player2X <= 0:
        player2X = 0
    elif player2X >= 736:
        player2X = 736

    # Enemy movement
    for i in range(num_of_enemies):
        # Game Over - Si cualquier enemigo llega muy abajo
        if enemyY[i] > 400:  # Condición más estricta por tener 2 jugadores
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1.5
            enemyY[i] += enemyY_change[i]

        # COLISIONES MODIFICADAS - Para ambos jugadores
        collision1 = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        collision2 = isCollision(enemyX[i], enemyY[i], bullet2X, bullet2Y)
        
        if collision1:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1  # Puntos para jugador 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        
        elif collision2:  # elif para evitar doble colisión
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bullet2Y = 520
            bullet2_state = "ready"
            score2_value += 1  # Puntos para jugador 2
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # MOVIMIENTO DE BALAS MODIFICADO - Para ambas balas
    # Bullet 1 movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Bullet 2 movement
    if bullet2Y <= 0:
        bullet2Y = 520
        bullet2_state = "ready"
    if bullet2_state == "fire":
        fire_bullet2(bullet2X, bullet2Y)
        bullet2Y -= bullet2Y_change

    # RENDERIZADO MODIFICADO - Ambos jugadores y puntuaciones
    player(playerX, playerY)
    player2(player2X, player2Y)  # NUEVO: Dibujar jugador 2
    show_scores()  # NUEVO: Mostrar ambas puntuaciones
    pygame.display.update()
