# slave.py
# this is where you create slave servers
from src.multi_clients import EchoSocket
from src.file_server import FileServer
from src.echo import BaseServer, TextServer

SERVER_IP = "127.0.0.1"  # localhost
SERVER_PORT = 8080  # port number
SERVER_NAME = "MasterServer"  # server name (does not have to be the same as master.py)

def main():
    # Create an instance of EchoSocket for the server
    app = EchoSocket(SERVER_IP, SERVER_PORT, SERVER_NAME, for_clients=True)

    # Create a slave client
    client_instance = app.create_new_client()
    app.start_client(client_instance, client_name="SlaveClient")

if __name__ == "__main__":
    main()