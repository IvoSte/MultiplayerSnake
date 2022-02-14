from agent import Agent
from pygame import Color

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
        self.color = Color(255, 255, 255, self.intensity)

        if self.intensity == 100:
            print("I am infectious")
            self.infectious = True
        else : 
            self.infectious = False

    def decrease_intensity(self):
        self.intensity -= 1
        if self.intensity < 0:
            self.reset()

    def reset(self):
        self.active = False
        self.intensity = 255