
if __name__ == "__main__":
    import sys
    sys.path.append("..")

from dataclasses import dataclass, asdict
import json
import dacite

class NetworkData():
    def to_json(self):
        return json.dumps(asdict(self))
    
    def from_json(self, json_string):
        self = dacite.from_dict(data_class=type(self), data=json.loads(json_string))
        
    def to_packet(self):
        return str.encode(self.to_json())

    def from_packet(self, packet):
        return self.from_json(packet.decode())

@dataclass
class PlayerInfo(NetworkData):
    player_id: str

@dataclass
class GameState(NetworkData):
    game_id: str
    
@dataclass
class GetPlayerIDCommand(NetworkData):
    command: str = "get_player_data"

@dataclass
class GetGameStateCommand(NetworkData):
    command: str = "get_game_state"

@dataclass
class DisconnectPlayerCommand(NetworkData):
    player_id: str
    command: str = "disconnect_player"
    
@dataclass
class CreateGameCommand(NetworkData):
    command: str = "create_game"
    
@dataclass
class SendPlayerInput(NetworkData):
    player_input: dict
    command: str = "send_player_input"