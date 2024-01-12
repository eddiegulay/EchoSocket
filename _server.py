# master.py
from src.server import Server
from src.jobs import execute_command_task, download_file_task


if __name__ == "__main__":
    master = Server("127.0.0.1", 8081, "Master")

    # Register the execute_command_task function with key 'execute'
    master.register_task_function('execute', execute_command_task)
    master.register_task_function('download', download_file_task)

    master.run()
