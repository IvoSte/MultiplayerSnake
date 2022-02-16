import random
import pygame
from colors import Color, turbo_color, color, extend_colormaps
from env_variables import PLAYER_SCORE_BOXES, SCREEN_SIZE_X, SCREEN_SIZE_Y, SNAKE_SIZE

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
        if PLAYER_SCORE_BOXES :
            self.display_players_information_boxes(players)
        else :
            self.display_player_information(players, self.display_player_score, 0, 0)
            self.display_player_information(players, self.display_snake_length, 500, 0)
            self.display_player_information(players, self.display_player_lives_left, 1000, 0)

    def display_player_information(self, players, display_function, x_offset, y_offset):
        positions = [[0 + x_offset, 0 + (20 * n) + y_offset] for n in range(len(players))]
        for idx, player in enumerate(players):
            display_function(player, positions[idx])

    def display_players_information_boxes(self, players):
        positions = [[0,0], [SCREEN_SIZE_X - 180, 0], [0, SCREEN_SIZE_Y - 90], [SCREEN_SIZE_X - 180, SCREEN_SIZE_Y - 90]]
        for idx, player in enumerate(players):
            text_color = color(player.colormap, player.color)
            self.display_player_information_box(player, positions[idx], text_color)

    def display_player_information_box(self, player, pos, color):
        length = pygame.font.SysFont("futura", 90).render(f"{player.length}", True, color)
        score =  pygame.font.SysFont("futura", 45).render(f"S {player.score}", True, color)
        eaten = pygame.font.SysFont("futura", 45).render(f"B {player.tails_eaten}", True, color)
        lives =  pygame.font.SysFont("garamond", 45).render(f" {'♥'*player.lives_left}", True, color)
        self.dis.blit(length, pos)
        self.dis.blit(score, [pos[0] + 105, pos[1]])
        self.dis.blit(eaten, [pos[0] + 105, pos[1] + 25])
        self.dis.blit(lives, [pos[0], pos[1] + 45])

    def display_player_score(self, player, position, color = Color.WHITE.value):
        value = self.score_font.render(f"{player.name} - points: {player.score}", True, color)
        self.dis.blit(value, position)

    def display_snake_length(self, player, position, color = Color.WHITE.value):
        value = self.score_font.render(f"tail length: {player.length}", True, color)
        self.dis.blit(value, position)

    def display_player_lives_left(self, player, position, color = Color.WHITE.value):
        value = self.score_font.render(f"lives: {player.lives_left}", True, color)
        self.dis.blit(value, position)


    def clear_screen(self):
        self.dis.fill(Color.BLUE.value)

    def render_sprite(self, sprite):
        pass

    def render_message(self, msg, color, relative_x, relative_y):
        msg = self.font_style.render(msg, True, color)
        self.dis.blit(msg, [self.display_size[0] * relative_x, self.display_size[1] * relative_y])

    def draw_snake(self, player):
        # Draw body
        for idx, pos in enumerate(player.body):
            pygame.draw.rect(self.dis, color(player.colormap, player.color + ((len(player.body) - idx) * player.colorscale)), [
                             pos[0], pos[1], self.snake_size[0], self.snake_size[1]])
        # Draw decaying body
        for idx, pos in enumerate(player.decaying_body):
            pygame.draw.rect(self.dis, player.decay_body_color[idx], [
                             pos[0], pos[1], self.snake_size[0], self.snake_size[1]])
            
    
    def draw_food(self, food):
        pygame.draw.rect(self.dis, food.color, [food.pos[0], food.pos[1], self.snake_size[0], self.snake_size[1]])

    def draw_environment(self, environment):
        for idx, agent in enumerate(environment.active_agents):
            #print(f"drawing agent {idx + 1}/{len(environment.active_agents)} at {agent.x_pos} {agent.y_pos}") #, end = '\r'
            pygame.draw.rect(self.dis, agent.color, [agent.x_pos, agent.y_pos, agent.size[0], agent.size[1]]) 
            