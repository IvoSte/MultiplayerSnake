from operator import attrgetter, length_hint
from entities.environment import Environment
from menus.baseMenu import BaseMenu
from menus.optionsMenu import OptionsMenu
from menus.pauseMenu import PauseMenu
from entities.player import Player
from entities.snake import Snake
from game.eventmanager import EventManager, TickEvent
from viewer.screens.screens import set_end_screen, set_final_score, set_options_screen
from audio.sounds import Sounds
from game.state import State
from viewer.colors import Color, colormaps, extend_colormaps
from entities.food import Food
from controls.input_controls import (
    controllerInputHandler,
    inputHandler,
    Controls,
    player_1_controls,
    player_2_controls,
    general_controls,
    player_3_controls,
    player_4_controls,
)
from game.env_variables import (
    BACKGROUND_VISUALS,
    DISABLE_MUSIC,
    FREEZE_FRAMES_ON_EAT,
    GAME_TIMER,
    GAME_TIMER_SWITCH,
    INITIAL_FOOD,
    NUMBER_OF_PLAYERS,
    INITIAL_LIVES,
    SCREEN_SIZE_X,
    SCREEN_SIZE_Y,
    SNAKE_SIZE,
    INITIAL_SNAKE_LENGTH,
    SNAKE_SPEED,
    START_COUNTDOWN,
    TICKS_PER_SECOND,
    WAVE_RATE,
)

import pygame
import time
import random


class GameEngine:
    def __init__(
        self, evManager: EventManager, display_size=(SCREEN_SIZE_X, SCREEN_SIZE_Y)
    ):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        # Global variables
        self.snake_size = (SNAKE_SIZE, SNAKE_SIZE)
        self.display_size = display_size

        # Call relevant init functions
        pygame.init()
        self.sounds = Sounds()
        # Keep a clock
        self.clock = pygame.time.Clock()
        self.time_elapsed = 0

        self.game_timer = (GAME_TIMER + START_COUNTDOWN) * TICKS_PER_SECOND

        # Keep a list of all the players
        self.control_sets = [
            player_1_controls,
            player_2_controls,
            player_3_controls,
            player_4_controls,
        ]
        self.controllers = {}
        self.players = []
        # food can be moved to the environment. For now the environment is intended to experiment with the background
        self.food = []
        self.environment = None

        # Set state
        self.state = State(
            game_over=False,
            in_end_screen=False,
            in_pause_menu=True,
            in_options_menu=False,
            in_game=True,
            in_menu=False,
            food=[],
        )
        # self.current_menu = BaseMenu(self)

    #### Game init -- Could be split to own file
    def init_game(self):
        # Pre game setup

        # initialize sound module
        self.init_sounds()

        # initialize controllers
        self.init_controllers()

        # Setup environment
        self.init_environment()

        # Create players
        self.init_players()

        # Grow food
        self.init_food()

        # Set game state
        self.state = State(
            game_over=False,
            in_end_screen=False,
            in_pause_menu=False,
            in_options_menu=False,
            in_game=True,
            in_menu=False,
            food=[],
        )
        self.game_timer = (GAME_TIMER + START_COUNTDOWN) * TICKS_PER_SECOND

    def init_sounds(self):
        self.sounds.init()
        if not DISABLE_MUSIC:
            self.sounds.play_music()
            self.sounds.set_music_volume(self.sounds.music_volume)

    def init_controllers(self):
        pygame.joystick.init()
        joysticks = [
            pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())
        ]
        for joystick in joysticks:
            joystick.init()
            # self.controllers[joystick.get_instance_id()] = joystick

    def init_players(self):
        self.players = []
        for i in range(NUMBER_OF_PLAYERS):
            self.players.append(
                Snake(
                    self.display_size[0] / 2,
                    self.display_size[1] / 2,
                    width=SNAKE_SIZE,
                    length=INITIAL_SNAKE_LENGTH,
                    speed=SNAKE_SPEED,
                    lives=INITIAL_LIVES,
                    colormap=colormaps[[*colormaps][i]],
                    name=f"{[*colormaps][i]}",
                    controls=self.control_sets[i],
                )
            )

    def init_environment(self):
        self.environment = Environment(
            self.display_size[0],
            self.display_size[1],
            self.snake_size,
            pygame.Color(50, 153, 213),
        )
        self.environment.init_environment()

    def init_food(self):
        self.food = []
        for _ in range(INITIAL_FOOD):
            self.spawn_food()

    def notify(self, event):
        pass
        # if isinstance(event, eventtype):
        #   action

    #### End game init

    def restart_game(self):
        self.init_game()
        self.run()

    def quit_game(self):
        pygame.quit()
        quit()

    def spawn_food(self):
        food_size = float(SNAKE_SIZE)
        foodx = (
            round(
                random.randrange(0, self.display_size[0] - self.snake_size[0])
                / food_size
            )
            * food_size
        )
        foody = (
            round(
                random.randrange(0, self.display_size[1] - self.snake_size[1])
                / food_size
            )
            * food_size
        )
        food_color = pygame.Color(0, random.randint(200, 255), 0)
        food = Food(self, (foodx, foody), food_color)
        self.food.append(food)

    def end_screen(self):
        # This function should be somewhere else and probably not a function, but for now its fine #TODO
        set_end_screen(self)
        set_final_score(self, self.get_final_score())
        # TODO this needs to be removed, ofcourse.
        # self.viewer.ui_player_information.display_players_information(self.players)

        pygame.display.update()
        in_end_screen = True
        while in_end_screen:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key in general_controls:
                    if general_controls[event.key] == Controls.RESTART:
                        self.restart_game()
                    else:
                        print("Quitting game from end screen")
                        self.quit_game()

    def pause_menu(self):
        self.state.in_game = False
        self.state.in_menu = True
        self.menu = PauseMenu(self)
        self.menu.display_menu()
        self.state.in_game = True
        self.state.in_menu = False

    def options_menu(self):
        self.state.in_game = False
        self.state.in_menu = True
        self.menu = OptionsMenu(self)
        self.menu.display_menu()
        self.state.in_game = True
        self.state.in_menu = False

    def options_menu_options(self, event):
        if general_controls[event.key] == Controls.MUSIC:
            if not self.sounds.music_paused:
                self.sounds.pause_music()
            else:
                self.sounds.unpause_music()
        if general_controls[event.key] == Controls.EFFECTS:
            if not self.sounds.effects_muted:
                self.sounds.mute_effects()
            else:
                self.sounds.unmute_effects()

    def parse_general_command(self, command):
        # Quit key
        if command == Controls.QUIT:
            self.state.game_over = True
        if command == Controls.PAUSE:
            self.pause_menu()

    def get_final_score(self):
        final_scores = {
            "Most points": max(self.players, key=attrgetter("score")),
            "Longest tail": max(self.players, key=attrgetter("length")),
            "Tails stolen": max(self.players, key=attrgetter("tails_eaten")),
        }
        return final_scores

    def players_alive(self) -> int:
        return sum(1 for player in self.players if player.alive)

    def players_lives_left(self) -> int:
        active_lives = self.players_alive()
        reserve_lives = sum(player.lives_left for player in self.players)
        return active_lives + reserve_lives

    def dead_players_lives_left(self) -> int:
        return sum(player.lives_left for player in self.players if not player.alive)

    def is_game_over(self):
        # In single player the player should be dead and have no lives left.
        # In multiplayer all players but on should be dead and without lives left.
        if (
            NUMBER_OF_PLAYERS == 1
            and self.players_lives_left() == 0
            or (
                NUMBER_OF_PLAYERS > 1
                and self.players_alive() == 1
                and self.dead_players_lives_left() == 0
            )
        ):
            self.state.game_over = True

        # Timer for timed games
        if GAME_TIMER_SWITCH and self.game_timer <= 0:
            self.state.game_over = True

    # TODO: Move to Input Manager
    def parse_input(self):
        # Read each input

        for event in pygame.event.get():
            # If the game is closed
            if event.type == pygame.QUIT:
                self.state.game_over = True
                self.end_screen()

            # If the event is a keypress
            if event.type == pygame.KEYDOWN:

                # Parse the keypress to a command
                if event.key in general_controls:
                    self.parse_general_command(general_controls[event.key])
                    break

                # Receive player command
                for player in self.players:
                    if event.key in player.controls:
                        player.set_command(player.controls[event.key])

            # TODO: This is needed to make the joystick work, but it makes no sense
            # This needs to be removed at some point (ideally)
            joysticks = [
                pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())
            ]
            if event.type == pygame.JOYAXISMOTION or event.type == pygame.JOYHATMOTION:
                command = controllerInputHandler(event)
                if command != None and len(self.players) - 1 >= event.instance_id:
                    self.players[event.instance_id + 1].set_command(command)

    def update_players(self):
        # Move players snake
        # Update players in random order
        for player in random.sample(self.players, len(self.players)):
            idx = self.players.index(player)
            # If the player is dead,
            if not player.alive:
                if player.lives_left > 0:
                    player.respawn()
                    player.lives_left -= 1
                continue
            player.move()

            player.is_dead(self.display_size, snakes=self.players)

            eaten_food = []
            for food in self.food:
                if player.eat_food(food=food):
                    player.move_freeze_timer = FREEZE_FRAMES_ON_EAT
                    eaten_food.append(food)
                    if random.random() < WAVE_RATE:
                        self.environment.activate_agent_on_position(food.pos)
                    self.sounds.play_player_effect(idx)
            for food in eaten_food:
                self.food.remove(food)

            player.update_body()

    def update(self):
        self.parse_input()
        self.update_players()
        self.environment.update_environment()

    def run(self):

        # Loop
        while not self.state.game_over:

            # Check if the game is over
            self.is_game_over()

            ###  Main game

            self.update()
            self.evManager.Post(TickEvent())

            # Move time forward
            self.time_elapsed = self.clock.tick(TICKS_PER_SECOND)
            if GAME_TIMER_SWITCH:
                self.game_timer -= 1

        self.end_screen()
        # Quit the game if the main game loop breaks
        self.quit_game()
