import socket
import select
import threading

class BaseServer:
    def __init__(self, server_address, server_port, server_name, for_clients=False):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = server_address
        self.server_port = self.port = server_port
        self.for_clients = for_clients
        self.clients = []

        if not for_clients:
            self.server_socket.bind((server_address, server_port))
            self.server_socket.listen(5)
            self.clients.append(self.server_socket)
        else:
            print(f"Continuing as client grand'ma 👵 {server_name}...")

        self.running = True
        self.server_name = server_name

    def start_server(self):
        pass

    def handle_client(self, client_socket):
        pass

    def handle_disconnect(self, disconnected_sock):
        print(f"Connection from {disconnected_sock.getpeername()} closed")
        self.clients.remove(disconnected_sock)
        disconnected_sock.close()
        self.broadcast(f"Client {disconnected_sock.getpeername()} has disconnected.")

    def broadcast(self, message):
        for client in self.clients[1:]:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error broadcasting message to {client.getpeername()}: {e}")
                self.handle_disconnect(client)

    def create_new_client(self, server_address=None, server_port=None, client_name=None):
        if client_name is None:
            client_name = self.server_name

        if server_address is None:
            server_address = self.server_address
            server_port = self.port

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_address, server_port))

        client_thread = threading.Thread(target=self.start_client, args=(client_socket, client_name))
        client_thread.start()

        return client_socket

    def start_client(self, client_socket, client_name):
        pass

    def run(self):
        pass

    def close_server(self):
        print("Closing the server...")
        self.running = False

        for client in self.clients[1:]:
            try:
                client.close()
            except Exception as e:
                print(f"Error closing client connection {client.getpeername()}: {e}")

        try:
            self.server_socket.close()
        except Exception as e:
            print(f"Error closing server socket: {e}")

class TextServer(BaseServer):
    def start_server(self):
        print(f"Started Text Server at {self.server_socket.getsockname()}")

        while self.running:
            readable, _, _ = select.select(self.clients, [], [])

            for sock in readable:
                if sock == self.server_socket:
                    client_socket, addr = self.server_socket.accept()
                    print(f"Accepted connection from {addr}")
                    self.clients.append(client_socket)

                    client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
                    client_handler.start()
                else:
                    try:
                        data = sock.recv(1024).decode('utf-8')
                        if not data:
                            self.handle_disconnect(sock)
                        else:
                            print(f"Received from client {sock.getpeername()}: {data}")

                            response = f"{self.server_name} received: {data}"
                            sock.send(response.encode('utf-8'))

                            if data.lower() == 'exit':
                                self.handle_disconnect(sock)
                    except Exception as e:
                        print(f"Error handling client {sock.getpeername()}: {e}")
                        self.handle_disconnect(sock)

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                print(f"Received from client {client_socket.getpeername()}: {data}")

                response = f"{self.server_name} received: {data}"
                client_socket.send(response.encode('utf-8'))
            except Exception as e:
                print(f"Error handling client {client_socket.getpeername()}: {e}")
                self.handle_disconnect(client_socket)

        client_socket.close()

    def run(self):
        server_thread = threading.Thread(target=self.start_server)
        server_thread.start()

        try:
            server_thread.join()
        except KeyboardInterrupt:
            self.close_server()

class FileServer(BaseServer):
    def __init__(self, server_address, server_port, server_name, for_clients=False, file_dir='received'):
        super().__init__(server_address, server_port, server_name, for_clients)
        self.file_dir = file_dir

    def start_server(self):
        print(f"Started File Server at {self.server_socket.getsockname()}")

        while self.running:
            readable, _, _ = select.select(self.clients, [], [])

            for sock in readable:
                if sock == self.server_socket:
                    client_socket, addr = self.server_socket.accept()
                    print(f"Accepted connection from {addr}")
                    self.clients.append(client_socket)

                    client_handler = threading.Thread(target=self.handle_file_client, args=(client_socket,))
                    client_handler.start()
                else:
                    try:
                        data = sock.recv(1024).decode('utf-8')
                        if not data:
                            self.handle_disconnect(sock)
                        elif data.lower() == 'file':
                            file_name = sock.recv(1024).decode('utf-8')
                            self.receive_file(sock)
                        else:
                            print(f"Received from client {sock.getpeername()}: {data}")

                            response = f"{self.server_name} received: {data}"
                            sock.send(response.encode('utf-8'))

                            if data.lower() == 'exit':
                                self.handle_disconnect(sock)
                    except Exception as e:
                        print(f"Error handling client {sock.getpeername()}: {e}")
                        self.handle_disconnect(sock)

    def receive_file(self, client_socket):
        try:
            command = client_socket.recv(4)

            if command == b'file':
                file_name = client_socket.recv(1024).decode('utf-8')

                with open(f"{self.file_dir}/{file_name}", 'wb') as file:
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

    def handle_file_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                print(f"Received from client {client_socket.getpeername()}: {data}")

                response = f"{self.server_name} received: {data}"
                client_socket.send(response.encode('utf-8'))
            except Exception as e:
                print(f"Error handling client {client_socket.getpeername()}: {e}")
                self.handle_disconnect(client_socket)

        client_socket.close()

    def run(self):
        server_thread = threading.Thread(target=self.start_server)
        server_thread.start()

        try:
            server_thread.join()
        except KeyboardInterrupt:
            self.close_server()
