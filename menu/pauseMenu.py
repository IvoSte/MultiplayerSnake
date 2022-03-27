from input_controls import Controls, general_controls, menu_controls
from menu.baseMenu import BaseMenu
from colors import Color



class PauseMenu(BaseMenu):

    def __init__(self, game):
        BaseMenu.__init__(self, game)
        self.state = "unpause"
        self.states = ["unpause", "restart", "options", "quit"]
        self.menu_functions = {
            "unpause" : self.unpause,
            "restart" : self.game.restart_game,
            "options" : self.game.options_menu,
            "quit" : self.game.end_screen,
        }

    def draw_menu(self):
        print("drawing menu")
        self.game.viewer.draw_text("Press P to unpause", Color.WHITE.value, 0.5, 0.4)
        self.game.viewer.draw_text("Press Q to quit", Color.WHITE.value, 0.5, 0.5)
        self.game.viewer.draw_text("Press R to restart", Color.WHITE.value, 0.5, 0.6)
        self.game.viewer.draw_text("Press O for options", Color.WHITE.value, 0.5, 0.7)

    def menu_control(self, event):
        if menu_controls[event.key] == Controls.PAUSE:
            self.in_menu = False
        elif menu_controls[event.key] == Controls.QUIT:
            self.game.end_screen()
        elif menu_controls[event.key] == Controls.RESTART:
            self.game.restart_game()
        elif menu_controls[event.key] == Controls.OPTIONS:
            self.game.options_menu()
        elif menu_controls[event.key] == Controls.CONFIRM:
            self.menu_functions[self.state]
        else :
            self.move_cursor(menu_controls[event.key])

    def move_cursor(self, direction):
        if direction == Controls.UP:
            self.state = self.states[(self.states.index(self.state) - 1)]
            # TODO add MaartenFX sound
        if direction == Controls.DOWN:
            self.state = self.states[(self.states.index(self.state) + 1) % (len(self.states) - 1)]
            # TODO add MaartenFX sound

    def unpause(self):
        self.in_menu = False