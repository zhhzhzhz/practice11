import pygame
import random

pygame.init()

# Размеры окна
WIDTH = 600
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Practice 11")

# Цвета
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)       # трава
ROAD_COLOR = (60, 60, 60)   # асфальт
RED = (200, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 220, 0)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()
FPS = 60

font = pygame.font.SysFont("Arial", 24)

# Дорога
road_x = 80
road_width = WIDTH - 160

# Игрок
player_width = 50
player_height = 80
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 120
player_speed = 7

# Враг
enemy_width = 50
enemy_height = 80
enemy_x = random.randint(road_x + 20, road_x + road_width - enemy_width - 20)
enemy_y = -enemy_height
enemy_speed = 4

# Монета
coin_radius = 15
coin_x = random.randint(road_x + 30, road_x + road_width - 30)
coin_y = random.randint(-600, -50)
coin_speed = 4
coin_weight = random.choice([1, 2, 5])

# Счет
score = 0
coins_collected = 0

# После каждых N монет скорость врага увеличивается
N = 5

# Сдвиг разметки, чтобы она двигалась вниз
road_line_offset = 0


def draw_car(surface, x, y, color, width, height):
    """
    Функция рисует машину без колес.
    """
    # Корпус машины
    pygame.draw.rect(surface, color, (x, y, width, height), border_radius=8)

    # Переднее стекло
    pygame.draw.rect(
        surface,
        WHITE,
        (x + 10, y + 10, width - 20, 18),
        border_radius=4
    )

    # Заднее стекло
    pygame.draw.rect(
        surface,
        WHITE,
        (x + 10, y + height - 30, width - 20, 18),
        border_radius=4
    )


running = True

while running:
    clock.tick(FPS)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Нажатые клавиши
    keys = pygame.key.get_pressed()

    # Игрок двигается только влево и вправо
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > road_x + 10:
        player_x -= player_speed

    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < road_x + road_width - player_width - 10:
        player_x += player_speed

    # Враг сам едет вниз
    enemy_y += enemy_speed

    # Если враг ушел вниз, появляется сверху
    if enemy_y > HEIGHT:
        enemy_y = -enemy_height
        enemy_x = random.randint(road_x + 20, road_x + road_width - enemy_width - 20)

    # Монета тоже сама едет вниз
    coin_y += coin_speed

    # Если монета ушла вниз, появляется сверху
    if coin_y > HEIGHT:
        coin_y = random.randint(-600, -50)
        coin_x = random.randint(road_x + 30, road_x + road_width - 30)
        coin_weight = random.choice([1, 2, 5])

    # Двигаем разметку дороги вниз
    road_line_offset += enemy_speed

    if road_line_offset >= 100:
        road_line_offset = 0

    # Прямоугольники для столкновений
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)

    coin_rect = pygame.Rect(
        coin_x - coin_radius,
        coin_y - coin_radius,
        coin_radius * 2,
        coin_radius * 2
    )

    # Столкновение с врагом
    if player_rect.colliderect(enemy_rect):
        running = False

    # Сбор монеты
    if player_rect.colliderect(coin_rect):
        score += coin_weight
        coins_collected += 1

        # Новая монета появляется сверху
        coin_y = random.randint(-600, -50)
        coin_x = random.randint(road_x + 30, road_x + road_width - 30)
        coin_weight = random.choice([1, 2, 5])

        # После каждых 5 монет скорость врага и монет увеличивается
        if coins_collected % N == 0:
            enemy_speed += 1
            coin_speed += 1

    # =====================
    # РИСОВАНИЕ
    # =====================

    # Зеленая трава
    screen.fill(GREEN)

    # Асфальт
    pygame.draw.rect(screen, ROAD_COLOR, (road_x, 0, road_width, HEIGHT))

    # Белые боковые линии дороги
    pygame.draw.line(screen, WHITE, (road_x, 0), (road_x, HEIGHT), 4)
    pygame.draw.line(screen, WHITE, (road_x + road_width, 0), (road_x + road_width, HEIGHT), 4)

    # Движущаяся центральная разметка
    for y in range(-100, HEIGHT, 100):
        pygame.draw.rect(
            screen,
            WHITE,
            (WIDTH // 2 - 5, y + road_line_offset, 10, 50)
        )

    # Монета
    pygame.draw.circle(screen, YELLOW, (coin_x, coin_y), coin_radius)

    # Вес монеты
    weight_text = font.render(str(coin_weight), True, BLACK)
    screen.blit(weight_text, (coin_x - 7, coin_y - 13))

    # Машины
    draw_car(screen, player_x, player_y, BLUE, player_width, player_height)
    draw_car(screen, enemy_x, enemy_y, RED, enemy_width, enemy_height)

    # Счет
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (20, 20))

    # Скорость
    speed_text = font.render(f"Speed: {enemy_speed}", True, WHITE)
    screen.blit(speed_text, (20, 50))

    pygame.display.update()

pygame.quit()