from agent import Agent
from colormaps import generate_colormap
from colors import color, fade_colors, interpolate
from pygame import Color
from env_variables import AGENT_EFFECT_STEP_SIZE


class Env_agent(Agent):

    def __init__(self, x_pos, y_pos, size, color):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.size = size
        self.base_color = Color(50, 153, 213)
        self.top_color = Color(0,255,255)
        self.color = color
        self.colormap = generate_colormap(0, color.r, 255, color.g, 255, color.b)
        self.intensity = 255

        self.active = False
        self.infectious = False
        self.neighbours = []

    def set_neighbours(self, neighbours):
        self.neighbours += neighbours

    def activate(self):
        self.active = True

    def deactivate(self):
        self.reset()

    def update(self):
        self.decrease_intensity()
        self.color = fade_colors(self.top_color, self.base_color, 255/AGENT_EFFECT_STEP_SIZE, (255 - self.intensity)/AGENT_EFFECT_STEP_SIZE) 
        #self.color = color(self.colormap, 255 - self.intensity)
        if self.intensity == 250:
            self.infectious = True
        else : 
            self.infectious = False

    def set_top_color(self, color):
        self.color = color
        self.top_color = color

    def set_base_color(self, color):
        self.base_color = color

    def decrease_intensity(self):
        self.intensity -= AGENT_EFFECT_STEP_SIZE
        if self.intensity < 0:
            self.reset()

    def reset(self):
        self.active = False
        self.intensity = 255

    def report(self):
        print(f"{self.x_pos = } {self.y_pos = }")