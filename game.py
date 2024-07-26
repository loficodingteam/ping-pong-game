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
ball = ball.Ball(
    x_pos=SCREEN_WIDTH // 2,
    y_pos=SCREEN_HEIGHT // 2
)

# Initialize game
while True:
    screen.fill(BACKGROUND_COLOR)

    screen.blit(pygame.font.Font(None, 48).render(f'Score: {left_racket.player_points}', True,
                                  (255, 50, 50)), (20, 10))
    screen.blit(pygame.font.SysFont(None, 48).render(f'Score: {right_racket.player_points}', False,
                                     (50, 50, 255)), (630, 10))

    #Draw Rackets
    pygame.draw.rect(
        surface=screen,
        color=left_racket.COLOR,
        rect=(left_racket.x_pos, left_racket.y_pos, left_racket.WIDTH, left_racket.HEIGHT)
    )

    pygame.draw.rect(
        surface=screen,
        color=right_racket.COLOR,
        rect=(right_racket.x_pos, right_racket.y_pos, right_racket.WIDTH, right_racket.HEIGHT)
    )

    # Draw middle line
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

    # Draw Ball
    pygame.draw.circle(
        surface=screen,
        color=ball.COLOR,
        center=(ball.x_pos, ball.y_pos),
        radius=ball.RADIUS
    )

    #Get events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Event handler for ball
    ball.event_handler(left_racket, right_racket)

    key = pygame.key.get_pressed()

    # Event handler for rackets
    left_racket.event_handler(key)
    right_racket.event_handler(key)

    # Move ball
    ball.move()

    # Update display ;)
    pygame.display.update()
    delay.tick(FPS)