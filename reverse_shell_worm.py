# master.py
from src.server import Server
import subprocess
import os

def execute_command_task(command):
    global current_working_directory
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return result.strip()  # Strip leading and trailing whitespace
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output}"


if __name__ == "__main__":
    master = Server("127.0.0.1", 8080, "Master")

    # Register the execute_command_task function with key 'execute'
    master.register_task_function('execute', execute_command_task)

    master.run()
