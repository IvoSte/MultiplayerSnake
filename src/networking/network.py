if __name__ == "__main__":
    import sys

    sys.path.append("..")

import socket
import pickle
import json

from networking.network_data_base import NetworkData
from networking.network_commands import (
    CreateGameCommand,
    DisconnectPlayerCommand,
    GetGameStateCommand,
    GetPlayerIDCommand,
    SendPlayerPositionCommand,
    GetPlayerPositionsCommand,
    SendPlayerInputCommand,
    PlayerReadyCommand,
    PlayerUnreadyCommand,
    JoinGameCommand,
)
from networking.network_data import PlayerInfo


class Network:
    # interface between connection and server
    def __init__(self, server_ip="localhost", port=25565):
        print("initializing network")
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = server_ip
        self.port = port
        self.addr = (self.server_ip, self.port)
        self.player_id = self.connect_player()

    def get_player(self):
        # TODO: get player information as JSON
        return {"player_id": self.player_id.player_id}

    def connect_player(self):
        try:
            self.connection.connect(self.addr)
            player_data = NetworkData.from_packet(
                self.connection.recv(2048), type_def=PlayerInfo
            )
            return player_data
        except Exception as e:
            print(f"connect player error: {e}")

    def send_command(self, command: NetworkData):
        try:
            return self.connection.send(command.to_packet())
        except Exception as e:
            print(f"Network error for {command.command}: {e}")

    def join_game(self):
        print(f"Player trying to join is {self.get_player()}")
        return self.send_command(JoinGameCommand(self.get_player()))

    def get_player_id(self):
        return self.send_command(GetPlayerIDCommand())

    def get_game_state(self):
        return self.send_command(GetGameStateCommand())

    def disconnect_client(self, player_id):
        return self.send_command(DisconnectPlayerCommand(player_id))

    def create_game(self):
        return self.send_command(CreateGameCommand())

    def send_player_position(self, player_position: list):
        return self.send_command(SendPlayerPositionCommand(player_position))

    def get_player_positions(self):
        return self.send_command(GetPlayerPositionsCommand())

    def send_multiplayer_command(self, command):
        if isinstance(command, PlayerReadyCommand):
            self.send_player_ready()
        if isinstance(command, PlayerUnreadyCommand):
            self.send_player_unready()

    def send_player_ready(self):
        return self.send_command(PlayerReadyCommand())

    def send_player_unready(self):
        return self.send_command(PlayerUnreadyCommand())

    def start_game_if_players_are_ready(self):
        pass

    # NOTE: this is not used, remove
    def send(self, data):
        try:
            # TODO make this JSON format
            self.connection.send(str.encode(data))
            return pickle.loads(self.connection.recv(2048 * 2))
        except Exception as e:
            print(f"Send error: {e}")

    def send_player_input(self, player_name, player_input):
        return self.send_command(SendPlayerInputCommand(player_name, player_input))
