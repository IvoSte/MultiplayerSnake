from agent import Agent
from pygame import Color
from env_variables import AGENT_EFFECT_STEP_SIZE


class Env_agent(Agent):

    def __init__(self, x_pos, y_pos, size, color):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.size = size
        self.base_color = color
        self.color = color
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
        self.color = [x + ((y-x)/(255/AGENT_EFFECT_STEP_SIZE)) * ((255 - self.intensity)/AGENT_EFFECT_STEP_SIZE) for x, y in zip(Color(0, 255, 255), self.base_color)]

        if self.intensity == 250:
            self.infectious = True
        else : 
            self.infectious = False

    def decrease_intensity(self):
        self.intensity -= AGENT_EFFECT_STEP_SIZE
        if self.intensity < 0:
            self.reset()

    def reset(self):
        self.active = False
        self.intensity = 255

    def report(self):
        print(f"{self.x_pos = } {self.y_pos = }")