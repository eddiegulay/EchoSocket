import socket
import select
import threading
import time

class FileServer:
    def __init__(self, server_address, server_port, server_name):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = server_address
        self.server_port = self.port = server_port
        self.server_socket.bind((server_address, server_port))
        self.server_socket.listen(5)
        self.clients = [self.server_socket]
        self.running = True
        self.server_name = server_name

    def start_server(self):
        print(f"Started File Server at {self.server_socket.getsockname()} for {self.server_name}")

        while self.running:
            readable, _, _ = select.select(self.clients, [], [])

            for sock in readable:
                if sock == self.server_socket:
                    client_socket, addr = self.server_socket.accept()
                    print(f"Accepted connection from {addr}")
                    self.clients.append(client_socket)

                    client_handler = threading.Thread(target=self.handle_file_client, args=(client_socket,))
                    client_handler.start()

    def handle_file_client(self, client_socket):
        try:
            # Receive the command indicating that a file is being sent
            command = client_socket.recv(4)

            if command == b'file':
                # Receive the file name
                file_name = client_socket.recv(1024).decode('utf-8')

                # Receive the file content
                with open(file_name, 'wb') as file:
                    while True:
                        data = client_socket.recv(1024)
                        if not data:
                            break
                        file.write(data)
                print(f"File {file_name} received from {client_socket.getpeername()}")
            else:
                print(f"Unexpected command received from {client_socket.getpeername()}: {command}")

        except Exception as e:
            print(f"Error receiving file from {client_socket.getpeername()}: {e}")
            self.handle_disconnect(client_socket)

    def handle_disconnect(self, disconnected_sock):
        print(f"Connection from {disconnected_sock.getpeername()} closed")
        self.clients.remove(disconnected_sock)
        disconnected_sock.close()

    def run(self):
        server_thread = threading.Thread(target=self.start_server)
        server_thread.start()

        try:
            server_thread.join()
        except KeyboardInterrupt:
            self.close_server()

    def close_server(self):
        print("Closing the file server...")
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

