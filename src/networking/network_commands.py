from dataclasses import dataclass
from src.networking.network_data_base import NetworkData

## Naming convention:
## DATA is something to be pulled from the server by the client, or from the client to the server
## A COMMAND is an instruction from the server or client to the other to do something specific.

# TODO: Use RESTful naming convention for commands

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
class GetPlayerPositionsCommand(NetworkData):
    command: str = "get_player_positions"


@dataclass
class SendPlayerPositionCommand(NetworkData):
    player_position: list
    command: str = "send_player_position"
