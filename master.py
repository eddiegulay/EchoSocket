# master.py
from src.server import Server

def reverse_string_task(data):
    return data[::-1]

if __name__ == "__main__":
    master = Server("127.0.0.1", 8080, "Master")

    # Register the reverse_string_task function with key 'reverse'
    master.register_task_function('reverse', reverse_string_task)

    master.run()
