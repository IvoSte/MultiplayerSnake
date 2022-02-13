from agent import Agent

class Env_agent(Agent):

    def __init__(self, x_pos, y_pos, size, color):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.size = size
        self.color = color
    