# EchoSocket


Welcome to EchoSocket, a project that facilitates two-way communication between a server and multiple clients. This project provides a basic framework for building applications that involve networking and communication.

<!-- project image -->
<p align="center">
  <img src="assets/echoSocket.jpg" alt="EchoSocket" width="500" />
</p>

## Table of Contents

- [EchoSocket](#echosocket)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)
  - [Project Structure](#project-structure)
  - [EchoSocket: Master-Slave Connection](#echosocket-master-slave-connection)
  - [Interacting with the System](#interacting-with-the-system)
    - [Notes](#notes)
  - [Contributing](#contributing)
  - [License](#license)

## Features

- Simple two-way communication between a server and multiple clients.
- Easy-to-use Python scripts for both the server and client components.
- Support for handling multiple client connections simultaneously.

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
|-- master.py
|-- slave.py
|-- src/
|   |-- multi_clients.py
|   |-- single_action.py
|-- .gitignore
|-- README.md
|-- (other project files)
```

- **basic:** Contains basic client and server scripts.
- **src:** Contains more advanced scripts for handling multiple clients.
- **master.py:** Where the server script is located.
- **slave.py:** Where the client script is located.

---
Certainly! Here's a simple README for creating connections between a master server and slave clients using the `EchoSocket` class in `multi_clients.py`:

---

## EchoSocket: Master-Slave Connection

1. **Run the Master Server:**

    - Open `master.py` and customize the following variables:

        ```python
        SERVER_IP = "127.0.0.1"  # Set the server IP address
        SERVER_PORT = 8080       # Set the server port
        SERVER_NAME = "MasterServer"  # Set the server name
        ```

    - Run the master server:

        ```bash
        python master.py
        ```

2. **Run the Slave Client:**

    - Open `slave.py` and customize the following variables:

        ```python
        SERVER_IP = "127.0.0.1"  # Set the server IP address
        SERVER_PORT = 8080       # Set the server port
        SERVER_NAME = "MasterServer"  # Set the server name (should match the master)
        ```

    - Run the slave client:

        ```bash
        python slave.py
        ```

## Interacting with the System

- Once the master server and slave clients are running, the master server will accept incoming connections from slaves.

- Slave clients can send messages to the master server, and the server will respond by echoing the received messages.

- To gracefully exit the system, type `'exit'` as a message in a slave client.

### Notes

- The master and slave instances of `EchoSocket` are designed to be flexible, allowing for easy customization of server IP, port, and name.

- The system uses a simple echo mechanism where the server responds with an echo of the received message.

---

## Contributing

Contributions are welcome! just fork and have fun!

## License

This project is licensed under the [MIT License](LICENSE).
