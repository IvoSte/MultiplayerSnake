from networking.room import Room
from util import generate_room_code

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

    def get_room(self, room_code):
        if room_code not in self.rooms:
            raise Exception(f"Room with room code {room_code} does not exist")
        return self.rooms[room_code]

    def join_room(self, room_code, player):
        if room_code not in self.rooms:
            raise Exception(f"Room with room code {room_code} does not exist")
        self.rooms[room_code].connect(player)

    def leave_room(self, room_code, player):
        if room_code not in self.rooms:
            raise Exception(f"Room with room code {room_code} does not exist")
        self.rooms[room_code].disconnect(player)
