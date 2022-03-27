import pygame
from colors import Color
from input_controls import Controls, general_controls, menu_controls

class BaseMenu():

    def __init__(self, game):
        self.game = game
        self.display_size = self.game.viewer.display_size
        self.in_menu = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.cursor_offset = - 100
        #self.menu_screen = pygame.Surface()

    def draw_cursor(self):
        self.game.viewer.draw_text('*', Color.WHITE.values, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.viewer.update()

    def display_menu(self):
        self.in_menu = True
        while self.in_menu:
            self.game.draw()
            # TODO Draw darkening screen over the game in the background
            self.draw_menu()
            pygame.display.update()
            self.parse_menu_input()

    def parse_menu_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key in menu_controls:
                self.menu_control(event)

    # class to override
    def draw_menu(self):
        pass

    # class to override
    def menu_control(self, event):
        pass


    