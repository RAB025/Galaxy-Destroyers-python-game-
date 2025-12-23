import random
import math
import pygame
from pygame import mixer

# ==============================
# INITIALIZATION
# ==============================

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("Spaceship.png")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

# ==============================
# GAME STATES
# ==============================

STATE_MENU = "menu"
STATE_SETTINGS = "settings"
STATE_GAME = "game"
STATE_PAUSE = "pause"

current_state = STATE_MENU

is_borderless = True

# ==============================
# FONTS
# ==============================

font = pygame.font.Font("freesansbold.ttf", 32)
title_font = pygame.font.Font("freesansbold.ttf", 64)

# ==============================
# BUTTON DEFINITIONS
# ==============================

close_button = pygame.Rect(SCREEN_WIDTH - 50, 10, 40, 40)

# Menu buttons
play_button = pygame.Rect(
    SCREEN_WIDTH // 2 - 150,
    SCREEN_HEIGHT // 2,
    300,
    60
)
settings_button = pygame.Rect(
    SCREEN_WIDTH // 2 - 150,
    SCREEN_HEIGHT // 2 + 80,
    300,
    60
)

# Pause menu buttons
resume_button = pygame.Rect(450, 400, 300, 60)
quit_button = pygame.Rect(450, 480, 300, 60)

# ==============================
# BACKGROUND & MUSIC
# ==============================

# Load and scale background dynamically
background_img = pygame.image.load("background.jpg")
background = pygame.transform.scale(
    background_img, (SCREEN_WIDTH, SCREEN_HEIGHT)
)

mixer.music.load("bgm.wav")
mixer.music.play(-1)

sound_on = True

# ==============================
# VOLUME SLIDER
# ==============================

volume = 0.5
slider_bar = pygame.Rect(350, 350, 500, 8)
slider_knob = pygame.Rect(350 + int(volume * 500) - 10, 343, 20, 22)
dragging = False

mixer.music.set_volume(volume)

# ==============================
# UI DRAW FUNCTIONS
# ==============================

def toggle_borderless():
    global screen, SCREEN_WIDTH, SCREEN_HEIGHT, is_borderless

    is_borderless = not is_borderless

    if is_borderless:
        screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
    else:
        screen = pygame.display.set_mode((1200, 900))

    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

def draw_close_button():
    pygame.draw.rect(screen, (200, 50, 50), close_button, border_radius=8)
    x_text = font.render("X", True, (255, 255, 255))
    screen.blit(x_text, (close_button.x + 12, close_button.y + 5))


def draw_menu():
    screen.fill((0, 0, 0))
    title = title_font.render("SPACE INVADERS", True, (255, 255, 255))
    screen.blit(title, (320, 250))

    pygame.draw.rect(screen, (50, 150, 255), play_button, border_radius=10)
    pygame.draw.rect(screen, (50, 150, 255), settings_button, border_radius=10)

    screen.blit(font.render("PLAY", True, (255, 255, 255)),
                (play_button.x + 110, play_button.y + 15))
    screen.blit(font.render("SETTINGS", True, (255, 255, 255)),
                (settings_button.x + 85, settings_button.y + 15))


def draw_settings():
    screen.fill((20, 20, 20))
    screen.blit(title_font.render("SETTINGS", True, (255, 255, 255)), (420, 250))

    pygame.draw.rect(screen, (200, 200, 200), slider_bar)
    pygame.draw.rect(screen, (50, 150, 255), slider_knob)

    screen.blit(font.render("Volume", True, (255, 255, 255)), (350, 310))
    screen.blit(font.render("Press ESC to return", True, (255, 255, 255)), (420, 420))


def draw_pause_menu():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    screen.blit(title_font.render("PAUSED", True, (255, 255, 255)), (450, 250))

    pygame.draw.rect(screen, (50, 150, 255), resume_button, border_radius=10)
    pygame.draw.rect(screen, (200, 50, 50), quit_button, border_radius=10)

    screen.blit(font.render("RESUME", True, (255, 255, 255)),
                (resume_button.x + 95, resume_button.y + 15))
    screen.blit(font.render("QUIT", True, (255, 255, 255)),
                (quit_button.x + 115, quit_button.y + 15))
    

# ==============================
# PLAYER
# ==============================

player_img = pygame.image.load("Player.png")
player_width = player_img.get_width()
player_height = player_img.get_height()

player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 30

player_x_change = 0

def draw_player(x, y):
    screen.blit(player_img, (x, y))

# ==============================
# ENEMIES
# ==============================

num_enemies = 5
enemy_img = [pygame.image.load("monster.png") for _ in range(num_enemies)]
enemy_width = enemy_img[0].get_width()
enemy_x = [random.randint(20, SCREEN_WIDTH - enemy_width - 20) for _ in range(num_enemies)]
enemy_y = [random.randint(20, SCREEN_HEIGHT // 4) for _ in range(num_enemies)]
enemy_x_change = [0.7] * num_enemies
enemy_y_change = [20] * num_enemies

def draw_enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

# ==============================
# BULLET
# ==============================

bullet_img = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 750
bullet_y_change = 7
bullet_state = "ready"

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"

    bullet_x_centered = x + player_width // 2 - bullet_img.get_width() // 2
    screen.blit(bullet_img, (bullet_x_centered, y))

# ==============================
# COLLISION
# ==============================

def is_collision(ex, ey, bx, by):
    return math.sqrt((ex - bx) ** 2 + (ey - by) ** 2) < 120

# ==============================
# SCORE
# ==============================

score = 0

def show_score():
    screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))

# ==============================
# MAIN GAME LOOP
# ==============================

running = True
while running:
    clock.tick(60)

    # ---------- EVENTS ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                toggle_borderless()


        # Global close button
        if event.type == pygame.MOUSEBUTTONDOWN and close_button.collidepoint(event.pos):
            running = False

        # MENU
        if current_state == STATE_MENU and event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.collidepoint(event.pos):
                current_state = STATE_GAME
            elif settings_button.collidepoint(event.pos):
                current_state = STATE_SETTINGS

        # SETTINGS
        elif current_state == STATE_SETTINGS:
            if event.type == pygame.MOUSEBUTTONDOWN and slider_knob.collidepoint(event.pos):
                dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                slider_knob.x = max(slider_bar.x,
                                    min(event.pos[0] - 10, slider_bar.x + slider_bar.width - 10))
                volume = (slider_knob.x - slider_bar.x) / slider_bar.width
                mixer.music.set_volume(volume)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                current_state = STATE_MENU

        # GAME
        elif current_state == STATE_GAME:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_state = STATE_PAUSE
                elif event.key == pygame.K_LEFT:
                    player_x_change = -5
                elif event.key == pygame.K_RIGHT:
                    player_x_change = 5
                elif event.key == pygame.K_SPACE and bullet_state == "ready":
                    bullet_x, bullet_y = player_x, player_y
                    if sound_on:
                        mixer.Sound("laser.wav").play()
                    fire_bullet(bullet_x, bullet_y)
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    player_x_change = 0

        # PAUSE
        elif current_state == STATE_PAUSE:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                current_state = STATE_GAME
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.collidepoint(event.pos):
                    current_state = STATE_GAME
                elif quit_button.collidepoint(event.pos):
                    running = False

    # ---------- RENDER ----------
    if current_state == STATE_MENU:
        draw_menu()
    elif current_state == STATE_SETTINGS:
        draw_settings()
    elif current_state == STATE_PAUSE:
        draw_pause_menu()
    elif current_state == STATE_GAME:
        screen.blit(background, (0, 0))
        player_x = max(0, min(player_x + player_x_change, 1072))

        if bullet_state == "fire":
            fire_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_y_change
            if bullet_y <= 0:
                bullet_y, bullet_state = 750, "ready"

        for i in range(num_enemies):
            enemy_x[i] += enemy_x_change[i]
            if enemy_x[i] <= 0 or enemy_x[i] >= SCREEN_WIDTH - enemy_width:
                enemy_x_change[i] *= -1
                enemy_y[i] += enemy_y_change[i]

            if is_collision(enemy_x[i], enemy_y[i], bullet_x + 44, bullet_y + 15):
                score += 1
                bullet_y, bullet_state = 750, "ready"
                enemy_x[i] = random.randint(20, 940)
                enemy_y[i] = random.randint(20, 200)

            draw_enemy(enemy_x[i], enemy_y[i], i)

        draw_player(player_x, player_y)
        show_score()

    draw_close_button()
    pygame.display.update()

pygame.quit()
