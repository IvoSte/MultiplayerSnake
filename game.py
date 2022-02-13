from environment import Environment
from player import Player
from screens import set_end_screen
from viewer import Viewer
from state import State
from colors import Color, colormaps
from food import Food
from input_controls import inputHandler, Controls, player_1_controls, player_2_controls, general_controls, player_3_controls, player_4_controls
from env_variables import INITIAL_FOOD, NUMBER_OF_PLAYERS, INITIAL_LIVES, SCREEN_SIZE_X, SCREEN_SIZE_Y, \
    SNAKE_SIZE, INITIAL_SNAKE_LENGTH, SNAKE_SPEED
from screens import set_end_screen, set_pause_screen
import pygame
import time
import random


class Game():

    def __init__(self, display_size=(SCREEN_SIZE_X,SCREEN_SIZE_Y)):
        # Global variables
        self.snake_size = (SNAKE_SIZE,SNAKE_SIZE)
        self.display_size = display_size

        # Call relevant init functions
        pygame.init()

        # Keep a clock
        self.clock = pygame.time.Clock()
        self.time_elapsed = 0
        
        # Initialize display
        self.viewer = Viewer(snake_size=self.snake_size, display_size=display_size)

        # Keep a list of all the players
        self.control_sets = [player_1_controls, player_2_controls, player_3_controls, player_4_controls]
        self.players = []
        # food can be moved to the environment. For now the environment is intended to experiment with the background
        self.food = []
        self.environment = None

        # Set state
        self.state = State(game_over = False, in_end_screen = False, food = [])
    
    def init(self):
        # Pre game setup
        
        # Setup environment
        self.init_environment()

        # Create players
        self.init_players()
        
        # Grow food
        self.init_food()
        # Set state
        self.state = State(game_over = False, in_end_screen = False, food = [])
        
        # Spawn food

    def init_players(self):
        self.players = []
        for i in range(NUMBER_OF_PLAYERS):
            self.players.append(Player(
                self.display_size[0] / 2, self.display_size[1] / 2, width = SNAKE_SIZE, length = INITIAL_SNAKE_LENGTH, speed=SNAKE_SPEED, lives = INITIAL_LIVES, \
                    colormap = colormaps[[*colormaps][i]], name=f"{i+1} - {[*colormaps][i]}", controls=self.control_sets[i]))

    def init_environment(self):
        self.environment = Environment(self.display_size[0], self.display_size[1], self.snake_size, Color.BLUE.value)

    def init_food(self):
        self.food = []
        for _ in range(INITIAL_FOOD):
            self.spawn_food()

    def spawn_food(self):
        food_size = float(SNAKE_SIZE) 
        foodx = round(random.randrange(0, self.display_size[0] - self.snake_size[0]) / food_size) * food_size
        foody = round(random.randrange(0, self.display_size[1] - self.snake_size[1]) / food_size) * food_size
        food_color = pygame.Color(0, random.randint(200,255), 0)
        food = Food(self, (foodx, foody), food_color)
        self.food.append(food)

    def end_screen(self):
        # This function should be somewhere else and probably not a function, but for now its fine #TODO
        set_end_screen(self)
        self.viewer.display_players_information(self.players)

        pygame.display.update()
        in_end_screen = True
        while in_end_screen:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    print("Quitting game from end screen")
                    pygame.quit()
                    quit()

    def parse_general_command(self, command):
        # Quit key
        if command == Controls.QUIT:
            self.state.game_over = True
        if command == Controls.PAUSE:
            self.pause_menu()

    def restart_game(self):
        self.init()
        self.run()

    def pause_menu(self):
        set_pause_screen(self)
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key in general_controls:
                    if general_controls[event.key] == Controls.PAUSE:
                        return
                    if general_controls[event.key] == Controls.QUIT:
                        print("to end screen from pause screen")
                        self.end_screen()
                    if general_controls[event.key] == Controls.RESTART:
                        self.restart_game()

    def players_alive(self) -> int:
        return sum(1 for player in self.players if player.alive)
        
    def players_lives_left(self) -> int:
        active_lives = self.players_alive()
        reserve_lives = sum(player.lives_left for player in self.players)
        return active_lives + reserve_lives

    def is_game_over(self):
        if len(self.players) == 1 and self.players_lives_left() == 0 or\
            len(self.players) > 1 and self.players_lives_left() == 1:
            self.state.game_over = True
            self.state.in_end_screen = True


    def draw(self):
        self.viewer.clear_screen()

        # Draw background / environment
        #self.viewer.draw_environment(self.environment)

        # Draw food TODO draw items / draw entities
        for food in self.food:
            self.viewer.draw_food(food)

        # Draw players
        for player in self.players:
            self.viewer.draw_snake(player)

        # Update score
        self.viewer.display_players_information(self.players)

        # Update screen
        self.viewer.update()


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

    def update_players(self):
        # Move players snake
        for player in self.players:

            # If the player is dead, 
            if not player.alive:
                if player.lives_left > 0:
                    player.respawn()
                    player.lives_left -= 1
                continue
            player.move()

            player.is_dead(self.viewer.display_size, snakes=self.players)

            eaten_food = []
            for food in self.food:
                if player.eat_food(food = food):
                    eaten_food.append(food)
            for food in eaten_food:
                self.food.remove(food)

            player.update_body()

    def update(self):
        self.parse_input()
        self.update_players()

    def run(self):

        # Loop
        while not self.state.game_over:

            # Check if the game is over
            self.is_game_over()

            ###  Main game

            self.update()
            self.draw()
            
            # Move time forward
            self.time_elapsed = self.clock.tick(30)
    
        # Quit the game if the main game loop breaks
        pygame.quit()
        quit()
