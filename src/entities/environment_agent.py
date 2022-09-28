from enum import Enum
from entities.agent import Agent
from viewer.colormaps import generate_colormap
from viewer.colors import color, fade_colors, interpolate 
from pygame import Color
from game.config import config

class AgentMode(Enum):
    BIG_WAVE = 0
    SMALL_WAVE = 1
    BIG_WAVE_COLOR_SHIFT = 2

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

        self.mode = AgentMode.SMALL_WAVE

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
        if self.mode == AgentMode.BIG_WAVE:
            self.update_big_wave()  
        if self.mode == AgentMode.SMALL_WAVE:
            self.update_small_wave()

    def update_big_wave(self):
        self.decrease_intensity()
        self.color = fade_colors(self.top_color, self.base_color, 255/config['COSMETIC']['AGENT_EFFECT_STEP_SIZE'], (255 - self.intensity)/config['COSMETIC']['AGENT_EFFECT_STEP_SIZE']) 
        #self.color = color_from_map(self.colormap, 255 - self.intensity)
        self.infectious = self.intensity == 250

    def update_small_wave(self):
        self.decrease_intensity(100)
        self.color = fade_colors(self.top_color, self.base_color, 255/config['COSMETIC']['AGENT_EFFECT_STEP_SIZE'], (255 - self.intensity)/config['COSMETIC']['AGENT_EFFECT_STEP_SIZE']) 
        #self.color = color_from_map(self.colormap, 255 - self.intensity)
        self.infectious = self.intensity == 155

    def set_top_color(self, color):
        self.color = color
        self.top_color = color

    def set_base_color(self, color):
        self.base_color = color

    def decrease_intensity(self, decrease = config["COSMETIC"]["AGENT_EFFECT_STEP_SIZE"]):
        self.intensity -= decrease
        if self.intensity < 0:
            self.reset()

    def reset(self):
        self.active = False
        self.intensity = 255

    def report(self):
        print(f"{self.x_pos = } {self.y_pos = }")
