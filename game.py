from player import Player
from viewer import Viewer
from state import State
from colors import Color, colormaps
from food import Food
from input_controls import inputHandler, Controls, player_1_controls, player_2_controls, general_controls, player_3_controls, player_4_controls
from env_variables import initial_food, number_of_players
import pygame
import time
import random


class Game():

    def __init__(self, display_size=(600,400)):
        # Global variables
        self.snake_size = (10,10)
        self.display_size = display_size

        # Call relevant init functions
        pygame.init()

        # Keep a clock
        self.clock = pygame.time.Clock()
        self.time_elapsed = 0
        
        # Initialize display
        self.viewer = Viewer(snake_size=self.snake_size, display_size=display_size)

        # Keep a list of all the players
        control_sets = [player_1_controls, player_2_controls, player_3_controls, player_4_controls]
        self.players = []
        for i in range(number_of_players):
            self.players.append(Player(
                display_size[0] / 2, display_size[1] / 2, speed=2, colormap = colormaps[i], name=f"p{i+1}", controls=control_sets[i]))
        
        # Set state
        self.state = State(game_over = False, in_end_screen = False, food = [])
    
    def spawn_food(self):
        foodx = round(random.randrange(0, self.display_size[0] - self.snake_size[0]) / 10.0) * 10.0
        foody = round(random.randrange(0, self.display_size[1] - self.snake_size[1]) / 10.0) * 10.0
        food = Food((foodx, foody), self)
        self.state.food.append(food)
        self.viewer.draw_food(food)

    def end_screen(self):
        # This function should be somewhere else and probably not a function, but for now its fine #TODO
        self.viewer.clear_screen()
        self.viewer.render_message("Match over! Press any key to quit", Color.RED.value)
        self.viewer.display_players_score(self.players)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print("Quitting game from end screen")
                self.state.game_over = True
                self.state.in_end_screen = False

    def parse_general_command(self, command):
        # Quit key
        if command == Controls.QUIT:
            self.state.game_over = True
        if command == Controls.PAUSE:
            self.pause_menu()

    def pause_menu(self):
        print("pause menu")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key in general_controls:
                    return
        return
                
    def players_alive(self) -> int:
        return sum(1 for player in self.players if player.alive)
        
    def run(self):
        # Pre game setup
        for _ in range(initial_food):
            self.spawn_food()

        # Loop
        while not self.state.game_over:
            if len(self.players) == 1 and self.players_alive() == 0 or\
                len(self.players) > 1 and self.players_alive() == 1:
                self.state.game_over = True
                self.state.in_end_screen = True

            ###  End Screen
            while self.state.in_end_screen == True:
                self.end_screen()

            ###  Main game
            # Clear screen function
            self.viewer.clear_screen()

            # Draw food
            for food in self.state.food:
                self.viewer.draw_food(food)

            # Read each input
            for event in pygame.event.get():
                # If the game is closed
                if event.type == pygame.QUIT:
                    self.state.game_over = True

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

            #if pygame.time.get_ticks() % player.speed == 0:
            # Move players snake
            for player in self.players:
                if not player.alive:
                    continue
                player.move()

                # TODO: This means it is game over for everyone if any one snake dies
                # Make it so that only that one snake dissappears and check if we have a winner
                
                player.is_dead(self.viewer.display_size, snakes=self.players)

                eaten_food = []
                for food in self.state.food:
                    if player.eat_food(food = food):
                        eaten_food.append(food)
                for food in eaten_food:
                    self.state.food.remove(food)

                player.update_body()
    
            for player in self.players:
                self.viewer.draw_snake(player)
            
            # Update score
            self.viewer.display_players_score(self.players)

            # Update screen
            self.viewer.update()
    
            # Move time forward
            self.time_elapsed = self.clock.tick(30)
    
        # Quit the game if the main game loop breaks
        pygame.quit()
        quit()
