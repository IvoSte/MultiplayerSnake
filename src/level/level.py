class Structure:
    def __init__(self):
        self.pos = (0, 0)
        self.size = (0, 0)
        self.color = (0, 0, 0)


class Level:

    def __init__(self):
        self.structures = []
        self.objects = []

    def add_structure(self, structure):
        self.structures.append(structure)