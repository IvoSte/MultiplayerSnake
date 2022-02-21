from colors import Color

def set_final_score(game, final_scores):
    for idx, (category, player) in enumerate(final_scores.items()):
        game.viewer.render_message(category, Color.WHITE.value, 0.3, 0.1 * (idx + 1))    
        game.viewer.render_message_bold(player.name, player.head_color, 0.5, 0.1 *  (idx + 1))    


def set_end_screen(game):
    game.viewer.clear_screen()
    game.viewer.render_message("Match over!", Color.WHITE.value, 0.5, 0.4)    
    game.viewer.render_message("Press Q to quit", Color.WHITE.value, 0.5, 0.5)
    game.viewer.render_message("Press R to restart", Color.WHITE.value, 0.5, 0.6)

def set_pause_screen(game):
    game.viewer.render_message("Press P to unpause", Color.WHITE.value, 0.5, 0.4)
    game.viewer.render_message("Press Q to quit", Color.WHITE.value, 0.5, 0.5)
    game.viewer.render_message("Press R to restart", Color.WHITE.value, 0.5, 0.6)
    game.viewer.render_message("Press O for options", Color.WHITE.value, 0.5, 0.7)
    

def set_options_screen(game):
    game.viewer.render_message("M enable/disable music", Color.WHITE.value, 0.05, 0.4)
    game.viewer.render_message("E enable/disable game sounds", Color.WHITE.value, 0.05, 0.5)
