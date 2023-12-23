import socket
import select
import threading

class ProbableTwoWay:
    def __init__(self, server_address, server_port, server_name):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((server_address, server_port))
        self.server_socket.listen(5)

        self.clients = [self.server_socket]
        self.running = True
        self.server_name = server_name

    def start_server(self):
        print(f"Started Server at {self.server_socket.getsockname()}")

        while self.running:
            # Use select to handle multiple connections
            readable, _, _ = select.select(self.clients, [], [])

            for sock in readable:
                if sock == self.server_socket:
                    # New connection, accept it
                    client_socket, addr = self.server_socket.accept()
                    print(f"Accepted connection from {addr}")
                    self.clients.append(client_socket)

                    # Create a new thread to handle the client
                    client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
                    client_handler.start()
                else:
                    # Handle data from a client
                    try:
                        data = sock.recv(1024).decode('utf-8')
                        if not data:
                            self.handle_disconnect(sock)
                        else:
                            print(f"Received from client {sock.getpeername()}: {data}")

                            # Send a response back to the client
                            response = f"{self.server_name} received: {data}"
                            sock.send(response.encode('utf-8'))

                            # Check for the exit message
                            if data.lower() == 'exit':
                                self.handle_disconnect(sock)
                    except Exception as e:
                        print(f"Error handling client {sock.getpeername()}: {e}")
                        self.handle_disconnect(sock)

    def handle_disconnect(self, disconnected_sock):
        print(f"Connection from {disconnected_sock.getpeername()} closed")
        self.clients.remove(disconnected_sock)
        disconnected_sock.close()

        # Inform other clients about the disconnection
        self.broadcast(f"Client {disconnected_sock.getpeername()} has disconnected.")

    def broadcast(self, message):
        for client in self.clients[1:]:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error broadcasting message to {client.getpeername()}: {e}")
                self.handle_disconnect(client)

    def create_new_client(self, server_address, server_port, client_name=None):
        if client_name is None:
            client_name = "Client"

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_address, server_port))

        client_thread = threading.Thread(target=self.start_client, args=(client_socket, client_name))
        client_thread.start()

        return client_socket

    def start_client(self, client_socket, client_name):
        while True:
            message = input(f"Enter a message for {self.server_name} (or 'exit' to close): ")

            # Send the message to the server
            client_socket.send(message.encode('utf-8'))

            if message.lower() == 'exit':
                break

            # Receive the response from the server
            response = client_socket.recv(1024).decode('utf-8')
            print(f"{client_name} response: {response}")

        client_socket.close()

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

        # Close all client connections
        for client in self.clients[1:]:
            try:
                client.close()
            except Exception as e:
                print(f"Error closing client connection {client.getpeername()}: {e}")

        # Close the server socket
        try:
            self.server_socket.close()
        except Exception as e:
            print(f"Error closing server socket: {e}")

