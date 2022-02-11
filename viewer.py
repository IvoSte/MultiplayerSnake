import pygame
from colors import Color

class Viewer():
    def __init__(self, snake_size=(10,10), display_size=(600,400), game_title="Multiplayer Snake Game - Extraordinaire"):
        # Set display
        self.display_size = display_size
        self.dis = pygame.display.set_mode((display_size[0], display_size[1]))
        pygame.display.set_caption(game_title)

        # Set fonts
        self.font_style = pygame.font.SysFont("bahnschrift", 25)
        self.score_font = pygame.font.SysFont("comicsansms", 35)
        
        # Snake Display variables
        self.snake_size = snake_size
        
    def update(self):
        pygame.display.update()

    def display_player_score(self, player):
        value = self.score_font.render(f"{player.name}: {player.score}", True, Color.YELLOW.value)
        # The player does not have 
        self.dis.blit(value, [0, 0])
    
    def clear_screen(self):
        self.dis.fill(Color.BLUE.value)

    def render_message(self, msg, color):
        msg = self.font_style.render(msg, True, color)
        self.dis.blit(msg, [self.display_size[0] / 6, self.display_size[1] / 3])

    def draw_snake(self, player):
        for pos in player.body:
            pygame.draw.rect(self.dis, Color.BLACK.value, [pos[0], pos[1], self.snake_size[0], self.snake_size[1]])
    
    def draw_food(self, food):
        pygame.draw.rect(self.dis, Color.GREEN.value, [food.pos[0], food.pos[1], self.snake_size[0], self.snake_size[1]])