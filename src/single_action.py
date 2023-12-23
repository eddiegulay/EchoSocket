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
                    except Exception as e:
                        print(f"Error handling client {sock.getpeername()}: {e}")
                        self.handle_disconnect(sock)

    def handle_client(self, client_socket):
        while True:
            try:
                # Receive data from the client
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                print(f"Received from client {client_socket.getpeername()}: {data}")

                # Send a response back to the client
                response = f"{self.server_name} received: {data}"
                client_socket.send(response.encode('utf-8'))
            except Exception as e:
                print(f"Error handling client {client_socket.getpeername()}: {e}")
                self.handle_disconnect(client_socket)

        client_socket.close()

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

    def start_client(self, server_address=None, server_port=None, client_name=None):
        if server_address is None:
            server_address = self.server_socket.getsockname()[0]
            server_port = self.server_socket.getsockname()[1]
            client_name = "Client"

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_address, server_port))

        while True:
            message = input(f"Enter a message for {self.server_name} (or 'exit' to close): ")

            # Send the message to the server
            client_socket.send(message.encode('utf-8'))

            if message.lower() == 'exit':
                break

            # Receive the response from the server
            response = client_socket.recv(1024).decode('utf-8')
            print(f"{self.server_name} response: {response}")

        client_socket.close()

    def run(self):
        server_thread = threading.Thread(target=self.start_server)
        client_thread = threading.Thread(target=self.start_client)

        server_thread.start()
        client_thread.start()

        try:
            server_thread.join()
            client_thread.join()
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

if __name__ == "__main__":
    app = ProbableTwoWay("127.0.0.1", 8080, "Server")
    app.run()
