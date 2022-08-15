from dataclasses import dataclass
from networking.network_data_base import NetworkData
from game.event_manager import PlayerInputEvent
from controls.input_controls import Controls

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


@dataclass
class SendPlayerInputCommand(NetworkData):
    player_name: str
    player_input: Controls
    command: str = "send_player_input"


@dataclass
class PlayerReadyCommand(NetworkData):
    """Player is connected and ready for the game to start"""

    player_name: str
    command: str = "player_ready"


@dataclass
class PlayerUnreadyCommand(NetworkData):
    """Player is connected and unredies for the game to start"""

    player_name: str
    command: str = "player_unready"
