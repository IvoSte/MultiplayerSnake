from controls.input_controls import Controls, general_controls, menu_controls
from menus.baseMenu import BaseMenu
from viewer.colors import Color



class PauseMenu(BaseMenu):

    def __init__(self, game):
        BaseMenu.__init__(self, game)
        self.state = "unpause"
        self.states = ["unpause", "restart", "options", "quit"]
        self.menu_functions = {
            "unpause" : self.quit_menu,
            "restart" : self.game.restart_game,
            "options" : self.game.options_menu,
            "quit" : self.game.end_screen,
        }

    def draw_menu(self):
        self.game.viewer.draw_text("Press P to unpause", Color.WHITE.value, 0.5, 0.4)
        self.game.viewer.draw_text("Press Q to quit", Color.WHITE.value, 0.5, 0.5)
        self.game.viewer.draw_text("Press R to restart", Color.WHITE.value, 0.5, 0.6)
        self.game.viewer.draw_text("Press O for options", Color.WHITE.value, 0.5, 0.7)

    def menu_control(self, event):
        if menu_controls[event.key] == Controls.PAUSE:
            self.quit_menu()
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

