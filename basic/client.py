import socket
import time

def start_client():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_name = input("Enter your name: ")

    # Connect to the server
    client_socket.connect(('127.0.0.1', 8888))

    while True:
        client_message = input("Enter a message: ")
        message = f"Client {client_name}: {client_message}"

        # Send the message to the server
        client_socket.send(message.encode('utf-8'))
        time.sleep(1)

        if message.lower() == 'exit':
            break

        # Receive the response from the server
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Server response: {response}")

    client_socket.close()

if __name__ == "__main__":
    start_client()
