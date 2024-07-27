import pygame
import sys
import racket
import ball

# Initialize pygame modules
pygame.font.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

FPS = 60

WHITE = (255, 255, 255)
RED = (255, 50, 50)
BLUE = (50, 50, 255)
BACKGROUND_COLOR = (25, 25, 25)


def draw_racket(racket: racket.Racket) -> None:
    pygame.draw.rect(
        surface=screen,
        color=racket.COLOR,
        rect=(racket.x_pos, racket.y_pos, racket.WIDTH, racket.HEIGHT)
    )


def draw_ball(game_ball: ball.Ball) -> None:
    pygame.draw.circle(
        surface=screen,
        color=game_ball.COLOR,
        center=(game_ball.x_pos, game_ball.y_pos),
        radius=game_ball.RADIUS
    )


def draw_counter(points: int, color: tuple, pos: tuple) -> None:
    screen.blit(
        pygame.font.Font(None, 48).render(f'Score: {points}', True, color), pos
    )


def draw_game_field() -> None:
    # Draw center line
    pygame.draw.rect(
        surface=screen,
        color=WHITE,
        rect=(SCREEN_WIDTH // 2 - 5, 0, 10, SCREEN_HEIGHT),
    )

    # Draw center circle
    pygame.draw.circle(
        surface=screen,
        color=WHITE,
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
        radius=100,
        width=10
    )


# Respawn rackets and ball
def respawn_objects() -> None:
    left_racket.respawn_racket()
    right_racket.respawn_racket()

    game_ball.respawn_ball()


# Window settings
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ping Pong')

# Create Clock object for setting framerate
delay = pygame.time.Clock()

# Create Rackets to play
left_racket = racket.Racket(
    x_pos = 0,
    y_pos = SCREEN_HEIGHT // 2 - racket.Racket.HEIGHT // 2,
    UP_BUTTON=pygame.K_w, 
    DOWN_BUTTON=pygame.K_s,
    FLAG=0
)

right_racket = racket.Racket(
    x_pos = SCREEN_WIDTH - racket.Racket.WIDTH,
    y_pos = SCREEN_HEIGHT  // 2 - racket.Racket.HEIGHT // 2,
    UP_BUTTON=pygame.K_UP,
    DOWN_BUTTON=pygame.K_DOWN,
    FLAG=1
)

# Create ball
game_ball = ball.Ball(
    x_pos=SCREEN_WIDTH // 2,
    y_pos=SCREEN_HEIGHT // 2
)

# Initialize game
while True:
    screen.fill(BACKGROUND_COLOR)

    #Draw Rackets
    draw_racket(left_racket)
    draw_racket(right_racket)

    # Draw middle line and circle
    draw_game_field()

    # Draw counters
    draw_counter(left_racket.player_points, RED, (20, 10))
    draw_counter(right_racket.player_points, BLUE, (630, 10))

    # Draw Ball
    draw_ball(game_ball)

    # Get events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Event handler for ball
    game_ball.event_handler(left_racket, right_racket)
    check_win = game_ball.win_handler(left_racket, right_racket)

    if check_win == left_racket.FLAG:
        screen.blit(
            pygame.font.Font(None, 60).render(f'Player 1 wins!', True, RED), (150, 500)
        )

        pygame.display.update()
        pygame.time.delay(1500)

        respawn_objects()

    elif check_win == right_racket.FLAG:
        screen.blit(
            pygame.font.Font(None, 60).render(f'Player 2 wins!', True, BLUE), (750, 500)
        )

        pygame.display.update()
        pygame.time.delay(1500)

        respawn_objects()

    key = pygame.key.get_pressed()

    # Event handler for rackets
    left_racket.event_handler(key)
    right_racket.event_handler(key)

    # Move ball
    game_ball.move()

    # Update display ;)
    pygame.display.update()
    delay.tick(FPS)