
if __name__ == "__main__":
    import sys
    sys.path.append("..")


from _thread import start_new_thread
import socket
import uuid
import json
from networking.network_data import PlayerInfo

class Server:

    def __init__(self, server_ip="localhost", port=25565):
        print("initializing server")
        self.server_ip = server_ip
        self.port = port
        self.addr = (self.server_ip, self.port)
        self.server = None
        self.bind_server(self.addr)
        self.connections = set()
        self.games = {}
        
    def bind_server(self, addr):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind(addr)
        except Exception as e:
            print(f"Failed to bind server: {e}")
        self.server.listen()
        
    def disconnect_player(self, player_id):
        # TODO delete any game if the game is empty
        # TODO remove player from game if it is not empty 
        
        # delete connection
        to_delete = None
        for conn in self.connections:
            if conn[2] == player_id:
                to_delete = conn
        self.connections.remove(to_delete)


    def listen_for_connections(self):
        
        print("Listening for connections...")
        # Players can connect to the server. A connection is added to the connection list
        # PLayers are assigned a rondom ID
        # A thread is spawned per player
        while True:
            try:
                conn, addr = self.server.accept()
                # Generate random player id
                player_id = str(uuid.uuid4())
                self.connections.add((conn, addr, player_id))
                
                start_new_thread(self.client_thread, (conn, player_id))
            except KeyboardInterrupt:
                print("Shutting down...")
                exit()

    def create_game(self, player_id):
        # TODO: create game
        pass
    
    def client_thread(self, connection, player_id):
        # on player connect
        connection.send(PlayerInfo(player_id).to_packet())
        
        while True:
            # TODO: Make this into the proper object
            data = json.loads(self.server.recv(4096).decode())
            
            # If nothing got sent, wait
            if not data:
                break
            
            if data.command == "create_game":
                self.create_game(player_id)
            
            elif data.command == "get_game_state":
                break
            
            elif data.command == "get_player_info":
                connection.send(PlayerInfo(player_id).to_packet())
            
            elif data.command == "send_player_input":
                break

            elif data.command == "disconnect_player":
                self.disconnect_player(data.player_id)
                return
            

    def ping_connections(self):
        for connection in self.connections:
            connection.send()
            
if __name__ == "__main__":
    server = Server()
    server.listen_for_connections()