import os
import random
import sys
import pygame
from game.event_manager import TickEvent
from game.event_manager import EventManager
from game.game import GameEngine
from game.event_manager import GamePausedEvent
from viewer.menus.controlsOptionsMenuView import ControlsOptionsMenuView
from viewer.menus.gameplayOptionsMenuView import GameplayOptionsMenuView
from viewer.menus.graphicsOptionsMenuView import GraphicsOptionsMenuView
from viewer.menus.optionsMenuView import OptionsMenuView
from viewer.menus.soundOptionsMenuView import SoundOptionsMenuView
from viewer.menus.postGameMenuView import PostGameMenuView
from viewer.menus.pauseMenuView import PauseMenuView
from viewer.colors import Color, turbo_color, color, extend_colormaps
from game.env_variables import (
    FULLSCREEN,
    GAME_TIMER,
    GAME_TIMER_SWITCH,
    PLAYER_SCORE_BOXES,
    RESOLUTION_SCALE,
    SCREEN_SIZE_X,
    SCREEN_SIZE_Y,
    SNAKE_SIZE,
    TICKS_PER_SECOND,
    VERZET,
    BACKGROUND_VISUALS,
)
from viewer.ui_elements.player_information import UI_player_information


class Viewer:
    def __init__(
        self,
        evManager: EventManager,
        game: GameEngine,
        snake_size=(SNAKE_SIZE, SNAKE_SIZE),
        display_size=(SCREEN_SIZE_X, SCREEN_SIZE_Y),
        game_title="Multiplayer Snake Game - Extraordinaire",
    ):

        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.game = game

        # Set display
        self.display_size = display_size
        if FULLSCREEN:
            self.display = pygame.playplay.set_mode(
                (display_size[0], display_size[1]), pygame.FULLSCREEN
            )
        else:
            self.display = pygame.display.set_mode((display_size[0], display_size[1]))
        pygame.display.set_caption(game_title)

        # self.screen = pygame.Surface()

        # Set fonts
        # Old fonts, for reference
        # self.text_font = pygame.font.SysFont("bahnschrift", 35)
        # self.score_font = pygame.font.SysFont("futura", 35)

        # For symbols list check https://freefontsdownload.net/free-segoeuisymbol-font-135679.htm
        self.text_font_path = os.path.join("assets", "fonts", "seguisym.ttf")
        self.symbols_font_path = os.path.join("assets", "fonts", "seguisym.ttf")
        self.score_font_path = os.path.join(
            "assets", "fonts", "futura.ttf"
        )  # quickens.ttf

        self.text_font = pygame.font.Font(self.text_font_path, 35)
        self.text_font_big = pygame.font.Font(self.text_font_path, 45)
        self.text_font_large = pygame.font.Font(self.text_font_path, 60)
        self.text_font_huge = pygame.font.Font(self.text_font_path, 90)

        self.score_font = pygame.font.Font(self.score_font_path, 35)
        self.score_font_big = pygame.font.Font(self.score_font_path, 45)
        self.score_font_large = pygame.font.Font(self.score_font_path, 60)
        self.score_font_huge = pygame.font.Font(self.score_font_path, 90)

        self.symbols_font = pygame.font.Font(self.symbols_font_path, 35)
        self.symbols_font_big = pygame.font.Font(self.symbols_font_path, 45)
        self.symbols_font_large = pygame.font.Font(self.symbols_font_path, 60)
        self.symbols_font_huge = pygame.font.Font(self.symbols_font_path, 90)

        # Snake Display variables
        self.snake_size = snake_size

        self.background_color = Color.BLUE.value
        self.background_colors = [
            Color.WHITE.value,
            Color.BLUE.value,
            Color.YELLOW.value,
            Color.RED.value,
            Color.GREEN.value,
        ]

        # Linking the menu to the menuView object
        self.menus = {
            "PauseMenu": PauseMenuView,
            "OptionsMenu": OptionsMenuView,
            "GameplayOptionsMenu": GameplayOptionsMenuView,
            "SoundOptionsMenu": SoundOptionsMenuView,
            "ControlsOptionsMenu": ControlsOptionsMenuView,
            "GraphicsOptionsMenu": GraphicsOptionsMenuView,
            "PostGameMenu": PostGameMenuView,
        }

        self.ui_player_information = UI_player_information(self)

    def update(self):
        pygame.display.update()

    def clear_screen(self):
        self.display.fill(self.background_color)

    def absolute_to_relative_position(
        self, pos: tuple[int, int]
    ) -> tuple[float, float]:
        # Convert absolute x and y positions to relative x and y positions
        return (pos[0] / self.display_size[0], pos[1] / self.display_size[1])

    def relative_to_absolute_position(self, relative_x, relative_y) -> tuple[int, int]:
        # Convert relative x and y positions to absolute x and y positions
        return (relative_x * self.display_size[0], relative_y * self.display_size[1])

    def draw_text(
        self,
        msg,
        color,
        relative_x,
        relative_y,
        font=None,
        border=False,
        bordercolor=None,
    ):
        # Make sure the message is a string
        if not isinstance(msg, str):
            msg = f"{msg}"
        # If no font is given as argument, use the default text font
        if font == None:
            font = self.text_font
        # Draw the border before the message
        if border:
            self.draw_text_border(msg, relative_x, relative_y, bordercolor, font)
        # Draw the message to the screen
        msg = font.render(msg, True, color)
        self.display.blit(
            msg, [self.display_size[0] * relative_x, self.display_size[1] * relative_y]
        )

    def draw_text_border(self, msg, relative_x, relative_y, bordercolor, font):
        # This function needs to be rewrote at some point TODO -- instead of making 9
        # prints around the value, a better way is to get a circle of points
        if bordercolor == None:
            bordercolor = Color.WHITE.value
        border = font.render(msg, True, bordercolor)
        offset = 0.003

        for x_offset in [-1 * offset, 0, offset]:
            for y_offset in [-1 * offset, 0, offset]:
                self.display.blit(
                    border,
                    [
                        (self.display_size[0] * (relative_x + x_offset)),
                        (self.display_size[1] * (relative_y + y_offset)),
                    ],
                )

    # DEPRECIATED -- Should be called by a regular draw_text with a bold font.
    def draw_text_bold(self, msg, color, relative_x, relative_y):
        self.text_font.set_bold(True)
        msg = self.text_font.render(msg, True, color)
        self.display.blit(
            msg, [self.display_size[0] * relative_x, self.display_size[1] * relative_y]
        )
        self.text_font.set_bold(False)

    def draw_game_timer(self, timer):
        # Start the countdown only after the game countdown
        if timer <= GAME_TIMER * TICKS_PER_SECOND:
            self.draw_text(
                msg=(timer // TICKS_PER_SECOND) + 1,
                color=Color.WHITE.value,
                relative_x=0.48,
                relative_y=0.02,
                font=self.score_font_large,
                border=True,
                bordercolor=Color.BLACK.value,
            )

    def draw_player_counters(self, players):
        for player in players:
            if player.move_freeze_timer >= 10:
                relative_x, relative_y = self.absolute_to_relative_position(
                    (player.x_pos, player.y_pos)
                )
                self.draw_text(
                    msg=(player.move_freeze_timer // TICKS_PER_SECOND) + 1,
                    color=color(player.colormap, player.color),
                    relative_x=relative_x,
                    relative_y=relative_y,
                    font=self.score_font_big,
                    border=True,
                    bordercolor=Color.WHITE.value,
                )

    def draw_snake(self, player):
        # Draw body
        for idx, pos in enumerate(player.body):
            pygame.draw.rect(
                self.display,
                color(
                    player.colormap,
                    player.color + ((len(player.body) - idx) * player.colorscale),
                ),
                [pos[0], pos[1], self.snake_size[0], self.snake_size[1]],
            )
        # Draw decaying body
        for idx, pos in enumerate(player.decaying_body):
            pygame.draw.rect(
                self.display,
                player.decay_body_color[idx],
                [pos[0], pos[1], self.snake_size[0], self.snake_size[1]],
            )

    def draw_food(self, food):
        pygame.draw.rect(
            self.display,
            food.color,
            [food.pos[0], food.pos[1], self.snake_size[0], self.snake_size[1]],
        )

    def draw_environment(self, environment):
        for idx, agent in enumerate(environment.active_agents):
            # print(f"drawing agent {idx + 1}/{len(environment.active_agents)} at {agent.x_pos} {agent.y_pos}") #, end = '\r'
            pygame.draw.rect(
                self.display,
                agent.color,
                [agent.x_pos, agent.y_pos, agent.size[0], agent.size[1]],
            )

    def notify(self, event):
        if isinstance(event, TickEvent):
            if self.game.state.in_game:
                self.draw_game()
            if self.game.state.in_menu:
                self.draw_menu()
        if isinstance(event, GamePausedEvent):
            pass

    def draw_game(self):
        self.clear_screen()

        # Draw background / environment
        if BACKGROUND_VISUALS:
            self.draw_environment(self.game.environment)

        # Draw food TODO draw items / draw entities
        for food in self.game.food:
            self.draw_food(food)

        # Draw players
        for player in self.game.players:
            self.draw_snake(player)

        # Update score
        self.ui_player_information.display_players_information(self.game.players)

        # Draw timers
        if GAME_TIMER_SWITCH:
            self.draw_game_timer(self.game.game_timer)
        self.draw_player_counters(self.game.players)

        # Update screen
        self.update()

    def draw_menu(self):
        self.clear_screen()
        # TODO Draw darkening screen over the game in the background
        self.menus[self.game.menuHandler.current_menu.name](
            self, self.game.menuHandler.current_menu
        ).draw()

        self.update()
        # self.game.menu.draw_menu()  # this is bad, there should not be a draw function in a gameengine object
        # so it should be something like
        # self.draw_menu(self.game.menu). But we're here already.
        # then, do we draw all elements from the gameengine menu? is it an interpreter, or ready made thing?
