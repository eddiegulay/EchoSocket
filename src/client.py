import socket
import threading
import json

class Client:
    def __init__(self, server_address, server_port, server_name):
        self.server_address = server_address
        self.server_port = server_port
        self.server_name = server_name

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_address, server_port))

        self.running = True

    def send_task(self, task_key, task_data):
        message = json.dumps({"task_key": task_key, "task_data": task_data})
        self.client_socket.send(message.encode('utf-8'))

    def start_client(self):
        while self.running:
            task_key = input("Enter the task key (or 'exit' to close): ")
            if task_key.lower() == 'exit':
                break

            task_data = input(f"Enter the task data for {self.server_name}: ")

            # Send the task to the server
            self.send_task(task_key, task_data)

            # Receive the response from the server
            response = self.client_socket.recv(1024).decode('utf-8')
            print(f"Server response: {response}")

    def close_client(self):
        print("Closing the client...")
        self.running = False

        # Close the client socket
        try:
            self.client_socket.close()
        except Exception as e:
            print(f"Error closing client socket: {e}")