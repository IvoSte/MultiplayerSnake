from networking.room import Room
from util import generate_room_code
from logger import log


ROOM_CODE_LENGTH = 4


class RoomManager:
    def __init__(self):
        self.rooms = {}

    def create_room(self):
        # room_code = generate_room_code(ROOM_CODE_LENGTH)
        # TODO: Remove hard-coded room code
        room_code = "AAAA"
        self.rooms[room_code] = Room(room_code)

        return (room_code, self.rooms[room_code])

    def set_player_ready_in_room(self, room_code, player_name):
        self.rooms[room_code].set_player_ready(player_name)

    def set_player_unready_in_room(self, room_code, player_name):
        self.rooms[room_code].set_player_unready(player_name)

    def get_room(self, room_code):
        if room_code not in self.rooms:
            log.error(f"Room with room code {room_code} does not exist")
            return None
        return self.rooms[room_code]

    def join_room(self, room_code, player):
        if room_code not in self.rooms:
            log.error(f"Room with room code {room_code} does not exist")
            return
        self.rooms[room_code].connect(player)

    def leave_room(self, room_code, player):
        if room_code not in self.rooms:
            log.error(f"Room with room code {room_code} does not exist")
            return
        self.rooms[room_code].disconnect(player)

    def all_ready_in_room(self, room_code):
        if room_code not in self.rooms:
            log.error(f"Room with room code {room_code} does not exist")
            return False
        print(self.rooms[room_code].all_players_ready)
        return self.rooms[room_code].all_players_ready()
