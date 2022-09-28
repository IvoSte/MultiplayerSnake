import random
from viewer.colors import Color
from entities.environment_agent import Env_agent
from game.config import config


class Environment:
    def __init__(self, size_x, size_y, unit_size, base_color):

        self.size_x = size_x
        self.size_y = size_y
        self.unit_size = unit_size

        self.units_x = size_x
        self.units_y = size_y
        self.base_color = base_color

        self.agents = []
        self.active_agents = set()

        self.neighbourhood_shape = config["COSMETIC"]["NEIGHBOURHOOD_SHAPE"]

        # self.report_agents()

    def init_environment(self):
        self.agents = self.init_agents()
        self.set_agent_neighbours(self.agents.values())

    def init_agents(self):
        agents = {
            (x_pos, y_pos): Env_agent(x_pos, y_pos, self.unit_size, self.base_color)
            for x_pos in range(self.units_x)
            for y_pos in range(self.units_y)
        }
        return agents

    def report_agents(self):
        for agent in self.agents.values():
            agent.report()

    def set_agent_neighbours(self, agents):
        for agent in agents:
            agent.set_neighbours(self.get_neighbours(agent))

    def get_neighbours(self, agent):
        if self.neighbourhood_shape == 0:
            return self.get_von_neumann_neighbours(agent)
        else:
            return self.get_moore_neighbours(agent)

    def get_moore_neighbours(self, agent):
        neighbours = []
        # Loop over all
        for x in range(agent.x_pos - 1, agent.x_pos + 2):
            for y in range(agent.x_pos - 1, agent.x_pos + 2):
                if (
                    x == agent.x_pos
                    and y == agent.y_pos
                    or x < 0
                    or y < 0
                    or x > self.size_x
                    or y > self.size_y
                ):
                    continue
                neighbours.append(self.agents[(x, y)])
        return neighbours

    def get_von_neumann_neighbours(self, agent):
        neighbours = []
        if agent.x_pos + 1 < self.size_x:
            neighbours.append(self.agents[(agent.x_pos + 1, agent.y_pos)])
        if agent.x_pos - 1 >= 0:
            neighbours.append(self.agents[(agent.x_pos - 1, agent.y_pos)])
        if agent.y_pos + 1 < self.size_y:
            neighbours.append(self.agents[(agent.x_pos, agent.y_pos + 1)])
        if agent.y_pos - 1 >= 0:
            neighbours.append(self.agents[(agent.x_pos, agent.y_pos - 1)])
        return neighbours

    def activate_agents(self, agents):
        for agent in agents:
            self.activate_agent(agent)

    def activate_agent_on_position(self, pos):
        agent = self.agents[pos]
        self.activate_agent(agent)

    def activate_agent_on_position_with_colormap(self, pos, colormap):
        agent = self.agents[pos]
        agent.colormap = colormap
        self.activate_agent(agent)

    def activate_agent(self, agent):
        agent.activate()
        self.active_agents.add(agent)

    def pos_to_loc(self, pos):
        return self.size_x * pos[1] + pos[0]

    def update_environment(self):
        agents_to_activate = []
        for agent in self.active_agents:
            agent.update()
            if agent.infectious:
                for other in agent.neighbours:
                    # other.set_top_color(agent.top_color)
                    # if not other.active:
                    agents_to_activate.append(other)
        self.activate_agents(agents_to_activate)
        self.deactivate_agents()

    def deactivate_agents(self):
        deactivate_agents = []
        for agent in self.active_agents:
            if not agent.active:
                deactivate_agents.append(agent)
        for agent in deactivate_agents:
            self.active_agents.remove(agent)
