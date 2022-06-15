from game.game import GameEngine
from game.event_manager import EventManager
from controls.controller import Controller
from viewer.viewer import Viewer
from networking.client import Client


def main():
    local = False

    if local:
        print(" -- Running in LOCAL SYSTEM mode.")
        evManager = EventManager()
        game = GameEngine(evManager)
        controller = Controller(evManager, game)
        viewer = Viewer(evManager, game)
        game.init_game()
        game.run()
    else:
        print(" -- Running in SERVER SYSTEM mode.")
        evManager = EventManager()
        game = GameEngine(evManager)
        client = Client(evManager, game, "localhost", 25565)
        controller = Controller(evManager, game)
        viewer = Viewer(evManager, game)
        game.init_game()
        game.run()


if __name__ == "__main__":
    main()
