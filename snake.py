import pygame
import random

pygame.init()

WIDTH = 600
HEIGHT = 400
BLOCK = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

BLACK = (0, 0, 0)
RED = (220, 0, 0)
BLUE = (0, 100, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 220, 0)

clock = pygame.time.Clock()
FPS = 10

font = pygame.font.SysFont("Arial", 24)

snake = [(100, 100)]

dx = BLOCK
dy = 0

score = 0
small_points_eaten = 0

FOOD_LIFETIME = 5000


def create_food(food_type="small"):
    x = random.randrange(0, WIDTH, BLOCK)
    y = random.randrange(0, HEIGHT, BLOCK)
    spawn_time = pygame.time.get_ticks()

    if food_type == "big":
        weight = 5
    else:
        weight = 1

    return {
        "x": x,
        "y": y,
        "type": food_type,
        "weight": weight,
        "spawn_time": spawn_time
    }


food = create_food("small")

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and dy == 0:
                dx = 0
                dy = -BLOCK

            elif event.key == pygame.K_DOWN and dy == 0:
                dx = 0
                dy = BLOCK

            elif event.key == pygame.K_LEFT and dx == 0:
                dx = -BLOCK
                dy = 0

            elif event.key == pygame.K_RIGHT and dx == 0:
                dx = BLOCK
                dy = 0

    head_x = snake[0][0] + dx
    head_y = snake[0][1] + dy
    new_head = (head_x, head_y)

    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        running = False

    if new_head in snake:
        running = False

    snake.insert(0, new_head)

    if head_x == food["x"] and head_y == food["y"]:
        score += food["weight"]

        for i in range(food["weight"]):
            snake.append(snake[-1])

        if food["type"] == "small":
            small_points_eaten += 1

            if small_points_eaten == 5:
                food = create_food("big")
                small_points_eaten = 0
            else:
                food = create_food("small")
        else:
            food = create_food("small")

    else:
        snake.pop()

    current_time = pygame.time.get_ticks()

    if current_time - food["spawn_time"] > FOOD_LIFETIME:
        food = create_food(food["type"])

    screen.fill(BLACK)

    for block in snake:
        pygame.draw.rect(screen, RED, (block[0], block[1], BLOCK, BLOCK))

    if food["type"] == "big":
        food_color = RED
        pygame.draw.rect(
            screen,
            food_color,
            (food["x"] - 5, food["y"] - 5, BLOCK + 10, BLOCK + 10)
        )
    else:
        food_color = BLUE
        pygame.draw.rect(
            screen,
            food_color,
            (food["x"], food["y"], BLOCK, BLOCK)
        )

    food_text = font.render(str(food["weight"]), True, YELLOW)
    screen.blit(food_text, (food["x"] + 3, food["y"] - 3))

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    left_text = font.render(f"Small before big: {5 - small_points_eaten}", True, WHITE)
    screen.blit(left_text, (10, 40))

    current_time = pygame.time.get_ticks()
    time_left = max(
        0,
        (FOOD_LIFETIME - (current_time - food["spawn_time"])) // 1000
    )

    timer_text = font.render(f"Food time: {time_left}", True, WHITE)
    screen.blit(timer_text, (10, 70))

    pygame.display.update()

pygame.quit()