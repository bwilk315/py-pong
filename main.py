
import pygame
import random

SCRW  = 640
SCRH  = 720
FPS   = 120
WHITE = pygame.Color(255, 255, 255, 255)
INVSQRT2 = 0.7071

pygame.init()
screen = pygame.display.set_mode((SCRW, SCRH))
surf   = pygame.display.get_surface()
clock  = pygame.time.Clock()
run    = True

player    = pygame.Rect(0, 0, SCRW / 4, SCRH / 20)
player.x  = SCRW / 2 - player.w / 2
player.y  = SCRH - 2 * player.h
p_speed   = 7
p_hor_vel = 0

ai        = player.copy()
ai.y      = player.h
a_hor_vel = 0

ball    = pygame.Rect(0, 0, SCRW / 20, SCRW / 20)
ball.x  = SCRW / 2 - ball.w / 2
ball.y  = SCRH / 2 - ball.w / 2
b_speed = 5
b_sips  = 0.2  # Increase in speed per second
b_vel   = pygame.Vector2(
    INVSQRT2 * (random.randint(0, 1) - 0.5) * 2,
    INVSQRT2 * (random.randint(0, 1) - 0.5) * 2
).normalize()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Handle user input
    p_hor_vel = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False
    if keys[pygame.K_RIGHT]:
        p_hor_vel += p_speed
    if keys[pygame.K_LEFT]:
        p_hor_vel -= p_speed
    
    # Control player's paddle position
        
    if p_hor_vel < 0:
        if player.x + p_hor_vel >= 0:
            player.x += p_hor_vel
        else:
            player.x = 0
    elif p_hor_vel > 0:
        if player.x + player.w + p_hor_vel <= SCRW:
            player.x += p_hor_vel
        else:
            player.x = SCRW - player.w

    # Control ai's paddle position
    
    px = ball.x + ball.w / 2
    if px >= ai.w / 2 and px <= SCRW - ai.w / 2:
        ai.x = px - ai.w / 2

    # Control ball position
    
    if b_vel.x > 0:
        if ball.x + ball.w >= SCRW:
            ball.x   = SCRW - ball.w
            b_vel.x *= -1
    elif b_vel.x < 0:
        if ball.x <= 0:
            ball.x   = 0
            b_vel.x *= -1

    if b_vel.y > 0:
        if ball.x + ball.w >= player.x and ball.x <= player.x + player.w:
            if ball.y >= player.y - player.h and ball.y <= player.y  - player.h * 3/4:
                ball.y   = player.y - player.h
                b_vel.y *= -1
    if b_vel.y < 0:
        if ball.x + ball.w >= ai.x and ball.x <= ai.x + ai.w:
            if ball.y - ball.h <= ai.y and ball.y >= ai.y - ai.h * 1/4:
                ball.y   = ai.y + ball.h
                b_vel.y *= -1

    if ball.y - ball.h >= SCRH or ball.y <= 0:
        b_vel.y *= -1
        b_speed  = 5
        ball.x = SCRW / 2
        ball.y = SCRH / 2

    ball.x  += b_vel.x * b_speed
    ball.y  += b_vel.y * b_speed
    b_speed += b_sips / FPS

    # Draw stuff
    
    screen.fill("black")
    pygame.draw.rect(surf, WHITE, player)
    pygame.draw.rect(surf, WHITE, ai)
    pygame.draw.circle(surf, WHITE, pygame.Vector2(ball.x + ball.w / 2, ball.y + ball.h / 2), ball.w / 2)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
