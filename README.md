# EchoSocket

This is EchoSocket, a project that facilitates two-way communication between a server and multiple clients. All in the look for faster realtime server-client communication.

<!-- project image -->
<p align="center">
  <img src="assets/echoSocket.jpg" alt="EchoSocket" width="500" />
</p>

## Table of Contents

- [EchoSocket](#echosocket)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Features](#features-1)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)
  - [Project Structure](#project-structure)
  - [Using EchoSocket](#using-echosocket)
    - [Server Setup](#server-setup)
    - [Client Interaction](#client-interaction)

## Features

Certainly! Here's a concise README content focusing on the mentioned points (1, 2, and 4):

---

## Features

1. **Simple Two-Way Communication:**
   - Enables real-time communication between a master server and multiple clients.
   - Clients can send and receive messages seamlessly, fostering efficient interactions.

2. **Modular Task Execution:**
   - Register custom task functions on the server for dynamic execution.
   - Clients submit tasks, and the server executes corresponding functions, allowing for easy extensibility.

3. **Graceful Server Shutdown:**
   - Ensures a controlled termination process upon server shutdown requests.
   - Closes client connections gracefully, maintaining stability in the system.

## Getting Started

### Prerequisites

- Python (version 3.x recommended)
- [Git](https://git-scm.com/) (optional)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/eddiegulay/EchoSocket.git
   ```

   or download and extract the ZIP file.

2. Navigate to the project directory:

   ```bash
   cd EchoSocket
   ```

3. Install dependencies (if any):

   ```bash
   # we use sockets for this project. it's a built-in module, so no need to install anything!
   ```

## Usage

## Project Structure

```txt
EchoSocket/
|-- basic/
|   |-- client.py
|   |-- server.py
|   |-- multi_clients.py
|   |-- single_action.py
|-- master.py
|-- slave.py
|-- src/
|   |-- client.py
|   |-- server.py
|-- .gitignore
|-- README.md
|-- (other project files)
```

- **basic:** Contains basic client and server scripts.
- **src:** Contains more advanced scripts for handling multiple clients. (The actual project)
- **master.py:** Where the server script is located.
- **slave.py:** Where the client script is located.

## Using EchoSocket

### Server Setup

1. **Create Server Instance:**

   In your `master.py` file, create an instance of the server and define your custom task functions.

   ```python
   # master.py
   from src.server import Server

   def reverse_string_task(data):
       return data[::-1]

   if __name__ == "__main__":
       # Create a server instance
       master = Server("127.0.0.1", 8080, "Master")

       # Register task functions
       master.register_task_function('reverse', reverse_string_task)

       # Run the server
       master.run()
   ```

2. **Run the Master Server:**

   Execute the `master.py` script to start the master server.

   ```bash
   python master.py
   ```

### Client Interaction

3. **Start a Slave Client:**

   In your `slave.py` file, create an instance of the client and send a task.

   ```python
   # slave.py
   from src.client import Client

   if __name__ == "__main__":
       # Create a client instance
       slave = Client("127.0.0.1", 8080, "Slave")

       # Send a task to reverse a string
       slave.send_task('reverse', 'Hello, EchoSocket!')

       # Wait for the response from the server
       response = slave.client_socket.recv(1024).decode('utf-8')
       print(f"Reversed Output: {response}")

       # Close the client connection
       slave.close_client()
   ```

4. **Run the Slave Client:**

   Execute the `slave.py` script to start the slave client.

   ```bash
   python slave.py
   ```