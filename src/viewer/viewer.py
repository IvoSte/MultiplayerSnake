import random
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
        self.font_style = pygame.font.SysFont("bahnschrift", 35)
        # self.score_font = pygame.font.SysFont("comicsansms", 35)
        self.score_font = pygame.font.SysFont("futura", 35)

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

        self.menus = {
            "PauseMenu": PauseMenuView,
            "OptionsMenu": OptionsMenuView,
            "GameplayOptionsMenu": GameplayOptionsMenuView,
            "SoundOptionsMenu": SoundOptionsMenuView,
            "ControlsOptionsMenu": ControlsOptionsMenuView,
            "GraphicsOptionsMenu": GraphicsOptionsMenuView,
            "PostGameMenu": PostGameMenuView,
        }

        self.background_switch_timer = None

        self.ui_player_information = UI_player_information(self)

    def update(self):
        pygame.display.update()

    def draw_game_timer(self, timer):
        # Start the countdown only after the game countdown
        if timer <= GAME_TIMER * TICKS_PER_SECOND:
            self.draw_counter_with_border(
                (timer // TICKS_PER_SECOND) + 1,
                ((SCREEN_SIZE_X // 2), (SCREEN_SIZE_Y) // 20),
                Color.WHITE.value,
                Color.BLACK.value,
                "futura",
                30 * RESOLUTION_SCALE,
            )

    def draw_player_counters(self, players):
        for player in players:
            if player.move_freeze_timer >= 10:
                self.draw_counter_with_border(
                    (player.move_freeze_timer // TICKS_PER_SECOND) + 1,
                    [player.x_pos, player.y_pos],
                    color(player.colormap, player.color),
                    Color.WHITE.value,
                    "futura",
                    60 * RESOLUTION_SCALE,
                )

    def draw_counter_with_border(self, value, pos, color, bordercolor, font, size):
        self.draw_text_with_border(
            value, (pos[0] - 10, pos[1] - 25), color, bordercolor, font, size
        )

    def draw_counter(self, value, pos, color, font, size):
        text = pygame.font.SysFont(font, size).render(f"{value}", True, color)
        self.display.blit(text, [pos[0], pos[1]])

    def draw_text_with_border(self, value, pos, color, bordercolor, font, size):
        border = pygame.font.SysFont(font, size).render(f"{value}", True, bordercolor)
        self.display.blit(border, [pos[0] + 2, pos[1]])
        self.display.blit(border, [pos[0] - 2, pos[1]])
        self.display.blit(border, [pos[0], pos[1] + 2])
        self.display.blit(border, [pos[0], pos[1] - 2])
        text = pygame.font.SysFont(font, size).render(f"{value}", True, color)
        self.display.blit(text, [pos[0], pos[1]])

    def clear_screen(self):
        self.display.fill(self.background_color)

    def draw_text(self, msg, color, relative_x, relative_y):
        msg = self.font_style.render(msg, True, color)
        self.display.blit(
            msg, [self.display_size[0] * relative_x, self.display_size[1] * relative_y]
        )

    def draw_text_bold(self, msg, color, relative_x, relative_y):
        self.font_style.set_bold(True)
        msg = self.font_style.render(msg, True, color)
        self.display.blit(
            msg, [self.display_size[0] * relative_x, self.display_size[1] * relative_y]
        )
        self.font_style.set_bold(False)

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
        self.menus[self.game.current_menu.name](self, self.game.current_menu).draw()

        self.update()
        # self.game.menu.draw_menu()  # this is bad, there should not be a draw function in a gameengine object
        # so it should be something like
        # self.draw_menu(self.game.menu). But we're here already.
        # then, do we draw all elements from the gameengine menu? is it an interpreter, or ready made thing?
