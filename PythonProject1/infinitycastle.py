import pygame, random, math
from pygame.locals import *

pygame.init()
pygame.mixer.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CELL_SIZE = 20
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Xenzia Demon Slayer Edition")

# Icon
icon = pygame.image.load("img\\tnjro.png").convert_alpha()
pygame.display.set_icon(icon)

# Background
bg = pygame.image.load("img\\ic.jpg")
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Tanjiro (player)
tanjiro_img = pygame.image.load("img\\tnjro.png").convert_alpha()
tanjiro_img = pygame.transform.scale(tanjiro_img, (CELL_SIZE * 3, CELL_SIZE * 3))

# Normal food (Muzan small)
NORMAL_SIZE = CELL_SIZE * 3
normal_demon_img = pygame.image.load(
    "img\\hantengu.png").convert_alpha()
normal_demon_img = pygame.transform.scale(normal_demon_img, (NORMAL_SIZE * 2, NORMAL_SIZE * 2))

# Bonus food (special Muzan)
BONUS_SIZE = CELL_SIZE * 5
bonus_demon_img = pygame.image.load(
    "img\\muzan.png").convert_alpha()
bonus_demon_img = pygame.transform.scale(bonus_demon_img, (BONUS_SIZE * 2, BONUS_SIZE * 2))

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Font
font = pygame.font.SysFont("Arial", 36)

# -------- SOUNDS --------
pygame.mixer.music.load("PythonProject1\\inf.mp3")
pygame.mixer.music.play(-1)  # loop forever

kill_sound = pygame.mixer.Sound("img\\slash.wav")
lose_sound = pygame.mixer.Sound("img\\toin.wav")
pygame.mixer.Sound.play(kill_sound)


def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


# Player setup
x, y = 100, 100
direction = "RIGHT"
score = 0
speed = 10
game_over = False
clock = pygame.time.Clock()
frame_counter = 0  # for animation


# Food functions
def spawn_food(size):
    while True:
        fx = random.randrange(0, SCREEN_WIDTH - size, CELL_SIZE)
        fy = random.randrange(0, SCREEN_HEIGHT - size, CELL_SIZE)
        food_rect = pygame.Rect(fx, fy, size, size)
        if not food_rect.collidepoint(x + CELL_SIZE // 2, y + CELL_SIZE // 2):
            return (fx, fy)


food = spawn_food(NORMAL_SIZE)

# Bonus food variables
bonus_food = None
bonus_timer = 0
BONUS_DURATION = 30 # frames
BONUS_CHANCE = 0.01
BONUS_POINTS = 5

# Game loop
run = True
while run:
    frame_counter += 1
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == K_UP:
                direction = "UP"
            if event.key == K_DOWN:
                direction = "DOWN"
            if event.key == K_LEFT:
                direction = "LEFT"
            if event.key == K_RIGHT:
                direction = "RIGHT"

    if not game_over:
        # Move Tanjiro
        if direction == "UP": y -= CELL_SIZE
        if direction == "DOWN": y += CELL_SIZE
        if direction == "LEFT": x -= CELL_SIZE
        if direction == "RIGHT": x += CELL_SIZE

        # Wall collision
        if x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT:
            game_over = True
            lose_sound.play()  # 🔊 play lose sound

        # Head rect for collision
        head_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

        # Check normal food
        food_rect = pygame.Rect(food[0], food[1], NORMAL_SIZE, NORMAL_SIZE)
        if head_rect.colliderect(food_rect):
            score += 1
            speed += 0.5
            food = spawn_food(NORMAL_SIZE)
            kill_sound.play()  # 🔊 play kill sound

        # Bonus food spawn
        if bonus_food is None and random.random() < BONUS_CHANCE:
            while True:
                fx = random.randrange(0, SCREEN_WIDTH - BONUS_SIZE, CELL_SIZE)
                fy = random.randrange(0, SCREEN_HEIGHT - BONUS_SIZE, CELL_SIZE)
                bonus_rect = pygame.Rect(fx, fy, BONUS_SIZE, BONUS_SIZE)
                if not bonus_rect.collidepoint(x + CELL_SIZE // 2, y + CELL_SIZE // 2):
                    bonus_food = (fx, fy)
                    bonus_timer = BONUS_DURATION
                    break

        # Bonus food collision or timer
        if bonus_food:
            bonus_rect = pygame.Rect(bonus_food[0], bonus_food[1], BONUS_SIZE, BONUS_SIZE)
            if head_rect.colliderect(bonus_rect):
                score += BONUS_POINTS
                speed += 1
                bonus_food = None
                bonus_timer = 0
                kill_sound.play()  # 🔊 play kill sound
            else:
                bonus_timer -= 1
                if bonus_timer <= 0:
                    bonus_food = None

        # Draw normal food
        screen.blit(normal_demon_img, food)

        # Draw bonus food with bounce and timer bar
        if bonus_food:
            bounce = 0.1 * math.sin(frame_counter * 0.3)
            size = int(BONUS_SIZE * (1 + bounce))
            bonus_img_scaled = pygame.transform.scale(bonus_demon_img, (size, size))
            offset = (BONUS_SIZE - size) // 2
            screen.blit(bonus_img_scaled, (bonus_food[0] + offset, bonus_food[1] + offset))
            # Timer bar
            bar_width = int(BONUS_SIZE * (bonus_timer / BONUS_DURATION))
            pygame.draw.rect(screen, RED, (bonus_food[0], bonus_food[1] - 10, bar_width, 5))

        # Draw Tanjiro head
        screen.blit(tanjiro_img, (x, y))

        # Draw score
        draw_text(f"Score: {score}", font, WHITE, SCREEN_WIDTH - 180, 20)

    else:
        draw_text("GAME OVER!", font, WHITE, SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 20)
        draw_text("Click Anywhere To Restart", font, WHITE, SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 20)

        if pygame.mouse.get_pressed()[0]:
            x, y = 100, 100
            direction = "RIGHT"
            score = 0
            speed = 10
            game_over = False
            food = spawn_food(NORMAL_SIZE)
            bonus_food = None
            bonus_timer = 0
            frame_counter = 0

    pygame.display.update()
    clock.tick(speed)

pygame.quit()