from colors import Color

def set_end_screen(game):
    game.viewer.clear_screen()
    game.viewer.render_message("Match over!", Color.WHITE.value, 0.5, 0.4)    
    game.viewer.render_message("Press Q to quit", Color.WHITE.value, 0.5, 0.5)
    game.viewer.render_message("Press R to restart", Color.WHITE.value, 0.5, 0.6)

def set_pause_screen(game):
    game.viewer.render_message("Press P to unpause", Color.WHITE.value, 0.5, 0.4)
    game.viewer.render_message("Press Q to quit", Color.WHITE.value, 0.5, 0.5)
    game.viewer.render_message("Press R to restart", Color.WHITE.value, 0.5, 0.6)
    