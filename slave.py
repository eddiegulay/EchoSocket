# slave.py
from src.client import Client

if __name__ == "__main__":
    slave = Client("127.0.0.1", 8080, "Slave")

    # Send a task to reverse the given string
    while True:
        string = input("Enter a string to reverse: ")
        if string.lower() == 'exit':
            break

        slave.send_task('reverse', string)

        # Wait for the response from the server
        response = slave.client_socket.recv(1024).decode('utf-8')
        print(f"Output: {response}")

    # kill the server
    slave.send_task('exit', '')

    slave.close_client()