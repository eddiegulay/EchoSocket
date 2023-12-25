# master.py
# this is your server file
from src.multi_clients import EchoSocket
from src.file_server import FileServer


SERVER_IP = "127.0.0.1" # localhost
SERVER_PORT = 8080 # port number
SERVER_NAME = "MasterServer" # server name


def main():
    # Create an instance of EchoSocket
    server = FileServer(SERVER_IP, SERVER_PORT, SERVER_NAME)

    try:
        # Start the server
        server.start_server()
    except KeyboardInterrupt:
        # Handle keyboard interrupt to gracefully close the server
        server.close_server()

if __name__ == "__main__":
    main()