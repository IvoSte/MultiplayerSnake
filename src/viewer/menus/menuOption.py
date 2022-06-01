from src.viewer.menus.baseMenuView import OptionValue


class MenuOption:

    def __init__(self, name, text, function = None, optionValue = None):
        self.name = name
        self.text = text
        self.function = function
        self.optionValue = optionValue