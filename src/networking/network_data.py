from dataclasses import dataclass
from networking.network_data_base import NetworkData

## Naming convention:
## DATA is something to be pulled from the server by the client, or from the client to the server -- Ik wil dit weten
## A COMMAND is an instruction from the server or client to the other to do something specific. -- Ik wil dat je dit doet

## DATA ##
@dataclass
class PlayerInfo(NetworkData):
    player_id: str


@dataclass
class GameState(NetworkData):
    game_id: str


@dataclass
class Message(NetworkData):
    message: str


@dataclass
class RoomJoinedData(NetworkData):
    room_code: str
    command: str = "room_joined_data"


@dataclass
class RoomCreatedData(NetworkData):
    room_code: str
    command: str = "room_created_data"


@dataclass
class UpdatePlayerPositionsData(NetworkData):
    """Received by players from the server"""

    player_list: dict
    ## {player id: {snake positions : [list(snake_length)],
    #               score : score_value}


@dataclass
class PlayerJoinedNotification(NetworkData):
    """Received by players from the server on connection join"""

    player: dict
    total_player_list: list


# @dataclass
# class UpdateScoreData(NetworkData):
#     player_id: str
#     score: int

# on eat apple, if (multiplayer): send UpdateObjectsData
## Observer Pattern
# @dataclass
# class UpdateObjectsData(NetworkData):
#     # object id x removed / added
#     update_object: dict
#     ## object id
#     ## object type
#     ## object position


# player code:
#     eat_apple
#         if (multiplayer):
#             send_to_server
#         else:
#             send_to_local


# on every tick:
#     if gameState_prev == gameState_now:
#         networkobjects = parse_delta(gameState_prev, gameState_now)
#         send(networkobjects)

# @dataclass
# class GameInfo():
#     player_list:
#         ## player id
#         ## player name
#         ## .. colourmap, etc.


# GameState Future
## (snake state)
# snake length
# snake colour (derived from player id)
