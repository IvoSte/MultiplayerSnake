from player import Player
from viewer import Viewer
from state import State
from colors import Color
from food import Food
from input_controls import inputHandler, Controls, player_1_controls, player_2_controls, general_controls
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
        self.players = []
        self.players.append(Player(display_size[0] / 2, display_size[1] / 2, speed=2, name = "p1", controls= player_1_controls))
        #self.players.append(Player(display_size[0] / 3, display_size[1] / 2, speed=15, name = "p2",  controls= player_2_controls))
        
        # Set state
        self.state = State(game_over = False, in_end_screen = False, food = None)
    
    def spawn_food(self):
        foodx = round(random.randrange(0, self.display_size[0] - self.snake_size[0]) / 10.0) * 10.0
        foody = round(random.randrange(0, self.display_size[1] - self.snake_size[1]) / 10.0) * 10.0
        self.state.food = Food((foodx, foody), self)
        self.viewer.draw_food(self.state.food)

    def end_screen(self):
        # This function should be somewhere else and probably not a function, but for now its fine #TODO
        self.viewer.clear_screen()
        self.viewer.render_message("You Lost! Press any key to quit", Color.RED.value)
        self.viewer.display_player_score(self.players[0])
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
                

    def run(self):
        # Pre game setup
        self.spawn_food()

        # Loop
        while not self.state.game_over:

            ###  End Screen
            while self.state.in_end_screen == True:
                self.end_screen()

            ###  Main game
            # Clear screen function
            self.viewer.clear_screen()

            # Draw food
            self.viewer.draw_food(self.state.food)

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
                player.move()

                # TODO: This means it is game over for everyone if any one snake dies
                # Make it so that only that one snake dissappears and check if we have a winner
                if player.is_dead(self.viewer.display_size, snakes=self.players):
                    print("Long live the player")
                    self.state.game_over = True

                player.eat_food(food = self.state.food)
                player.update_body()
    
            for player in self.players:
                self.viewer.draw_snake(player)
            
            # Update score
            self.viewer.display_player_score(self.players[0])

            # Update screen
            self.viewer.update()
    
            # Move time forward
            self.elapsed = self.clock.tick(30)
    
        # Quit the game if the main game loop breaks
        pygame.quit()
        quit()
