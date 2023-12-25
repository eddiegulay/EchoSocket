# slave.py
from src.client import Client

if __name__ == "__main__":
    slave = Client("127.0.0.1", 8080, "THe Attacker")

    while True:
        command = input(">> ")
        if command.lower() == 'exit':
            break

        # Send a task to execute the command on the server
        slave.send_task('execute', command)

        # Wait for the response from the server
        response = slave.client_socket.recv(4096).decode('utf-8')
        print(f"Command Output:\n{response}")

    # Close the client connection
    slave.close_client()
