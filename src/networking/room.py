class Room:
    def __init__(self, room_code):
        self.room_code = room_code
        self.player_list = []
        self.players_ready_check = {}

    def connect(self, player):
        # add to player list
        self.player_list.append(player)
        # add to player ready check
        self.players_ready_check[player["name"]] = False

    def disconnect(self, player):
        # remove from player list
        if player in self.player_list:
            self.player_list.remove(player)
        # remove from player ready check
        if player in self.players_ready_check:
            del self.players_ready_check[player["name"]]

    def set_player_ready(self, player):
        self.players_ready_check[player["name"]] = True

    def set_player_unready(self, player):
        self.players_ready_check[player["name"]] = False

    @property
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
