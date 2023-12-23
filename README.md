# EchoSocket


Welcome to EchoSocket, a project that facilitates two-way communication between a server and multiple clients. This project provides a basic framework for building applications that involve networking and communication.

## Table of Contents

- [EchoSocket](#echosocket)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)
  - [Project Structure](#project-structure)
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

## Contributing

Contributions are welcome! just fork and have fun!

## License

This project is licensed under the [MIT License](LICENSE).
