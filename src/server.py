if __name__ == "__main__":
    import sys

    sys.path.append("..")


from dataclasses import dataclass
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
    LeaveRoomCommand,
    SpawnNewFoodCommand,
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
    ReadyCheckUpdatedNotification,
    RoomJoinedData,
    RoomCreatedData,
    GameStartState,
    RoomConfig,
)

# TODO refactor the connection tuple object to this dataclass.
# @dataclass
# class PlayerConnection:
#     conn: socket
#     addr: _RetAddress
#     player_id: str


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

    def remove_connection(self, connection):
        # TODO: Vies
        full_connection_to_delete = None
        for full_conn in self.connections:
            if full_conn[0] == connection:
                full_connection_to_delete = full_conn
                break

        # delete connection
        self.connections.remove(full_connection_to_delete)

    def disconnect_player(self, connection):
        # TODO delete any game if the game is empty
        # TODO remove player from game if it is not empty
        self.room_manager.leave_all_rooms_for_player(connection)

        self.room_manager.print_all_rooms()

        self.remove_connection(connection)

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

    def send_to_others_in_room(self, room_code: str, self_conn, packet: bytes):
        for (conn, _, _) in self.connections:
            if conn == self_conn:
                continue
            conn.send(packet)

    def send_to_all(self, packet: bytes):
        for (conn, _, _) in self.connections:
            conn.send(packet)

    def create_room(self, conn, data):
        log.debug("Creating room... -- in server")
        room_code, _ = self.room_manager.create_room()
        self.room_manager.join_room(room_code, conn, data.player_info)
        conn.send(RoomCreatedData(room_code).to_packet())

    def join_room(self, conn, data):
        log.debug("Joining room... -- in server")
        # TODO: Make different games instead of one hardcoded one
        self.room_manager.join_room(data.room_code, conn, data.player_info)

        player_room = self.room_manager.get_room(data.room_code)
        if player_room is None:
            # TODO: Send to connection
            conn.send(
                ErrorNotification(
                    f"Failed to connect to room - no room with room code {data.room_code} found."
                ).to_packet()
            )
            return

        # TODO: player_room.player_list is a dictionary, send it as such instead of transforming it to an array
        self.send_to_all(
            PlayerJoinedNotification(
                data.player_info,
                [
                    player_room.player_list[playerkey]
                    for playerkey in player_room.player_list
                ],
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
                    self.send_to_all(
                        ReadyCheckUpdatedNotification(
                            data.player_name, True
                        ).to_packet()
                    )

                elif isinstance(data, PlayerUnreadyCommand):
                    self.room_manager.set_player_unready_in_room(
                        data.room_code, data.player_name
                    )
                    self.send_to_all(
                        ReadyCheckUpdatedNotification(
                            data.player_name, False
                        ).to_packet()
                    )

                elif isinstance(data, JoinRoomCommand):
                    self.join_room(connection, data)

                elif isinstance(data, StartGameCommand):
                    if self.room_manager.all_ready_in_room(data.room_code):
                        # TODO: Replace with send_to_room
                        self.send_to_all(
                            GameStartNotification(
                                GameStartState(
                                    data.room_code, RoomConfig((60, 40)), (20, 20), []
                                )
                            ).to_packet()
                        )

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
                    connection.send(
                        UpdatePlayerPositionsData(player_positions).to_packet()
                    )

                elif isinstance(data, LeaveRoomCommand):
                    self.room_manager.leave_room(data.room_code, connection)
                    self.room_manager.print_all_rooms()

                elif isinstance(data, DisconnectPlayerCommand):
                    self.disconnect_player(data.player_id)

                elif isinstance(data, SendPlayerInputCommand):
                    self.send_to_all(data.to_packet())

                elif isinstance(data, SpawnNewFoodCommand):
                    self.send_to_others_in_room(
                        data.room_code,
                        connection,
                        SpawnNewFoodCommand.to_packet(),
                    )

            except ConnectionResetError as e:
                log.warning(f"Remote host lost connection")
                # log.debug(e)
                self.disconnect_player(connection)
                break
            except Exception as e:
                log.error(
                    f"Client thread encountered exception: {e}\nTrying to keep alive..."
                )

    def ping_connections(self):
        for connection in self.connections:
            connection.send()


if __name__ == "__main__":
    abes_ip = "217.105.109.132"
    laptop_abe_local_ip = "192.168.1.104"
    ivos_ip = "87.214.136.100"
    ivo_local = "192.168.1.124"
    local_ip = "localhost"
    ip_uni = "145.97.151.17"

    server = Server(server_ip=ivo_local)
    server.listen_for_connections()
