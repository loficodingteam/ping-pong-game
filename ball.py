import pygame
import game
import random
import racket

class Ball:

    RADIUS: int = 15
    COLOR: tuple = (247, 174, 2)

    _SPEED: int = 5

    _ACCELERATION: int = _SPEED / 100 * 10

    def __init__(self, x_pos: int, y_pos: int) -> None:
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.last_racket = None

        self.init_speed()


    def init_speed(self) -> None:
        self.x_speed = random.choice([self._SPEED, self._SPEED * -1])
        self.y_speed = random.choice([self._SPEED, self._SPEED * -1])


    def move(self) -> None:
        self.x_pos += self.x_speed
        self.y_pos += self.y_speed


    def acceleration(self, x_pos: float, y_pos: float):
        self.x_speed = self.x_speed + self._ACCELERATION if self.x_speed > 0 else self.x_speed - self._ACCELERATION
        self.y_speed = self.y_speed + self._ACCELERATION if self.y_speed > 0 else self.y_speed - self._ACCELERATION


    def respawn_ball(self) -> None:
        self.x_pos = game.SCREEN_WIDTH // 2
        self.y_pos = game.SCREEN_HEIGHT // 2 - 20

        self.last_racket = None

        self.init_speed()
    

    def event_handler(self, left_racket: racket.Racket, right_racket: racket.Racket) -> None:
        left_border = self.x_pos - self.RADIUS
        right_border = self.x_pos + self.RADIUS
        top_border = self.y_pos - self.RADIUS
        bottom_border = self.y_pos + self.RADIUS

        if top_border <= 0:
            game.SOUND_HIT_TOP_BOTTOM_BORDER.play()
            self.y_speed *= -1

        if bottom_border >= game.SCREEN_HEIGHT:
            game.SOUND_HIT_TOP_BOTTOM_BORDER.play()
            self.y_speed *= -1

        # Collision for left_racket and ball
        if  left_racket.x_pos <= left_border <= left_racket.x_pos + left_racket.WIDTH + 1 and \
            left_racket.y_pos <= self.y_pos <= left_racket.y_pos + left_racket.HEIGHT + 1 and \
            self.last_racket != left_racket.FLAG:
            game.SOUND_HIT_THE_RACKET.play()

            self.last_racket = left_racket.FLAG

            self.x_speed *= -1

            self.acceleration(self.x_pos, self.y_pos)

        if top_border <= left_racket.y_pos + left_racket.HEIGHT and \
            left_racket.x_pos - left_racket.WIDTH <= left_border <= left_racket.x_pos + left_racket.WIDTH + 1 and \
            top_border >= left_racket.y_pos and \
            self.last_racket != left_racket.FLAG:
            game.SOUND_HIT_THE_RACKET.play()
            
            self.last_racket = left_racket.FLAG

            self.y_speed *= -1

            self.acceleration(self.x_pos, self.y_pos)

        if bottom_border >= left_racket.y_pos and \
            left_racket.x_pos - left_racket.WIDTH <= left_border <= left_racket.x_pos + left_racket.WIDTH + 1 and \
            top_border <= left_racket.y_pos + left_racket.HEIGHT and \
            self.last_racket != left_racket.FLAG:
            game.SOUND_HIT_THE_RACKET.play()

            self.last_racket = left_racket.FLAG

            self.y_speed *= -1

            self.acceleration(self.x_pos, self.y_pos)

        # Collision for right_racket and ball
        if right_racket.x_pos <= right_border <= right_racket.x_pos + right_racket.WIDTH + 1 and \
            right_racket.y_pos <= self.y_pos <= right_racket.y_pos + right_racket.HEIGHT + 1 and \
            self.last_racket != right_racket.FLAG:
            game.SOUND_HIT_THE_RACKET.play()

            self.last_racket = right_racket.FLAG

            self.x_speed *= -1

            self.acceleration(self.x_pos, self.y_pos)

        if top_border <= right_racket.y_pos + right_racket.HEIGHT and \
            right_racket.x_pos <= right_border <= right_racket.x_pos + right_racket.WIDTH * 2 + 1 and \
            top_border >= right_racket.y_pos and \
            self.last_racket != right_racket.FLAG:
            game.SOUND_HIT_THE_RACKET.play()

            self.last_racket = right_racket.FLAG

            self.y_speed *= -1

            self.acceleration(self.x_pos, self.y_pos)

        if bottom_border >= right_racket.y_pos and \
            right_racket.x_pos <= right_border <= right_racket.x_pos + right_racket.WIDTH * 2 + 1 and \
            top_border <= right_racket.y_pos + right_racket.HEIGHT and \
            self.last_racket != right_racket.FLAG:
            game.SOUND_HIT_THE_RACKET.play()

            self.last_racket = right_racket.FLAG
            
            self.y_speed *= -1

            self.acceleration(self.x_pos, self.y_pos)


    def round_win_handler(self, left_racket: racket.Racket, right_racket: racket.Racket) -> int:
        if self.x_pos > game.SCREEN_WIDTH:
            game.SOUND_HIT_LEFT_RIGHT_BORDER.play()

            left_racket.player_points += 1

            game.draw_counter(left_racket.player_points, game.RED, (20, 10))
            game.draw_counter(right_racket.player_points, game.BLUE, (630, 10))

            pygame.display.update()
            
            return left_racket.FLAG

        if self.x_pos <= 0:
            game.SOUND_HIT_LEFT_RIGHT_BORDER.play()

            right_racket.player_points += 1

            game.draw_counter(left_racket.player_points, game.RED, (20, 10))
            game.draw_counter(right_racket.player_points, game.BLUE, (630, 10))

            pygame.display.update()

            return right_racket.FLAG