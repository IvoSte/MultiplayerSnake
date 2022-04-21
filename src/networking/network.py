if __name__ == "__main__":
    import sys

    sys.path.append("..")

import socket
import pickle
import json

from src.networking.network_data_base import NetworkData
from src.networking.network_commands import (
    CreateGameCommand,
    DisconnectPlayerCommand,
    GetGameStateCommand,
    GetPlayerIDCommand,
    SendPlayerPositionCommand,
    GetPlayerPositionsCommand,
)
from src.networking.network_data import PlayerInfo


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
        return self.player_id

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

    def send(self, data):
        try:
            # TODO make this JSON format
            self.connection.send(str.encode(data))
            return pickle.loads(self.connection.recv(2048 * 2))
        except Exception as e:
            print(f"Send error: {e}")
