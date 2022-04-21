if __name__ == "__main__":
    import sys

    sys.path.append("..")


from _thread import start_new_thread
import socket
import uuid
import json
from src.networking.network_commands import (
    CreateGameCommand,
    DisconnectPlayerCommand,
    GetGameStateCommand,
    GetPlayerIDCommand,
    GetPlayerPositionsCommand,
    SendPlayerPositionCommand,
)

from src.networking.network_data_base import NetworkData
from src.networking.network_data import PlayerInfo, Message, UpdatePlayerPositionsData


class Server:
    def __init__(self, server_ip="localhost", port=25565):
        print("initializing server")
        self.server_ip = server_ip
        self.port = port
        self.addr = (self.server_ip, self.port)
        self.server = None
        self.bind_server(self.addr)
        self.connections = set()
        self.games = {}

    def bind_server(self, addr):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind(addr)
        except Exception as e:
            print(f"Failed to bind server: {e}")
        print("Server has been bounded")
        self.server.listen()

    def disconnect_player(self, player_id):
        # TODO delete any game if the game is empty
        # TODO remove player from game if it is not empty

        # delete connection
        to_delete = None
        for conn in self.connections:
            if conn[2] == player_id:
                to_delete = conn
        self.connections.remove(to_delete)

    def listen_for_connections(self):

        print("Listening for connections...")
        # Players can connect to the server. A connection is added to the connection list
        # PLayers are assigned a rondom ID
        # A thread is spawned per player
        while True:
            try:
                conn, addr = self.server.accept()
                # Generate random player id
                player_id = str(uuid.uuid4())
                self.connections.add((conn, addr, player_id))

                start_new_thread(self.client_thread, (conn, player_id))
            except KeyboardInterrupt:
                print("Shutting down...")
                exit()

    def send_to_all(self, packet):
        raise NotImplementedError("")

    def create_game(self, player_id):
        # TODO: create game
        raise NotImplementedError("")

    def client_thread(self, connection, player_id):
        """For each connected player, spawn a client thread. This now listens to
        calls from the client, connecting the client with the server."""
        print(f"Started a thread for client {player_id}")
        # on player connect
        connection.send(PlayerInfo(player_id).to_packet())

        while True:
            data = NetworkData.from_packet(connection.recv(4096))
            # If nothing got sent, wait
            if not data:
                continue

            print(data.command)

            if isinstance(data, CreateGameCommand):
                self.create_game(player_id)

            elif isinstance(data, GetGameStateCommand):
                msg = Message(
                    "Ivo kan beter smashen dan sommigen maar niet beter dan anderen."
                )
                connection.send(msg.to_packet())

            elif isinstance(data, GetPlayerIDCommand):
                connection.send(PlayerInfo(player_id).to_packet())

            elif isinstance(data, SendPlayerPositionCommand):
                print(f"SERVER: received player position: {data.player_position}")
                # TODO: Update gamestate of server for player positions

            # TODO: make command
            elif isinstance(data, GetPlayerPositionsCommand):
                # TODO: Get player positions from gamestate
                player_positions = {1: [1, 2, 3, 4, 5]}
                connection.send(UpdatePlayerPositionsData(player_positions).to_packet())

            elif isinstance(data, DisconnectPlayerCommand):
                self.disconnect_player(data.player_id)
                return

    def ping_connections(self):
        for connection in self.connections:
            connection.send()


if __name__ == "__main__":
    server = Server()
    server.listen_for_connections()
