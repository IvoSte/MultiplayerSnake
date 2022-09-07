from dataclasses import dataclass
from networking.network_data_base import NetworkData
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


# TODO The player name needs to be sent, more than one player needs to be able to ready and it should be player dependent
@dataclass
class PlayerReadyCommand(NetworkData):
    """Player is connected and ready for the game to start"""

    command: str = "player_ready"


@dataclass
class PlayerUnreadyCommand(NetworkData):
    """Player is connected and unredies for the game to start"""

    command: str = "player_unready"


@dataclass
class JoinGameCommand(NetworkData):
    """A socket connection has joined the game"""

    player_info: dict
    command: str = "join_game"
