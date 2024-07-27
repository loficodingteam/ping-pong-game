import pygame
import sys
import racket
import ball
import start_menu

# Initialize pygame modules
pygame.init()

# Constants
SCREEN_WIDTH: int = 1200
SCREEN_HEIGHT: int = 700

FPS: int = 60

WHITE: tuple = (255, 255, 255)
RED: tuple = (255, 50, 50)
BLUE: tuple = (50, 50, 255)
BACKGROUND_COLOR: tuple = (25, 25, 25)

WIN_POINTS: int = 5

SOUND_BEAT_RACKET = pygame.mixer.Sound('sounds/spank-border.wav')
SOUND_BEAT_RACKET.set_volume(0.3)

SOUND_BEAT_LEFT_RIGHT_BORDER = pygame.mixer.Sound('sounds/oh-shit-iam-sorry-win-round.wav')
SOUND_BEAT_LEFT_RIGHT_BORDER.set_volume(0.3)

SOUND_WIN_GAME = pygame.mixer.Sound('sounds/fuck-you-win-the-game.wav')
SOUND_WIN_GAME.set_volume(0.3)

SOUND_PRESS_START = pygame.mixer.Sound('sounds/do-you-like-what-you-see-start-game.wav')
SOUND_PRESS_START.set_volume(0.3)

SOUND_BEAT_TOP_BOTTOM_BORDER = pygame.mixer.Sound('sounds/woo-top-bottom-border.wav')
SOUND_BEAT_TOP_BOTTOM_BORDER.set_volume(0.3)


# Draw functions
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
    score_text = pygame.font.Font(None, 48).render(f'Score: {points}', True, color)
    screen.blit(
        score_text, pos
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
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20),
        radius=100,
        width=10
    )


def draw_start_menu():
    background, background_button, triangle_button_coord = start_menu.init_menu()

    screen.blit(background, (0, 0))

    pygame.draw.rect(
        surface=screen,
        color=start_menu.BACKGROUND_COLOR_BUTTON,
        rect=background_button,
        width=0,
        border_radius=4
    )

    pygame.draw.polygon(
        surface=screen,
        color=WHITE,
        points=triangle_button_coord
    )

    
def draw_round_winner(player: int, color: tuple, coord: tuple):
    screen.blit(
        pygame.font.Font(None, 60).render(f'Player {player + 1} wins!', True, color), coord
    )

    pygame.display.update()

# Respawn rackets and ball
def respawn_objects() -> None:
    left_racket.respawn_racket()
    right_racket.respawn_racket()

    game_ball.respawn_ball()


def reset_game(left_racket: racket.Racket, right_racket: racket.Racket):
    left_racket.game_win_handler()
    pygame.time.delay(3000)
    start_menu.flag = True
    respawn_objects()
    left_racket.player_points = 0
    right_racket.player_points = 0


# Window settings
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ping Pong')

# Create Clock object for setting framerate
delay = pygame.time.Clock()

# Create Rackets to play
left_racket = racket.Racket(
    x_pos=0,
    y_pos=SCREEN_HEIGHT // 2 - racket.Racket.HEIGHT // 2,
    UP_BUTTON=pygame.K_w, 
    DOWN_BUTTON=pygame.K_s,
    FLAG=0
)

right_racket = racket.Racket(
    x_pos=SCREEN_WIDTH - racket.Racket.WIDTH,
    y_pos=SCREEN_HEIGHT  // 2 - racket.Racket.HEIGHT // 2,
    UP_BUTTON=pygame.K_UP,
    DOWN_BUTTON=pygame.K_DOWN,
    FLAG=1
)

# Create ball
game_ball = ball.Ball(
    x_pos=SCREEN_WIDTH // 2,
    y_pos=SCREEN_HEIGHT // 2
)

# Create start menu
start_menu = start_menu.StartMenu(SCREEN_WIDTH, SCREEN_HEIGHT, True)

# Initialize game
while True:
    screen.fill(BACKGROUND_COLOR)

    #Draw Rackets
    draw_racket(left_racket)
    draw_racket(right_racket)

    # Draw middle line and circle
    draw_game_field()

    # Draw Ball
    draw_ball(game_ball)

    if start_menu.flag is True:
        draw_start_menu()

    # Get events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Event handler for start menu
    start_menu.event_handler(event)
    if start_menu.flag == True:
        continue

    # Event handler for ball
    game_ball.event_handler(left_racket, right_racket)

    # Event handler for 
    if left_racket.player_points == WIN_POINTS:
        SOUND_WIN_GAME.play()
        reset_game(left_racket, right_racket)
        continue

    elif right_racket.player_points == WIN_POINTS:
        SOUND_WIN_GAME.play()
        reset_game(left_racket, right_racket)
        continue
    
    # Get method result
    check_win_round = game_ball.round_win_handler(left_racket, right_racket)

    # Event handler for win round
    if check_win_round == left_racket.FLAG:
        draw_round_winner(check_win_round, RED, (150, 500))
        pygame.time.delay(1500)

        respawn_objects()

    elif check_win_round == right_racket.FLAG:
        draw_round_winner(check_win_round, BLUE, (750, 500))
        pygame.time.delay(1500)

        respawn_objects()

    # Draw counters
    draw_counter(left_racket.player_points, RED, (20, 10))
    draw_counter(right_racket.player_points, BLUE, (630, 10))

    # Get pressed keys mask
    key = pygame.key.get_pressed()

    # Event handler for rackets
    left_racket.event_handler(key)
    right_racket.event_handler(key)

    # Move ball
    game_ball.move()

    # Update display ;)
    pygame.display.update()
    delay.tick(FPS)