import pygame

from viewer.colors import Color


class PauseMenuView:
    def __init__(self, viewer, menu):
        self.viewer = viewer
        self.menu = menu
        self.display_size = self.viewer.display_size
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.cursor_offset = -100

    def draw(self):
        self.draw_options()
        self.draw_cursor()

    def draw_options(self):
        # x = 0.5
        # y = 0.4
        # for state in self.menu.states:
        #     self.viewer.draw_test(state, Color.WHITE.value, x, y)
        #     y += 0.1
        self.viewer.draw_text("Press P to unpause", Color.WHITE.value, 0.5, 0.4)
        self.viewer.draw_text("Press Q to quit", Color.WHITE.value, 0.5, 0.5)
        self.viewer.draw_text("Press R to restart", Color.WHITE.value, 0.5, 0.6)
        self.viewer.draw_text("Press O for options", Color.WHITE.value, 0.5, 0.7)

    def draw_cursor(self):
        self.viewer.draw_text(
            "*", Color.WHITE.value, self.cursor_rect.x, self.cursor_rect.y
        )
