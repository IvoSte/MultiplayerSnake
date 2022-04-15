from dataclasses import dataclass
from src.networking.network_data_base import NetworkData

## COMMANDS ##
@dataclass
class GetPlayerIDCommand(NetworkData):
    command: str = "get_player_info"

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