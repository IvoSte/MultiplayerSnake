import os
import random
import sys
import pygame
from game.event_manager import TickEvent
from game.event_manager import EventManager
from game.game import GameEngine
from game.event_manager import GamePausedEvent
from viewer.menus.MultiplayerOptionsMenuView import MultiplayerOptionsMenuView
from viewer.menus.mainMenuView import MainMenuView
from viewer.menus.multiplayerLoadMenuView import MultiplayerLoadMenuView
from viewer.menus.multiplayerRoomMenuView import MultiplayerRoomMenuView
from viewer.menus.controlsOptionsMenuView import ControlsOptionsMenuView
from viewer.menus.gameplayOptionsMenuView import GameplayOptionsMenuView
from viewer.menus.graphicsOptionsMenuView import GraphicsOptionsMenuView
from viewer.menus.optionsMenuView import OptionsMenuView
from viewer.menus.soundOptionsMenuView import SoundOptionsMenuView
from viewer.menus.postGameMenuView import PostGameMenuView
from viewer.menus.pauseMenuView import PauseMenuView
from viewer.colors import Color, turbo_color, color_from_map, extend_colormaps
from viewer.ui_elements.player_information import UI_player_information
from game.config import config


class Viewer:
    def __init__(
        self,
        evManager: EventManager,
        game: GameEngine,
        snake_size=(
            config["GAME"]["SNAKE_SIZE"] * config["GAME"]["RESOLUTION_SCALE"],
            config["GAME"]["SNAKE_SIZE"] * config["GAME"]["RESOLUTION_SCALE"],
        ),
        display_size=(
            config["GAME"]["SCREEN_SIZE_X"] * config["GAME"]["RESOLUTION_SCALE"],
            config["GAME"]["SCREEN_SIZE_Y"] * config["GAME"]["RESOLUTION_SCALE"],
        ),
        game_title="Multiplayer Snake Game - Extraordinaire",
    ):

        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.game = game

        # Set display
        self.display_size = display_size
        if config["GAME"]["FULLSCREEN"]:
            self.display = pygame.display.set_mode(
                (display_size[0], display_size[1]), pygame.config["GAME"]["FULLSCREEN"]
            )
        else:
            self.display = pygame.display.set_mode((display_size[0], display_size[1]))
        pygame.display.set_caption(game_title)

        self.transparent_screen = pygame.Surface(self.display_size, pygame.SRCALPHA)
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
        # DEPRECIATED
        self.snake_size = snake_size

        # Size of units, x and y for a single grid thing. Base values, should be obtainable from objects themselves
        self.unit_size = (
            self.display_size[0] / self.game.model.grid_size[0],
            self.display_size[1] / self.game.model.grid_size[1],
        )

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
            "MainMenu": MainMenuView,
            "PauseMenu": PauseMenuView,
            "OptionsMenu": OptionsMenuView,
            "GameplayOptionsMenu": GameplayOptionsMenuView,
            "SoundOptionsMenu": SoundOptionsMenuView,
            "ControlsOptionsMenu": ControlsOptionsMenuView,
            "GraphicsOptionsMenu": GraphicsOptionsMenuView,
            "PostGameMenu": PostGameMenuView,
            "MultiplayerLoadMenu": MultiplayerLoadMenuView,
            "MultiplayerRoomMenu": MultiplayerRoomMenuView,
            "MultiplayerOptionsMenu": MultiplayerOptionsMenuView,
        }

        self.ui_player_information = UI_player_information(self)

    def update(self):
        self.display.blit(self.transparent_screen, (0, 0))
        pygame.display.update()

    def clear_screen(self):
        self.transparent_screen.fill(pygame.Color(0, 0, 0, 0))
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
        if (
            timer
            <= config["GAMEPLAY"]["GAME_TIMER"] * config["GAME"]["TICKS_PER_SECOND"]
        ):
            self.draw_text(
                msg=(timer // config["GAME"]["TICKS_PER_SECOND"]) + 1,
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
                    (player.x_pos * player.width, player.y_pos * player.width)
                )
                self.draw_text(
                    msg=(player.move_freeze_timer // config["GAME"]["TICKS_PER_SECOND"])
                    + 1,
                    color=color_from_map(player.colormap, player.color),
                    relative_x=relative_x,
                    relative_y=relative_y,
                    font=self.score_font_huge,
                    border=True,
                    bordercolor=Color.WHITE.value,
                )

    def draw_coordinates(self):
        for x in range(self.game.model.grid_size[0]):
            for y in range(self.game.model.grid_size[1]):
                pygame.draw.circle(
                    self.display,
                    Color.BLACK.value,
                    (
                        x * (self.display_size[0] / self.game.model.grid_size[0]),
                        y * (self.display_size[1] / self.game.model.grid_size[1]),
                    ),
                    1.0,
                )

    def rect_pixels_from_coords(self, x, y, size_x, size_y, x_offset=0.0, y_offset=0.0):
        # Retrieve the correct rectangle object parameters from grid coordinates.
        # Offset arguments can be used to shift when the game space is not
        # equal to the full display (e.g. with borders)
        x_offset = 0.5 * size_x
        y_offset = 0.5 * size_y
        return [
            (x * (self.display_size[0] / self.game.model.grid_size[0]))
            - (0.5 * size_x)
            + x_offset,
            (y * (self.display_size[1] / self.game.model.grid_size[1]))
            - (0.5 * size_y)
            + y_offset,
            size_x,
            size_y,
        ]

    def draw_snake(self, snake):
        if snake.is_ghost:
            display = self.transparent_screen
        else:
            display = self.display
        # Draw body
        for idx, pos in enumerate(snake.body):
            pygame.draw.rect(
                display,
                color_from_map(
                    snake.colormap,
                    snake.color + ((len(snake.body) - idx) * snake.colorscale),
                )
                + (100,),
                self.rect_pixels_from_coords(
                    pos[0],
                    pos[1],
                    self.unit_size[0],
                    self.unit_size[1],
                ),
            )
        # Draw shields
        # for idx in range(snake.length, max(0, snake.length - snake.shield_length), -1):
        #     self.draw_shield(snake.body[(idx * snake.body_segment_density) - 1])

        for idx, pos in enumerate(snake.body):
            if (
                snake.position_is_shielded(pos)
                # only draw one shield per block
                # BUGGED - ended here
                and idx - 1 % snake.body_segment_density == 0
            ):
                self.draw_shield(pos)

        # Draw decaying body
        for idx, pos in enumerate(snake.decaying_body):
            pygame.draw.rect(
                self.display,
                snake.decay_body_color[idx],
                self.rect_pixels_from_coords(
                    pos[0], pos[1], self.unit_size[0], self.unit_size[1]
                ),
            )

    def draw_shield(self, pos):
        x1, y1, x2, y2 = self.rect_pixels_from_coords(
            pos[0], pos[1], self.unit_size[0], self.unit_size[1]
        )
        pygame.draw.rect(
            self.transparent_screen,
            pygame.Color(14, 100, 180, 50),
            [x1, y1, x2, y2],
            border_radius=5,
        )
        pygame.draw.rect(
            self.transparent_screen,
            pygame.Color(103, 212, 240, 150),
            [x1 - 5, y1 - 5, x2 + 10, y2 + 10],
            width=5,
            border_radius=5,
        )

    def draw_food(self, food):
        pygame.draw.rect(
            self.display,
            food.color,
            self.rect_pixels_from_coords(
                food.pos[0], food.pos[1], self.unit_size[0], self.unit_size[1]
            ),
        )

    def draw_powerup(self, powerup):
        pygame.draw.rect(
            self.display,
            powerup.color,
            self.rect_pixels_from_coords(
                powerup.pos[0], powerup.pos[1], self.unit_size[0], self.unit_size[1]
            ),
        )

    def draw_environment(self, environment):
        for idx, agent in enumerate(environment.active_agents):
            # print(f"drawing agent {idx + 1}/{len(environment.active_agents)} at {agent.x_pos} {agent.y_pos}") #, end = '\r'
            pygame.draw.rect(
                self.display,
                agent.color,
                self.rect_pixels_from_coords(
                    agent.x_pos, agent.y_pos, self.unit_size[0], self.unit_size[1]
                ),
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
        if config["COSMETIC"]["BACKGROUND_VISUALS"]:
            self.draw_environment(self.game.environment)

        # Draw food TODO draw items / draw entities
        for food in self.game.model.food:
            self.draw_food(food)

        # Draw powerups
        for powerup in self.game.model.powerups:
            self.draw_powerup(powerup)

        # Draw players
        for snake in self.game.model.snakes:
            self.draw_snake(snake)

        # Update score
        self.ui_player_information.display_players_information(self.game.model.snakes)

        # Draw timers
        if config["GAMEPLAY"]["GAME_TIMER_SWITCH"]:
            self.draw_game_timer(self.game.model.game_timer)
        self.draw_player_counters(self.game.model.snakes)

        # Draw coordinates -- useful for development.
        if config["DEV"]["DRAW_COORDINATES"]:
            self.draw_coordinates()

        # Update screen
        self.update()

    def draw_menu(self):
        self.clear_screen()
        # TODO Draw darkening screen over the game in the background
        self.menus[self.game.menuHandler.current_menu.name](
            self, self.game.menuHandler.current_menu
        ).draw()
        # TODO tempoeary
        # self.ui_player_information.display_players_information(self.game.model.snakes)
        self.update()
        # self.game.menu.draw_menu()  # this is bad, there should not be a draw function in a gameengine object
        # so it should be something like
        # self.draw_menu(self.game.menu). But we're here already.
        # then, do we draw all elements from the gameengine menu? is it an interpreter, or ready made thing?
