import random
from viewer.colors import Color
from entities.environment_agent import Env_agent
from game.env_variables import NEIGHBOURHOOD_SHAPE

class Environment:

    def __init__(self, size_x, size_y, unit_size, base_color):

        self.size_x = size_x
        self.size_y = size_y
        self.unit_size = unit_size
        self.agents_x = size_x // unit_size[0]
        self.agents_y = size_y // unit_size[1]

        # TODO this is a hacky way, but the actual good way does impose limits on e.g. the sizes. A more scalable approach would be good.
        self.units_x = int(size_x / float(unit_size[0]))
        self.units_y = int(size_y / float(unit_size[1]))
        self.base_color = base_color

        # Easily transform location to position and back. Better to calculate once and then never again.
        self.loc_pos_transform = {} #{i : (((i % self.agents_x) * unit_size[0]), ((i // self.agents_x) * unit_size[1])) for i in range(len(self.agents))}
        self.pos_loc_transform = {} #{(((i % self.agents_x)* unit_size[0]), ((i // self.agents_x)) * unit_size[1]) : i for i in range(len(self.agents))}

        self.agents = []
        self.active_agents = set()


        self.neighbourhood_shape = NEIGHBOURHOOD_SHAPE

        #self.report_agents()

    def init_environment(self):
        self.agents = self.init_agents()
        self.set_agent_neighbours(self.agents)

    def init_agents(self):
        agents = []
        idx = 0
        for x in range(self.units_x):
            for y in range(self.units_y):
                x_pos = x * self.unit_size[0]
                y_pos = y * self.unit_size[1]
                agents.append(Env_agent(x_pos, y_pos, self.unit_size, self.base_color))
                self.loc_pos_transform[idx] = (x_pos, y_pos)
                self.pos_loc_transform[(x_pos, y_pos)] = idx
                idx += 1
        return agents
        #return [Env_agent(x * self.unit_size[0], y * self.unit_size[1], self.unit_size, self.base_color) for x in range(self.units_x) for y in range(self.units_y)]

    def report_agents(self):
        for agent in self.agents:
            agent.report()

    def set_agent_neighbours(self, agents):
        for agent in agents:
            agent.set_neighbours(self.get_neighbours(agent))

    def get_neighbours(self, agent):
        if self.neighbourhood_shape == 0:
            return self.get_von_neumann_neighbours(agent)
        else : 
            return self.get_moore_neighbours(agent)

    def get_moore_neighbours(self, agent):
        neighbours = []
        # Loop over all 
        for x in range(agent.x_pos - self.unit_size, agent.x_pos + (2 * self.unit_size), self.unit_size):
            for y in range(agent.x_pos - self.unit_size, agent.x_pos + (2 * self.unit_size), self.unit_size):
                if x == agent.x_pos and y == agent.y_pos or \
                    x < 0 or y < 0 or x > self.size_x or y > self.size_y:
                    continue
                neighbours.append(self.agents[self.pos_loc_transform[(x,y)]])
        return neighbours

    def get_von_neumann_neighbours(self, agent):
        neighbours = []
        if agent.x_pos + self.unit_size[0] < self.size_x:
            neighbours.append(self.agents[self.pos_loc_transform[(agent.x_pos + self.unit_size[0], agent.y_pos)]])
        if agent.x_pos - self.unit_size[0] >= 0:
            neighbours.append(self.agents[self.pos_loc_transform[(agent.x_pos - self.unit_size[0], agent.y_pos)]])
        if agent.y_pos + self.unit_size[1] < self.size_y:
            neighbours.append(self.agents[self.pos_loc_transform[(agent.x_pos, agent.y_pos + self.unit_size[1])]])
        if agent.y_pos - self.unit_size[1] >= 0:
            neighbours.append(self.agents[self.pos_loc_transform[(agent.x_pos, agent.y_pos - self.unit_size[1])]])
        return neighbours

    def activate_agents(self, agents):
        for agent in agents:
            self.activate_agent(agent)

    def activate_agent_on_position(self, pos):
        agent = self.agents[self.pos_loc_transform[pos]]
        #agent.set_top_color(random.choice([Color.BLUE.value, Color.WHITE.value, Color.YELLOW.value, Color.RED.value, Color.GREEN.value]))
        self.activate_agent(agent)

    def activate_agent_on_position_with_colormap(self, pos, colormap):
        agent = self.agents[self.pos_loc_transform[pos]]
        agent.colormap = colormap
        #agent.set_top_color(random.choice([Color.BLUE.value, Color.WHITE.value, Color.YELLOW.value, Color.RED.value, Color.GREEN.value]))
        self.activate_agent(agent)

    def activate_agent(self, agent):
        agent.activate()
        self.active_agents.add(agent)

    def pos_to_loc(self, pos):
        return (self.size_x * pos[1] + pos[0])

    def update_environment(self):
        agents_to_activate = []
        for agent in self.active_agents:
            agent.update()
            if agent.infectious :
                for other in agent.neighbours:
                    #other.set_top_color(agent.top_color)
                    #if not other.active:
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
