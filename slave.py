# client.py
from src.multi_clients import EchoSocket

SERVER_IP = "127.0.0.1"  # localhost
SERVER_PORT = 8080  # port number
SERVER_NAME = "MasterServer"  # server name (does not have to be the same as master.py)

def main():
    # Create an instance of EchoSocket for the client
    app = EchoSocket(SERVER_IP, SERVER_PORT, SERVER_NAME, for_clients=True)

    # create a slave server / client
    client_instance = app.create_new_client()

    # send a text message
    app.start_client(client_instance, client_name="Django Unchained")

    # send a file
    file_name = "example.txt"
    app.send_file(client_instance, file_name)

if __name__ == "__main__":
    main()
