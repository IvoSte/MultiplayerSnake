import pygame
from viewer.colors import Color
from controls.input_controls import Controls, general_controls, menu_controls

class BaseMenu():

    def __init__(self, game):
        self.game = game
        self.display_size = self.game.viewer.display_size
        self.in_menu = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.cursor_offset = - 100
        self.state = ""
        self.states = [""]
        #self.menu_screen = pygame.Surface()

    def draw_cursor(self):
        self.game.viewer.draw_text('*', Color.WHITE.values, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.viewer.update()

    def display_menu(self):
        self.in_menu = True
        while self.in_menu:
            self.game.draw()
            pygame.display.update()
            self.parse_menu_input()

    def parse_menu_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key in menu_controls:
                self.menu_control(event)

    # class to override
    def draw_menu(self):
        print("ERROR: Trying to draw a base menu.")
        pass

    # class to override
    def menu_control(self, event):
        if menu_controls[event.key] == Controls.PAUSE:
            self.quit_menu()
        elif menu_controls[event.key] == Controls.QUIT:
            self.game.end_screen()

    def quit_menu(self):
        self.in_menu = False

    def move_cursor(self, direction):
        if direction == Controls.UP:
            self.state = self.states[(self.states.index(self.state) - 1)]
            # TODO add MaartenFX sound
        if direction == Controls.DOWN:
            self.state = self.states[(self.states.index(self.state) + 1) % (len(self.states) - 1)]
            # TODO add MaartenFX sound

    