from menus.baseMenu import BaseMenu
from viewer.colors import Color

class MainMenu(BaseMenu):

    def __init__(self, game):
        BaseMenu.__init__(self, game)

        self.state = "Start"
        self.start_x, self.start_y = self.display_size[0], self.display_size[1] + 30
        self.options_x, self.options_y = self.display_size[0], self.display_size[1] + 50
        self.credits_x, self.credits_y = self.display_size[0], self.display_size[1] + 70
        self.cursor_rect.midtop = (self.start_x + self.cursor_offset, self.start_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Main Menu', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text("Start Game", 20, self.startx, self.starty)
            self.game.draw_text("Options", 20, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()