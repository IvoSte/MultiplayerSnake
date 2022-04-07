
if __name__ == "__main__":
    import sys
    sys.path.append("..")


# Client depends on the Network
from networking.network import Network

class Client():

    def __init__(self, server, port):
        print("initializing client")
        # server assigns player ids
        # zoek naar de server, connect, get player_info
        self.network = Network(server, port)
        self.player_id = self.network.get_player_id()
        
        # receive game state, send to viewer
        self.game_state = None
        self.get_game_state()

            
    def send_player_input(self, command):
        self.network.send_player_input(command)
        # parse player input, send to server

    def get_game_state(self):
        self.game_state = self.network.get_game_state()

    def disconnect(self):
        self.network.disconnect_client(self.player_id)
        
if __name__=='__main__':
    client = Client("localhost", 25565)
    