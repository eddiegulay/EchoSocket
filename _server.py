# master.py
from src.server import Server
from src.jobs import execute_command_task, download_file_task

SERVER_IP = "192.168.136.14"
PORT = 8081

if __name__ == "__main__":
    master = Server(SERVER_IP, PORT, "Master")

    # Register the execute_command_task function with key 'execute'
    master.register_task_function('execute', execute_command_task)
    master.register_task_function('download', download_file_task)

    master.run()
