from game.game import GameEngine
from game.eventmanager import EventManager
from viewer.viewer import Viewer


def main():
    evManager = EventManager()
    game = GameEngine(evManager)
    # controller = Controller(evManager, game)
    viewer = Viewer(evManager, game)
    game.init_game()
    game.run()


if __name__ == "__main__":
    main()
