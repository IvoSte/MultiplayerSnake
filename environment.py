from environment_agent import Env_agent


class Environment:

    def __init__(self, size_x, size_y, unit_size, base_color):

        self.size_x = size_x
        self.size_y = size_y
        self.unit_size = unit_size

        # TODO this is a hacky way, but the actual good way does impose limits on e.g. the sizes. A more scalable approach would be good.
        self.units_x = int(size_x / float(unit_size[0]))
        self.units_y = int(size_y / float(unit_size[1]))
        self.base_color = base_color

        self.agents = self.init_agents()
    
    def init_agents(self):
        return [Env_agent(x,y, self.unit_size, self.base_color) for x in range(self.units_x) for y in range(self.units_y)]

