if __name__ == "__main__":
    import sys

    sys.path.append("..")


import threading
from logger import log
import socket
import uuid
import json
from networking.network_commands import (
    CreateRoomCommand,
    DisconnectPlayerCommand,
    GetGameStateCommand,
    GetPlayerIDCommand,
    GetPlayerPositionsCommand,
    SendPlayerPositionCommand,
    SendPlayerInputCommand,
    PlayerReadyCommand,
    PlayerUnreadyCommand,
    StartGameCommand,
    JoinRoomCommand,
)

from networking.room_manager import RoomManager

from networking.network_data_base import NetworkData
from networking.network_data import (
    PlayerInfo,
    Message,
    UpdatePlayerPositionsData,
    PlayerJoinedNotification,
    ErrorNotification,
    GameStartNotification,
    RoomJoinedData,
    RoomCreatedData,
)


class Server:
    def __init__(self, server_ip="192.168.1.104", port=25565):
        print("initializing server")
        self.server_ip = server_ip
        self.port = port
        self.addr = (self.server_ip, self.port)
        self.server = None
        self.bind_server(self.addr)
        self.connections = set()
        self.games = {}
        self.room_manager = RoomManager()
        # self.log = []

    def bind_server(self, addr):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind(addr)
        except Exception as e:
            raise Exception(f"Failed to bind server: {e}")
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
            except KeyboardInterrupt:
                print("Shutting down...")
                exit()
            # Generate random player id
            player_id = str(uuid.uuid4())
            self.connections.add((conn, addr, player_id))

            t = threading.Thread(target=self.client_thread, args=(conn, player_id))
            t.daemon = True
            t.start()

    def send_to_room(self, room_code: str, packet: bytes):
        raise NotImplementedError()

    def send_to_all(self, packet: bytes):
        for (conn, _, _) in self.connections:
            conn.send(packet)

    def create_room(self, conn, data):
        print("Creating room...")
        room_code, _ = self.room_manager.create_room()
        self.room_manager.join_room(room_code, data.player_info)
        conn.send(RoomCreatedData(room_code).to_packet())

    def join_room(self, conn, data):
        print("Joining room...")
        # TODO: Make different games instead of one hardcoded one
        self.room_manager.join_room(data.room_code, data.player_info)

        player_room = self.room_manager.get_room(data.room_code)
        if player_room is None:
            # TODO: Send to connection
            conn.send(
                ErrorNotification(
                    f"Failed to connect to room - no room with room code {data.room_code} found."
                ).to_packet()
            )
            return

        self.send_to_all(
            PlayerJoinedNotification(
                data.player_info, player_room.player_list
            ).to_packet()
        )
        conn.send(RoomJoinedData(data.room_code).to_packet())

    def client_thread(self, connection, player_id):
        """For each connected player, spawn a client thread. This now listens to
        calls from the client, connecting the client with the server."""
        print(f"Started a thread for client {player_id}")
        # on player connect
        connection.send(PlayerInfo(player_id).to_packet())

        while True:
            try:
                data = NetworkData.from_packet(connection.recv(4096))
            except ConnectionResetError:
                log.warning(f"Remote host lost connection")
                break
            except Exception as e:
                log.error(
                    f"Client thread encountered exception: {e}\nTrying to keep alive..."
                )
            # If nothing got sent, wait
            if not data:
                continue

            print(f"-- Network Data Command: {data.command}")

            # print(f"{data.command} {data.player_input}")

            if isinstance(data, CreateRoomCommand):
                self.create_room(connection, data)

            elif isinstance(data, PlayerReadyCommand):
                self.room_manager.set_player_ready_in_room(
                    data.room_code, data.player_name
                )

            elif isinstance(data, PlayerUnreadyCommand):
                self.room_manager.set_player_unready_in_room(
                    data.room_code, data.player_name
                )

            elif isinstance(data, JoinRoomCommand):
                print("Joining Game Command logic")
                self.join_room(connection, data)

            elif isinstance(data, StartGameCommand):
                print("Trying to start game")
                print("Checking if players in room are ready...")
                if self.room_manager.all_ready_in_room(data.room_code):
                    print("All players in room are ready")
                    # TODO: Replace with send_to_room
                    self.send_to_all(GameStartNotification().to_packet())

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

            elif isinstance(data, SendPlayerInputCommand):
                self.send_to_all(data.to_packet())

    def ping_connections(self):
        for connection in self.connections:
            connection.send()


if __name__ == "__main__":
    abes_ip = "217.105.109.132"
    laptop_abe_local_ip = "192.168.1.104"
    ivos_ip = "87.214.136.100"
    ivo_local = "192.168.1.124"
    local_ip = "localhost"

    server = Server(server_ip=ivo_local)
    server.listen_for_connections()
