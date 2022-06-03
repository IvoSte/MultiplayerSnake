from game.env_variables import PLAYER_SCORE_BOXES, RESOLUTION_SCALE, SCREEN_SIZE_X, SCREEN_SIZE_Y
from viewer.colors import color
import pygame

class UI_player_information:

    def __init__(self, viewer):
        self.viewer = viewer
        #self.text_large = pygame.font.SysFont("futura", 45 * RESOLUTION_SCALE)
        #self.text_medium = pygame.font.SysFont("futura", 22 * RESOLUTION_SCALE)
        #self.text_symbols = pygame.font.SysFont("garamond", 22 * RESOLUTION_SCALE)

    def display_players_information(self, players):
        self.display_players_information_boxes(players)

    def display_players_information_boxes(self, players):
        #positions = [[0,0], [SCREEN_SIZE_X - (90 * RESOLUTION_SCALE), 0], [0, SCREEN_SIZE_Y - (45 *  RESOLUTION_SCALE)], [SCREEN_SIZE_X - (90 * RESOLUTION_SCALE), SCREEN_SIZE_Y - (45 * RESOLUTION_SCALE)]]
        positions = [[0.1, 0.1], [0.9, 0.1], [0.1, 0.9], [0.9, 0.9]]
        
        for idx, player in enumerate(players):
            text_color = color(player.colormap, player.color)
            self.display_player_information_box(player, positions[idx], text_color)

    def display_player_information_box(self, player, pos, color):
        # self.viewer.draw_text()
        # length = self.viewer.text_font_large.render(f"{player.length}", True, color)
        # score =  self.viewer.text_font.render(f"S {player.score}", True, color)
        # eaten = self.viewer.text_font.render(f"B {player.tails_eaten}", True, color)
        # lives = self.viewer.symbols_font.render(f" {'♥'*(player.lives_left + player.alive)}", True, color)

        self.viewer.draw_score(
            f"{player.length}", color, pos[0] - 0.05, pos[1] - 0.05)
        self.viewer.draw_score(f"S {player.score}", color, pos[0], pos[1] - 0.05)
        self.viewer.draw_text_large(f"B {player.tails_eaten}", color, pos[0], pos[1])
        self.viewer.draw_unicode(f"{'♥'*(player.lives_left + player.alive)}", color, pos[0], pos[1])

        # self.viewer.display.blit(length, pos)
        # self.viewer.display.blit(score, [pos[0] + 52 * RESOLUTION_SCALE, pos[1]])
        # self.viewer.display.blit(eaten, [pos[0] + 52 * RESOLUTION_SCALE, pos[1] + 12 * RESOLUTION_SCALE])
        # self.viewer.display.blit(lives, [pos[0], pos[1] + 22 * RESOLUTION_SCALE])

    # def display_player_information(self, players, display_function, x_offset, y_offset):
    #     positions = [[0 + x_offset, 0 + (20 * n) + y_offset] for n in range(len(players))]
    #     for idx, player in enumerate(players):
    #         display_function(player, positions[idx])
