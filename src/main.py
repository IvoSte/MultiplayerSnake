from game.game import GameEngine
from game.event_manager import EventManager
from controls.controller import Controller
from viewer.viewer import Viewer
from networking.client import Client


def main():
    local = False
    abes_ip = "217.105.109.132"
    laptop_abe_local_ip = "192.168.1.104"
    home_port = 25565
    ivos_ip = "87.214.136.100"
    ivo_local = "192.168.1.101"
    local_ip = "localhost"
    ip_uni = "145.97.151.17"
    ip_uni_abe = "145.97.137.202"

    ip = ivos_ip
    port = home_port

    if local:
        print(" -- Running in LOCAL SYSTEM mode.")
        evManager = EventManager()
        game = GameEngine(evManager)
        controller = Controller(evManager, game)
        viewer = Viewer(evManager, game)
        game.on_startup_game()
        game.run()
    else:
        print(" -- Running in SERVER SYSTEM mode.")
        evManager = EventManager()
        game = GameEngine(evManager)
        client = Client(evManager, game, ip, port)
        controller = Controller(evManager, game)
        viewer = Viewer(evManager, game)
        game.on_startup_game()
        game.run()


if __name__ == "__main__":
    main()
