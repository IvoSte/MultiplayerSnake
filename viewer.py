import random
import pygame
from colors import Color, turbo_color, color
from env_variables import SCREEN_SIZE_X, SCREEN_SIZE_Y, SNAKE_SIZE

class Viewer():
    def __init__(self, snake_size=(SNAKE_SIZE,SNAKE_SIZE), display_size=(SCREEN_SIZE_X,SCREEN_SIZE_Y), game_title="Multiplayer Snake Game - Extraordinaire"):
        # Set display
        self.display_size = display_size
        self.dis = pygame.display.set_mode((display_size[0], display_size[1]))
        pygame.display.set_caption(game_title)

        # Set fonts
        self.font_style = pygame.font.SysFont("bahnschrift", 35)
        #self.score_font = pygame.font.SysFont("comicsansms", 35)
        self.score_font = pygame.font.SysFont("futura", 35)

        # Snake Display variables
        self.snake_size = snake_size
        
    def update(self):
        pygame.display.update()



    # A bit obtuse way. Possibly better to print either per player, or per item itself.
    # This way is pretty workable for this stage. We can disable per column, and each player should
    # have the same information at all times.

    def display_players_information(self, players):
        self.display_player_information(players, self.display_player_score, 0, 0)
        self.display_player_information(players, self.display_snake_length, 250, 0)
        self.display_player_information(players, self.display_player_lives_left, 450, 0)

    def display_player_information(self, players, display_function, x_offset, y_offset):
        positions = [[0 + x_offset, 0 + (20 * n) + y_offset] for n in range(len(players))]
        for idx, player in enumerate(players):
            display_function(player, positions[idx])

    def display_player_score(self, player, position):
        value = self.score_font.render(f"{player.name} - points: {player.score}", True, Color.WHITE.value)
        self.dis.blit(value, position)

    def display_snake_length(self, player, position):
        value = self.score_font.render(f"tail length: {player.length}", True, Color.WHITE.value)
        self.dis.blit(value, position)

    def display_player_lives_left(self, player, position):
        value = self.score_font.render(f"lives: {player.lives_left}", True, Color.WHITE.value)
        self.dis.blit(value, position)


    def clear_screen(self):
        self.dis.fill(Color.BLUE.value)

    def render_sprite(self, sprite):
        pass

    def render_message(self, msg, color, relative_x, relative_y):
        msg = self.font_style.render(msg, True, color)
        self.dis.blit(msg, [self.display_size[0] * relative_x, self.display_size[1] * relative_y])

    def draw_snake(self, player):
        for idx, pos in enumerate(player.body):
            pygame.draw.rect(self.dis, color(player.colormap, player.color + (idx * player.colorscale)), [
                             pos[0], pos[1], self.snake_size[0], self.snake_size[1]])
    
    def draw_food(self, food):
        pygame.draw.rect(self.dis, food.color, [food.pos[0], food.pos[1], self.snake_size[0], self.snake_size[1]])

    def draw_environment(self, environment):
        for idx, agent in enumerate(environment.agents):
            print(f"drawing agent {idx}/{len(environment.agents)}", end = '\r')
            pygame.draw.rect(self.dis, pygame.Color(0, 0, 0), [agent.x_pos, agent.y_pos, agent.size[0], agent.size[1]]) 
            