from game.env_variables import (
    PLAYER_SCORE_BOXES,
    RESOLUTION_SCALE,
    SCREEN_SIZE_X,
    SCREEN_SIZE_Y,
)
from viewer.colors import color
import pygame


class UI_player_information:
    def __init__(self, viewer):
        self.viewer = viewer

    def display_players_information(self, players):
        self.display_players_information_boxes(players)

    def display_players_information_boxes(self, players):
        positions = [[0.05, 0.05], [0.88, 0.05], [0.05, 0.95], [0.88, 0.95]]

        for idx, player in enumerate(players):
            text_color = color(player.colormap, player.color)
            self.display_player_information_box(player, positions[idx], text_color)

    def display_player_information_box(self, player, pos, color):
        self.viewer.draw_text(
            f"{player.length}",
            color,
            pos[0] - 0.05,
            pos[1] - 0.05,
            self.viewer.score_font_huge,
        )
        self.viewer.draw_text(
            f"S{player.score}",
            color,
            pos[0] + 0.05,
            pos[1] - 0.05,
            self.viewer.score_font_big,
        )
        self.viewer.draw_text(
            f"B{player.tails_eaten}",
            color,
            pos[0] + 0.05,
            pos[1],
            self.viewer.score_font_big,
        )
        self.viewer.draw_text(
            f"{'♥'*(player.lives_left + player.alive)}",
            color,
            pos[0] - 0.03,
            pos[1] + 0.03,
            self.viewer.symbols_font_big,
        )
