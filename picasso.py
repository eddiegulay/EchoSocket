from src.server import Server
from src.jobs import draw_task

SERVER_IP = "localhost"
PORT = 8081

if __name__ == "__main__":
    master = Server(SERVER_IP, PORT, server_name="Picasso Server")

    master.register_task_function('draw', draw_task)

    master.run()