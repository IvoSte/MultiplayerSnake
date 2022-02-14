from environment_agent import Env_agent
from env_variables import NEIGHBOURHOOD_SHAPE

class Environment:

    def __init__(self, size_x, size_y, unit_size, base_color):

        self.size_x = size_x
        self.size_y = size_y
        self.unit_size = unit_size
        self.agents_x = size_x // unit_size[0]
        self.agents_y = size_y // unit_size[1]
        print(f"{self.agents_x} {self.agents_y}")

        # TODO this is a hacky way, but the actual good way does impose limits on e.g. the sizes. A more scalable approach would be good.
        self.units_x = int(size_x / float(unit_size[0]))
        self.units_y = int(size_y / float(unit_size[1]))
        self.base_color = base_color

        self.agents = self.init_agents()
        self.active_agents = set()

        self.neighbourhood_shape = NEIGHBOURHOOD_SHAPE

        # Easily transform location to position and back. Better to calculate once and then never again.
        self.loc_pos_transform = {i : (((i % self.agents_x) * unit_size[0]), ((i // self.agents_x) * unit_size[1])) for i in range(len(self.agents))}
        self.pos_loc_transform = {(((i % self.agents_x)* unit_size[0]), ((i // self.agents_x)) * unit_size[1]) : i for i in range(len(self.agents))}


    def init_agents(self):
        return [Env_agent(x,y, self.unit_size, self.base_color) for x in range(self.units_x) for y in range(self.units_y)]

    def set_agent_neighbours(self):
        for agent in self.agents:
            agent.set_neighbours(self.get_neighbours(agent))

    def get_neighbours(self, agent):
        if self.neighbourhood_shape == 0:
            return self.get_von_neumann_neighbours(agent)
        else : 
            return self.get_moore_neighbours(agent)

    def get_moore_neighbours(self, agent):
        neighbours = []
        # Loop over all 
        for x in range(agent.x_pos-1, agent.x_pos + 2):
            for y in range(agent.x_pos-1, agent.x_pos + 2):
                if x == agent.x_pos and y == agent.y_pos or \
                    x < 0 or y < 0 or x > self.size_x or y > self.size_y:
                    continue
                neighbours.append(self.agents[self.pos_loc_transform[(x,y)]])
        return neighbours        

    def get_von_neumann_neighbours(self, agent):
        neighbours = []
        neighbours.append(self.agents[self.pos_loc_transform[(agent.x_pos + 1,agent.y_pos)]])
        neighbours.append(self.agents[self.pos_loc_transform[(agent.x_pos - 1,agent.y_pos)]])
        neighbours.append(self.agents[self.pos_loc_transform[(agent.x_pos, agent.y_pos + 1)]])
        neighbours.append(self.agents[self.pos_loc_transform[(agent.x_pos, agent.y_pos - 1)]])
        return neighbours

    def activate_agents(self, pos):
        x = int(pos[0])
        y = int(pos[1])
        self.agents[self.pos_loc_transform[(x,y)]].activate()
        self.active_agents.add(self.agents[self.pos_loc_transform[pos]])

    def activate_agent(self, agent):
        agent.activate()
        self.active_agents.add(agent)

    def pos_to_loc(self, pos):
        return (self.size_x * pos[1] + pos[0])

    def update_environment(self):
        for agent in self.active_agents:
            agent.update()
            if agent.infectious :
                for other in agent.neighbours:
                    self.activate_agent(other)

        self.deactivate_agents()

    def deactivate_agents(self):
        deactivate_agents = []
        for agent in self.active_agents:
            if not agent.active:
                deactivate_agents.append(agent)
        for agent in deactivate_agents:
            self.active_agents.remove(agent)
