import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 600
BORDER = 20
BLOCK = 25
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('🐍 Snake Game for Kids! 🐍')

# Load UI images (MAKE SURE THEY ARE IN THE SAME FOLDER)
title_image = pygame.image.load("snake_play.png").convert_alpha()
title_image = pygame.transform.scale(title_image, (WIDTH, HEIGHT))

gameover_image = pygame.image.load("game_last.png").convert_alpha()
gameover_image = pygame.transform.scale(gameover_image, (WIDTH, HEIGHT))

# Colors
PASTEL_GREEN = (144, 238, 144)
SNAKE_GREEN = (102, 205, 102)
DARK_GREEN = (60, 179, 113)
CREAM = (255, 253, 208)
SOFT_PINK = (255, 182, 193)
SOFT_BLUE = (173, 216, 230)
CORAL = (255, 127, 80)
LAVENDER = (230, 230, 250)
MINT = (189, 252, 201)
PEACH = (255, 218, 185)
LIGHT_YELLOW = (255, 255, 224)
SOFT_PURPLE = (221, 160, 221)
WHITE = (255, 255, 255)
BLACK = (50, 50, 50)
RED_APPLE = (255, 99, 71)

# Fonts
font = pygame.font.SysFont('Comic Sans MS', 24, bold=True)
small_font = pygame.font.SysFont('Comic Sans MS', 18, bold=True)
big_font = pygame.font.SysFont('Comic Sans MS', 36, bold=True)

def draw_cute_background():
    screen.fill(CREAM)
    for i in range(0, WIDTH, 60):
        for j in range(0, HEIGHT, 60):
            pygame.draw.circle(screen, LIGHT_YELLOW, (i + 30, j + 30), 2, 1)

def draw_simple_border():
    pygame.draw.rect(screen, SOFT_PINK, (0, 0, WIDTH, BORDER))
    pygame.draw.rect(screen, SOFT_PINK, (0, HEIGHT - BORDER, WIDTH, BORDER))
    pygame.draw.rect(screen, SOFT_PINK, (0, 0, BORDER, HEIGHT))
    pygame.draw.rect(screen, SOFT_PINK, (WIDTH - BORDER, 0, BORDER, HEIGHT))
    pygame.draw.circle(screen, SOFT_PINK, (BORDER, BORDER), BORDER)
    pygame.draw.circle(screen, SOFT_PINK, (WIDTH - BORDER, BORDER), BORDER)
    pygame.draw.circle(screen, SOFT_PINK, (BORDER, HEIGHT - BORDER), BORDER)
    pygame.draw.circle(screen, SOFT_PINK, (WIDTH - BORDER, HEIGHT - BORDER), BORDER)

def draw_super_cute_snake(snake_list, direction):
    for i, (x, y) in enumerate(snake_list):
        if i == 0:
            pygame.draw.circle(screen, SNAKE_GREEN, (x + BLOCK // 2, y + BLOCK // 2), BLOCK // 2 + 2)
            pygame.draw.circle(screen, PASTEL_GREEN, (x + BLOCK // 2 - 2, y + BLOCK // 2 - 2), BLOCK // 2)
            eye_size = 4
            if direction == 'right':
                eye1_pos = (x + 8, y + 6)
                eye2_pos = (x + 8, y + 18)
            elif direction == 'left':
                eye1_pos = (x + 16, y + 6)
                eye2_pos = (x + 16, y + 18)
            elif direction == 'up':
                eye1_pos = (x + 6, y + 16)
                eye2_pos = (x + 18, y + 16)
            else:
                eye1_pos = (x + 6, y + 8)
                eye2_pos = (x + 18, y + 8)

            pygame.draw.circle(screen, WHITE, eye1_pos, eye_size)
            pygame.draw.circle(screen, WHITE, eye2_pos, eye_size)
            pygame.draw.circle(screen, BLACK, eye1_pos, eye_size - 1)
            pygame.draw.circle(screen, BLACK, eye2_pos, eye_size - 1)
            pygame.draw.circle(screen, WHITE, (eye1_pos[0] + 1, eye1_pos[1] - 1), 1)
            pygame.draw.circle(screen, WHITE, (eye2_pos[0] + 1, eye2_pos[1] - 1), 1)
            smile_center = (x + BLOCK // 2, y + BLOCK // 2 + 4)
            pygame.draw.arc(screen, BLACK, (smile_center[0] - 6, smile_center[1] - 3, 12, 8), 0, math.pi, 2)
        else:
            pygame.draw.rect(screen, DARK_GREEN, (x + 2, y + 2, BLOCK - 4, BLOCK - 4), border_radius=8)
            pygame.draw.rect(screen, PASTEL_GREEN, (x + 4, y + 4, BLOCK - 8, BLOCK - 8), border_radius=6)

def draw_yummy_food(food_pos):
    x, y = food_pos
    center_x, center_y = x + BLOCK // 2, y + BLOCK // 2
    pygame.draw.circle(screen, RED_APPLE, (center_x, center_y + 2), BLOCK // 2 - 1)
    pygame.draw.circle(screen, CORAL, (center_x - 2, center_y), BLOCK // 2 - 3)
    pygame.draw.rect(screen, DARK_GREEN, (center_x - 1, center_y - 8, 2, 6))
    pygame.draw.ellipse(screen, PASTEL_GREEN, (center_x + 2, center_y - 8, 6, 4))

def show_text(text, x, y, color=BLACK, font_obj=None):
    if font_obj is None:
        font_obj = font
    surf = font_obj.render(text, True, color)
    screen.blit(surf, (x, y))

def draw_score_and_level(score, level):
    show_text(f'🍎 Score: {score}', 30, 30, BLACK, font)
    stars = '⭐' * min(level, 5)
    show_text(f'{stars} Level {level}', 30, 60, BLACK, font)

def get_valid_food_position(snake_list):
    while True:
        margin = BORDER + BLOCK * 3
        max_x = (WIDTH - margin * 2) // BLOCK
        max_y = (HEIGHT - margin * 2) // BLOCK
        food_x = random.randint(0, max_x - 1) * BLOCK + margin
        food_y = random.randint(0, max_y - 1) * BLOCK + margin
        if (food_x, food_y) not in snake_list:
            return (food_x, food_y)

def check_food_collision(snake_head, food_pos):
    head_x, head_y = snake_head
    food_x, food_y = food_pos
    return abs(head_x - food_x) < BLOCK and abs(head_y - food_y) < BLOCK

clock = pygame.time.Clock()

def game_loop():
    running = True
    start_x = (WIDTH // 2 // BLOCK) * BLOCK
    start_y = (HEIGHT // 2 // BLOCK) * BLOCK
    snake = [(start_x, start_y)]
    dx, dy = BLOCK, 0
    direction = 'right'
    score = 0
    level = 1
    snake_length = 1
    base_speed = 4
    current_speed = base_speed
    food = get_valid_food_position(snake)

    while running:
        draw_cute_background()
        draw_simple_border()
        draw_super_cute_snake(snake, direction)
        draw_yummy_food(food)
        draw_score_and_level(score, level)

        if score == 0:
            show_text("Use arrow keys to move! 🐍", WIDTH//2 - 120, HEIGHT - 50, SOFT_PURPLE, small_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a) and dx == 0:
                    dx, dy = -BLOCK, 0
                    direction = 'left'
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and dx == 0:
                    dx, dy = BLOCK, 0
                    direction = 'right'
                elif event.key in (pygame.K_UP, pygame.K_w) and dy == 0:
                    dx, dy = 0, -BLOCK
                    direction = 'up'
                elif event.key in (pygame.K_DOWN, pygame.K_s) and dy == 0:
                    dx, dy = 0, BLOCK
                    direction = 'down'

        if dx != 0 or dy != 0:
            head_x, head_y = snake[0]
            new_head = (head_x + dx, head_y + dy)
            snake.insert(0, new_head)

            if check_food_collision(new_head, food):
                score += 1
                snake_length += 1
                food = get_valid_food_position(snake)
                if score % 3 == 0:
                    level += 1
                    current_speed = min(current_speed + 0.5, 8)

            if len(snake) > snake_length:
                snake.pop()

        head_x, head_y = snake[0]
        if (head_x < BORDER or head_x >= WIDTH - BORDER or
            head_y < BORDER or head_y >= HEIGHT - BORDER):
            break
        if snake[0] in snake[1:]:
            break

        pygame.display.update()
        clock.tick(current_speed)

    # Game Over Screen
    screen.blit(gameover_image, (0, 0))
    pygame.display.update()
    pygame.time.wait(3000)  # Wait 3 seconds

    # Restart option
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                waiting = False
    return True

# Main game loop
if __name__ == "__main__":
    while True:
        screen.blit(title_image, (0, 0))
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False

        if not game_loop():
            break

    pygame.quit()
