# master.py
# this is your server file
from src.multi_clients import EchoSocket


SERVER_IP = "127.0.0.1" # localhost
SERVER_PORT = 8080 # port number
SERVER_NAME = "MasterServer" # server name


def main():
    text_server = EchoSocket("127.0.0.1", 8080, "MasterServer")
    text_server.run()

if __name__ == "__main__":
    main()