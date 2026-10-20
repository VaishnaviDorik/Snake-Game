
import random
import pygame

pygame.init()

# Game settings
CELL = 20
COLS = 30
ROWS = 24
HEADER = 50
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL + HEADER
FPS = 10

# Colors
BLACK = (18, 18, 22)
GREEN = (65, 190, 95)
LIGHT_GREEN = (115, 225, 125)
RED = (235, 75, 75)
WHITE = (245, 245, 245)
GRAY = (170, 170, 180)


def make_food(snake):
    empty = [
        (x, y)
        for x in range(COLS)
        for y in range(ROWS)
        if (x, y) not in snake
    ]
    return random.choice(empty) if empty else None


def reset_game():
    x, y = COLS // 2, ROWS // 2
    snake = [(x, y), (x - 1, y), (x - 2, y)]
    direction = (1, 0)
    food = make_food(snake)
    return snake, direction, food, 0, False


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Snake Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 24)

snake, direction, food, score, game_over = reset_game()
running = True

keys = {
    pygame.K_UP: (0, -1),
    pygame.K_w: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_s: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_a: (-1, 0),
    pygame.K_RIGHT: (1, 0),
    pygame.K_d: (1, 0),
}

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif game_over and event.key in (
                pygame.K_r, pygame.K_RETURN, pygame.K_SPACE
            ):
                snake, direction, food, score, game_over = reset_game()

            elif not game_over and event.key in keys:
                new_direction = keys[event.key]
                # Do not allow an immediate reverse turn.
                if new_direction != (-direction[0], -direction[1]):
                    direction = new_direction

    if not game_over:
        head_x, head_y = snake[0]
        new_head = (
            head_x + direction[0],
            head_y + direction[1],
        )

        eating = new_head == food
        body = snake if eating else snake[:-1]

        hit_wall = (
            new_head[0] < 0
            or new_head[0] >= COLS
            or new_head[1] < 0
            or new_head[1] >= ROWS
        )
        hit_body = new_head in body

        if hit_wall or hit_body:
            game_over = True
        else:
            snake.insert(0, new_head)

            if eating:
                score += 1
                food = make_food(snake)
                if food is None:
                    game_over = True
            else:
                snake.pop()

    # Draw the screen
    screen.fill(BLACK)
    pygame.draw.rect(screen, (35, 35, 43), (0, 0, WIDTH, HEADER))

    score_text = font.render(
        f"SNAKE GAME       Score: {score}", True, WHITE
    )
    screen.blit(score_text, (12, 12))

    # Food
    if food is not None:
        pygame.draw.circle(
            screen,
            RED,
            (
                food[0] * CELL + CELL // 2,
                HEADER + food[1] * CELL + CELL // 2,
            ),
            CELL // 2 - 2,
        )

    # Snake
    for index, (x, y) in enumerate(snake):
        color = LIGHT_GREEN if index == 0 else GREEN
        rect = pygame.Rect(
            x * CELL + 1,
            HEADER + y * CELL + 1,
            CELL - 2,
            CELL - 2,
        )
        pygame.draw.rect(screen, color, rect, border_radius=4)

    if game_over:
        overlay = pygame.Surface((WIDTH, ROWS * CELL), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 185))
        screen.blit(overlay, (0, HEADER))

        message = font.render("GAME OVER!", True, WHITE)
        final_score = small_font.render(
            f"Your score: {score}", True, LIGHT_GREEN
        )
        restart = small_font.render(
            "Press R or Enter to restart", True, WHITE
        )
        quit_text = small_font.render(
            "Press Esc to quit", True, GRAY
        )

        center_x = WIDTH // 2
        center_y = HEADER + (ROWS * CELL) // 2

        screen.blit(
            message, message.get_rect(center=(center_x, center_y - 40))
        )
        screen.blit(
            final_score,
            final_score.get_rect(center=(center_x, center_y)),
        )
        screen.blit(
            restart,
            restart.get_rect(center=(center_x, center_y + 35)),
        )
        screen.blit(
            quit_text,
            quit_text.get_rect(center=(center_x, center_y + 65)),
        )

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
