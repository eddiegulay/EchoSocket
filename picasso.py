from src.server import Server
from src.jobs import draw_task


if __name__ == "__main__":
    master = Server("127.0.0.1", 8081, server_name="Picasso Server")

    master.register_task_function('draw', draw_task)

    master.run()