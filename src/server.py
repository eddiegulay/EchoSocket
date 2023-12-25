import socket
import threading
import json

class Server:
    def __init__(self, server_address, server_port, server_name):
        self.server_address = server_address
        self.server_port = server_port
        self.server_name = server_name

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((server_address, server_port))
        self.server_socket.listen(5)

        self.clients = []

        # Task functions dictionary
        self.task_functions = {}
        self.default_task_function = self.default_echo_task

        self.running = True

    def start_server(self):
        print(f"Server started at {self.server_address}:{self.server_port}")

        while self.running:
            client_socket, addr = self.server_socket.accept()
            print(f"Accepted connection from {addr}")
            self.clients.append(client_socket)

            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    self.handle_disconnect(client_socket)
                    break

                # Deserialize the JSON message
                message = json.loads(data)

                # Extract task key and task data
                task_key = message.get("task_key", "")
                task_data = message.get("task_data", "")

                if task_key.strip() == "exit":
                    self.close_server()
                    break

                print(f"Running task {task_key} from {client_socket.getpeername()}")
                # Process the task based on the task key
                try:
                    task_function = self.task_functions.get(task_key, self.default_task_function)
                    response = task_function(task_data)
                    # Send the response back to the client
                    client_socket.send(response.encode('utf-8'))
                except Exception as e:
                    response = f"Failed to process task {task_key}, try to register the task function\n"
                    response += f"Available task keys: {list(self.task_functions.keys())}"
                    client_socket.send(response.encode('utf-8'))
                    break

            except Exception as e:
                response = f"Problem: {e}"
                client_socket.send(response.encode('utf-8'))
                # self.handle_disconnect(client_socket)
                break

    def handle_disconnect(self, disconnected_sock):
        print(f"Connection from {disconnected_sock.getpeername()} closed")
        self.clients.remove(disconnected_sock)
        disconnected_sock.close()


    def broadcast(self, message):
        for client in self.clients:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error broadcasting message to {client.getpeername()}: {e}")
                self.handle_disconnect(client)

    def default_echo_task(self, task_data):
        return f"{self.server_name} received: {task_data}"

    def register_task_function(self, task_key, task_function):
        self.task_functions[task_key] = task_function

    def run(self):
        server_thread = threading.Thread(target=self.start_server)
        server_thread.start()

        try:
            server_thread.join()
        except KeyboardInterrupt:
            self.close_server()

    def close_server(self):
        print("Closing the server...")
        self.running = False

        # Close the server socket
        try:
            self.server_socket.close()
        except Exception as e:
            print(f"Error closing server socket: {e}")