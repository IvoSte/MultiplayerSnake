from colors import Color
from input_controls import Controls, menu_controls, general_controls
from menu.baseMenu import BaseMenu



class OptionsMenu(BaseMenu):

    def __init__(self, game):
        BaseMenu.__init__(self, game)
        self.state = "music"
        self.states = ["music", "game_sounds"]
        self.menu_functions = {
            "music" : self.unpause,
            "game_sounds" : self.game.restart_game,
        }

    def draw_menu(self):
        self.game.viewer.draw_text("M enable/disable music", Color.WHITE.value, 0.05, 0.4)
        self.game.viewer.draw_text("E enable/disable game sounds", Color.WHITE.value, 0.05, 0.5)

    def menu_control(self, event):
        if menu_controls[event.key] == Controls.PAUSE:
            self.quit_menu()
        elif menu_controls[event.key] == Controls.QUIT:
            self.game.end_screen()
        elif general_controls[event.key] == Controls.MUSIC:
            if not self.game.sounds.music_paused:
                self.game.sounds.pause_music()
            else :
                self.game.sounds.unpause_music()
        elif general_controls[event.key] == Controls.EFFECTS:
            if not self.game.sounds.effects_muted:
                self.game.sounds.mute_effects()
            else :
                self.game.sounds.unmute_effects()
        elif menu_controls[event.key] == Controls.CONFIRM:
            self.menu_functions[self.state]
        else :
            self.move_cursor(menu_controls[event.key])


    def unpause(self):
        self.in_menu = False