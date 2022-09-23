if __name__ == "__main__":
    import sys

    sys.path.append("..")

from dataclasses import dataclass
from distutils.log import info
import time
import keyboard

from game.event_manager import PlayerInputEvent, PlayerInputFromServerEvent

# Client depends on the Network
# from src.game.game import GameEngine
from networking.network import Network, NetworkData
from networking.network_commands import SendPlayerInputCommand
from networking.network_data import (
    UpdatePlayerPositionsData,
    PlayerInfo,
    GameState,
    PlayerJoinedNotification,
    ErrorNotification,
    GameStartNotification,
    RoomJoinedData,
    RoomCreatedData,
)

import threading

from game.event_manager import PlayerMultiplayerEvent


class Client:
    def __init__(self, evManager, game, server, port):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.game = game
        print("initializing client")
        # server assigns player ids
        # zoek naar de server, connect, get player_info
        self.network = Network(server, port)

        t = threading.Thread(target=self.listen, args=())
        t.daemon = True
        t.start()

        # receive game state, send to viewer
        # self.game_state = None
        # self.network.get_game_state()

        # self.player_id = None
        # self.network.get_player_id()

        # print(self.player_id)
        # print(self.game_state)
        # TODO: send player position on change in model

    def notify(self, event):
        if isinstance(event, PlayerInputEvent):
            self.network.send_player_input(event.player.name, event.command)
        if isinstance(event, PlayerMultiplayerEvent):
            print(f"received {event.command}")
            self.network.send_multiplayer_command(event.command)

    def listen(self):

        print("Listening from client...")
        while True:
            data = NetworkData.from_packet(self.network.connection.recv(4096))

            if isinstance(data, UpdatePlayerPositionsData):
                player_positions = data.player_list
                print(f"CLIENT: player positions= {player_positions}")

            if isinstance(data, RoomCreatedData):
                print(f"Created and connected to room with room code {data.room_code}")
                self.game.model.room_code = data.room_code
                self.game.menuHandler.multiplayer_room_menu()

            if isinstance(data, RoomJoinedData):
                print(f"Connected to room with room code {data.room_code}")
                self.game.model.room_code = data.room_code
                self.game.menuHandler.multiplayer_room_menu()

            if isinstance(data, GameStartNotification):
                print(f"Game has started...")
                # TODO: Start game
                self.game.init_game()
                # NOTE: Feels a bit iffy, but maybe this is how it should be

            if isinstance(data, PlayerJoinedNotification):
                print("Player has joined!")
                player_ids = data.total_player_list
                self.game.model.connected_player_ids = data.total_player_list
                print(f"{self.game.model.connected_player_ids=}")
                print(f"CLIENT: full player list= {player_ids}")

            if isinstance(data, ErrorNotification):
                print("ERROR - We received an error:")
                print(data.error_message)

            elif isinstance(data, GameState):
                print(f"{data=}")

            elif isinstance(data, PlayerInfo):
                print(f"{data=}")

            elif isinstance(data, SendPlayerInputCommand):
                player = self.game.model.get_player_from_name(data.player_name)
                if player is None:
                    print(f"No existing player with name {data.player_name}")
                    continue

                self.evManager.Post(
                    PlayerInputFromServerEvent(player=player, command=data.player_input)
                )

    def keep_alive(self):
        while True:
            try:
                time.sleep(5)
                continue
            except KeyboardInterrupt:
                print("Exiting from client.")
                exit()
        # g = GameEngine()
        # g.init_game()
        # g.run()

    def disconnect(self):
        self.network.disconnect_client(self.player_id)


if __name__ == "__main__":
    client = Client("localhost", 25565)
    client.keep_alive()
    # client.run()

    # TODO: Determine where the move command over the network is triggered
    # Is this gonna be in the client? in the model? with an event? not with an event but with direct coupling?
    # TODO: Determine how new information from the server is processed in the client,
    # Does is copy a state to itsself (all other players' positions are updated through new location information)
    # Or is the move exectuted through the gameengine (snake.move() is called on an entitiy)

    # def init():
    #     self.model = gameEngine
    #     self.controller = CONTROLLER
    #     self.network = network()

    # client:
    #     server message retrieved:
    #         UpdatePositionsEvent -> model.update_player_positions
    #         OR
    #         model.player_positions = client.player_positions

    # model:
    #     PlayerMovedEvent -> client.update_player_positions

    # def notify(self, event):
    #     # method one
    #     if isinstance(event, PlayerMoved):
    #         send new Location
    #     if isinstance(event, fruiteaten)
    #         send new fruit data

    #     # method two
    #     if isinstance(event, tickevent):
    #         get game state
    #         get player info
    #         handle all trafic
