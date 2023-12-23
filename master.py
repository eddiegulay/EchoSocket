# master.py
# this is your server file
from src.multi_clients import EchoSocket

def main():
    # Create an instance of EchoSocket
    server = EchoSocket("127.0.0.1", 8080, "MasterServer")

    try:
        # Start the server
        server.start_server()
    except KeyboardInterrupt:
        # Handle keyboard interrupt to gracefully close the server
        server.close_server()

if __name__ == "__main__":
    main()
