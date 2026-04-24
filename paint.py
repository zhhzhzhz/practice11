import pygame
import math

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)
RED = (220, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 180, 0)

font = pygame.font.SysFont("Arial", 22)

current_tool = "pen"
current_color = BLACK
shape_size = 80

screen.fill(WHITE)

running = True
drawing = False


def draw_menu():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 60))

    text = font.render(
        "1 Pen | 2 Square | 3 Right Triangle | 4 Equilateral Triangle | 5 Rhombus | C Clear",
        True,
        BLACK
    )

    screen.blit(text, (10, 15))


def draw_shape(tool, x, y):
    if tool == "square":
        pygame.draw.rect(
            screen,
            current_color,
            (x, y, shape_size, shape_size),
            3
        )

    elif tool == "right_triangle":
        points = [
            (x, y),
            (x, y + shape_size),
            (x + shape_size, y + shape_size)
        ]

        pygame.draw.polygon(screen, current_color, points, 3)

    elif tool == "equilateral_triangle":
        height = int((math.sqrt(3) / 2) * shape_size)

        points = [
            (x, y + height),
            (x + shape_size // 2, y),
            (x + shape_size, y + height)
        ]

        pygame.draw.polygon(screen, current_color, points, 3)

    elif tool == "rhombus":
        points = [
            (x + shape_size // 2, y),
            (x + shape_size, y + shape_size // 2),
            (x + shape_size // 2, y + shape_size),
            (x, y + shape_size // 2)
        ]

        pygame.draw.polygon(screen, current_color, points, 3)


while running:
    draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_tool = "pen"

            elif event.key == pygame.K_2:
                current_tool = "square"

            elif event.key == pygame.K_3:
                current_tool = "right_triangle"

            elif event.key == pygame.K_4:
                current_tool = "equilateral_triangle"

            elif event.key == pygame.K_5:
                current_tool = "rhombus"

            elif event.key == pygame.K_c:
                screen.fill(WHITE)

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if y > 60:
                if current_tool == "pen":
                    drawing = True
                else:
                    draw_shape(current_tool, x, y)

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False

        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos

            if drawing and current_tool == "pen" and y > 60:
                pygame.draw.circle(screen, current_color, (x, y), 4)

    pygame.display.update()

pygame.quit()