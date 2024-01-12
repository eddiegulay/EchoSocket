# slave.py
from src.client import Client

if __name__ == "__main__":
    slave = Client("127.0.0.1", 8081, "tHe clIeNt")

    while True:
        command = input(">> ")
        if command.lower() == 'exit':
            break

        elif command.lower().startswith('download'):
            # Send a task to download a file
            slave.send_task('download', command.split()[1])
            # continue

        elif command.lower().startswith('cmd'):
            # Send a task to execute the command on the server
            slave.send_task('execute', command.split()[1])

        else:
            print("We don't support that command yet.")
            continue
        # Wait for the response from the server
        response = slave.client_socket.recv(4096).decode('utf-8')
        print(f"Command Output:\n{response}")

    # Close the client connection
    slave.close_client()
