import pygame

class StartMenu:

    BACKGROUND_COLOR: tuple = (102, 102, 102)
    BACKGROUND_COLOR_BUTTON: tuple = (200, 200, 200)

    def __init__(self, bg_width, bg_height, flag) -> None:
        self.BACKGROUND_WIDTH: int = bg_width
        self.BACKGROUND_HEIGHT: int = bg_height
        self.flag: bool = flag

    
    def init_menu(self) -> list:
        # Init background
        self.background = pygame.Surface((self.BACKGROUND_WIDTH, self.BACKGROUND_HEIGHT))
        self.background.fill(self.BACKGROUND_COLOR)
        self.background.set_alpha(150)

        # Init button background
        self.background_button = pygame.rect.Rect(550, 275, 100, 100)

        # Init button triangle
        self.triangle_button_coord = [[585, 300], [620, 325], [585, 350]]

        return self.background, self.background_button, self.triangle_button_coord


    def event_handler(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.flag == True:
            self.flag = False
        elif event.type != pygame.MOUSEBUTTONDOWN and self.flag == True:
            pygame.display.update()