import pygame
import game

class Racket:

    WIDTH: int = 20
    HEIGHT: int = 150
    COLOR: tuple = (255, 255, 255)
    SPEED: int = 6

    def __init__(
            self,
            x_pos: int,
            y_pos: int,
            UP_BUTTON: int,
            DOWN_BUTTON: int,
            FLAG: int
    ) -> None:
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.UP_BUTTON = UP_BUTTON
        self.DOWN_BUTTON = DOWN_BUTTON
        self.FLAG = FLAG
        self.player_points = 0
    
    def respawn_racket(self) -> None:
        if self.FLAG == 0:
            self.x_pos = 0
            self.y_pos = game.SCREEN_HEIGHT // 2 - self.HEIGHT // 2
        
        elif self.FLAG == 1:
            self.x_pos = game.SCREEN_WIDTH - self.WIDTH
            self.y_pos = game.SCREEN_HEIGHT  // 2 - self.HEIGHT // 2
        

    def event_handler(self, key: pygame.key.ScancodeWrapper) -> None:
        if key[self.UP_BUTTON] and self.y_pos > 0:
            self.y_pos -= self.SPEED
        
        if key[self.DOWN_BUTTON] and self.y_pos < game.SCREEN_HEIGHT - self.HEIGHT:
            self.y_pos += self.SPEED
    

    def game_win_handler(self) -> None:
        game.screen.blit(
            pygame.font.Font(None, 82).render(f'Player {self.FLAG + 1} is winner!', True, (237, 176, 45)), (345, 450)
        )

        pygame.display.update()