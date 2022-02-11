from player import Player
from viewer import Viewer
from state import State
from colors import Color
from food import Food
from input_controls import inputHandler, Controls
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
        
        # Initialize display
        self.viewer = Viewer(snake_size=self.snake_size, display_size=display_size)

        # Keep a list of all the players
        self.players = []
        self.players.append(Player(display_size[0] / 2, display_size[1] / 2, speed=15))
        
        # Set state
        self.state = State(game_over = False, in_end_screen = False, food = None)
    
    def spawn_food(self):
        foodx = round(random.randrange(0, self.display_size[0] - self.snake_size[0]) / 10.0) * 10.0
        foody = round(random.randrange(0, self.display_size[1] - self.snake_size[1]) / 10.0) * 10.0
        self.state.food = Food((foodx, foody), self)
        self.viewer.draw_food(self.state.food)

    def run(self):
        # Pre game setup
        self.spawn_food()

        # Loop
        while not self.state.game_over:

            ###  End Screen
            while self.state.in_end_screen == True:
                self.viewer.clear_screen()
                self.viewer.render_message("You Lost! Press any key to quit", Color.RED.value)
                self.viewer.display_player_score(self.players[0])
                pygame.display.update()
    
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        print("Quitting game from end screen")
                        self.state.game_over = True
                        self.state.in_end_screen = False
    
            ###  Main game
            # Clear screen function
            self.viewer.clear_screen()

            # Draw food
            self.viewer.draw_food(self.state.food)
            
            for player in self.players:
                # Move the player
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.state.game_over = True

                    if event.type == pygame.KEYDOWN:
                        command = inputHandler(event)
                        # Quit key
                        if command == Controls.QUIT:
                            self.state.game_over = True
                            break
                        # Move
                        player.set_command(command)
                #if pygame.time.get_ticks() % player.speed == 0:
                player.move()

                # TODO: This means it is game over for everyone if any one snake dies
                # Make it so that only that one snake dissappears and check if we have a winner
                if player.is_dead(self.viewer.display_size, snakes=self.players):
                    print("Long live the player")
                    self.state.game_over = True

                player.eat_food(food = self.state.food)
                player.update_body()
    
            self.viewer.draw_snake(self.players[0])
            
            # Update score
            self.viewer.display_player_score(self.players[0])

            # Update screen
            self.viewer.update()
    
            # Move time forward
            self.clock.tick(15)
    
        # Quit the game if the main game loop breaks
        pygame.quit()
        quit()
