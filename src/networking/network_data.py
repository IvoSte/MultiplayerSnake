from dataclasses import dataclass
from winreg import DeleteValue
from src.networking.network_data_base import NetworkData

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
class UpdatePlayersData(NetworkData):
    player_list: dict
        ## {player id: {snake positions : [list(snake_length)],
        #               score : score_value}

# @dataclass
# class UpdateScoreData(NetworkData):
#     player_id: str
#     score: int

# on eat apple, if (multiplayer): send UpdateObjectsData
## Observer Pattern
@dataclass
class UpdateObjectsData(NetworkData):
    # object id x removed / added
    update_object: dict
    ## object id
    ## object type
    ## object position

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