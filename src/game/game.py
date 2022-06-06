from operator import attrgetter, length_hint
from game.gameModel import GameModel
from entities.environment import Environment
from menus.baseMenu import BaseMenu
from entities.player import Player
from entities.snake import Snake
from game.event_manager import EventManager, TickEvent, GetInputsEvent
from game.event_manager import GeneralControlInputEvent, PlayerInputEvent, QuitEvent
from game.event_manager import GamePausedEvent, RestartGameEvent
from game.event_manager import MenuControlInputEvent, GameEndedEvent
from menus.menuHandler import MenuHandler
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

        self.menuHandler = MenuHandler(self)

        self.model = GameModel()

        # Global variables
        self.snake_size = (SNAKE_SIZE, SNAKE_SIZE)
        self.display_size = display_size

        # Call relevant init functions
        pygame.init()
        self.sounds = Sounds()
        # Keep a clock
        self.clock = pygame.time.Clock()
        self.time_elapsed = 0

        # Keep a list of all the players
        self.control_sets = [
            player_1_controls,
            player_2_controls,
            player_3_controls,
            player_4_controls,
        ]
        self.controllers = {}
        # food can be moved to the environment. For now the environment is intended to experiment with the background
        self.environment = None

        # Set state
        self.state = State(
            running=True,
            game_over=False,
            game_paused=False,
            in_game=True,
            in_menu=False,
            food=[],
        )

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
            running=True,
            game_over=False,
            game_paused=False,
            in_game=True,
            in_menu=False,
            food=[],
        )
        self.model.set_game_timer((GAME_TIMER + START_COUNTDOWN) * TICKS_PER_SECOND)

    def reset_game(self):

        # Setup enviroment
        self.init_environment()

        # Spawn new snakes for the players
        self.reset_snakes()

        # Grow food
        self.init_food()

        # Set game state
        self.state = State(
            running=True,
            game_over=False,
            game_paused=False,
            in_game=True,
            in_menu=False,
            food=[],
        )
        self.model.set_game_timer((GAME_TIMER + START_COUNTDOWN) * TICKS_PER_SECOND)

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
        self.model.clear_players()
        self.model.clear_snakes()

        for i in range(NUMBER_OF_PLAYERS):
            snake = Snake(
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
            player = Player(
                name=f"{[*colormaps][i]}",
                snake=snake,
                controls=self.control_sets[i],
                snake_colormap=colormaps[[*colormaps][i]],
            )
            self.model.add_player(player)
            self.model.add_snake(snake)

    def init_environment(self):
        self.environment = Environment(
            self.display_size[0],
            self.display_size[1],
            self.snake_size,
            pygame.Color(50, 153, 213),
        )
        self.environment.init_environment()

    def init_food(self):
        self.model.clear_food()
        for _ in range(INITIAL_FOOD):
            self.spawn_food()

    def reset_snakes(self):
        self.model.clear_snakes()
        for player in self.model.players:
            snake = Snake(
                self.display_size[0] / 2,
                self.display_size[1] / 2,
                width=SNAKE_SIZE,
                length=INITIAL_SNAKE_LENGTH,
                speed=SNAKE_SPEED,
                lives=INITIAL_LIVES,
                colormap=player.snake_colormap,
                name=f"{player.name}",
                controls=player.controls,
            )
            player.set_snake(snake)
            self.model.add_snake(snake)

    def notify(self, event):
        if isinstance(event, QuitEvent):
            self.state.game_over = True
            self.state.running = False
            # self.end_screen()
        if isinstance(event, PlayerInputEvent):
            event.player.snake.set_command(event.command)

        if isinstance(event, GeneralControlInputEvent):
            if event.command == Controls.QUIT:
                self.state.game_over = True
                self.evManager.Post(QuitEvent())
            if event.command == Controls.PAUSE:
                self.state.game_paused = True
                self.evManager.Post(GamePausedEvent())
                self.menuHandler.pause_menu()
        if isinstance(event, RestartGameEvent):
            # TODO not sure why this is not reached when RestartGameEvent is sent.
            self.restart_game()
        if isinstance(event, MenuControlInputEvent):
            self.menuHandler.current_menu.menu_control(event.command)
            print(f"game notify {event} {event.command}")
        if isinstance(event, GameEndedEvent):
            self.menuHandler.postgame_menu()

    #### End game init

    def restart_game(self):
        self.reset_game()
        self.run()

    def quit_game(self):
        self.end_screen()
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
        self.model.food.append(food)

    def end_screen(self):
        pass

    def update_snakes(self):
        # Move snakes snake
        # Update snakes in random order
        for snake in random.sample(self.model.snakes, len(self.model.snakes)):
            idx = self.model.snakes.index(snake)
            # If the snake is dead,
            if not snake.alive:
                if snake.lives_left > 0:
                    snake.respawn()
                    snake.lives_left -= 1
                continue
            snake.move()

            snake.is_dead(self.display_size, snakes=self.model.snakes)

            eaten_food = []
            for food in self.model.food:
                if snake.eat_food(food=food):
                    snake.move_freeze_timer = FREEZE_FRAMES_ON_EAT
                    eaten_food.append(food)
                    if random.random() < WAVE_RATE:
                        self.environment.activate_agent_on_position(food.pos)
                    self.sounds.play_player_effect(idx)
            for food in eaten_food:
                self.model.remove_food(food)

            snake.update_body()

    def update(self):
        # self.parse_input()
        self.update_snakes()
        self.environment.update_environment()

    def run(self):

        # Loop
        while self.state.running:

            ###  Main game

            # Get and parse inputs
            self.evManager.Post(GetInputsEvent())

            if self.state.in_game:

                # Check if the game is over
                if self.model.is_game_over():
                    self.state.game_over = True
                    self.evManager.Post(GameEndedEvent())

                # Update game state according to inputs
                self.update()

                # Move time forward
                self.time_elapsed = self.clock.tick(TICKS_PER_SECOND)

                if GAME_TIMER_SWITCH:
                    self.model.game_timer -= 1

            # Update viewer and all other objects
            self.evManager.Post(TickEvent())

        # Quit the game if the main game loop breaks
        self.quit_game()
