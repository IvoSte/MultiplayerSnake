class Room:
    def __init__(self, room_code):
        self.room_code = room_code
        self.player_list = {}
        self.players_ready_check = {}

    def is_empty(self):
        return len(self.player_list) == 0

    def connect(self, conn, player):
        # TODO: Add checking to see if player or connection is already in room
        # add to player list
        self.player_list[conn] = player
        # add to player ready check
        self.players_ready_check[player["name"]] = False

    def disconnect(self, conn):
        playername = self.player_list[conn]["name"]
        # remove from player ready check
        if playername in self.players_ready_check:
            del self.players_ready_check[playername]
        # remove from player list
        del self.player_list[conn]

    def set_player_ready(self, player_name):
        self.players_ready_check[player_name] = True

    def set_player_unready(self, player_name):
        self.players_ready_check[player_name] = False

    def all_players_ready(self):
        for player_ready in self.players_ready_check.values():
            if not player_ready:
                return False
        return True

    def show_players_in_room(self):
        print(self.player_list)

    def check_player_heartbeats(self):
        # Ping players for a heartbeat
        pass

    def __str__(self):
        return str((self.room_code, self.player_list))
