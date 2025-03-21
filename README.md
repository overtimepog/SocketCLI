# Socket Programming CLI

A simple command-line interface application demonstrating TCP and UDP socket programming for networking labs.

## Features

- Support for both TCP and UDP protocols
- Server and client modes
- Word scrambling functionality to demonstrate network communication
- User-friendly interface with emoji indicators
- Automatic IP address detection for server mode

## Requirements

- Python 3.x

## Usage

Run the script from a terminal:

```bash
python socketcli.py
```

Or make it executable (Unix-based systems):

```bash
chmod +x socketcli.py
./socketcli.py
```

## Modes

### Server Mode

1. Choose TCP or UDP protocol
2. Select Server mode
3. The application displays your IP address and random port number
4. Share these details with clients who want to connect
5. Wait for connections or messages
6. The server receives text from clients, scrambles it, and sends it back
7. Press Ctrl+C to exit

### Client Mode

1. Choose TCP or UDP protocol
2. Select Client mode
3. Enter the server's IP address and port number
4. Type text to send to the server for scrambling
5. Receive and view the scrambled response
6. Type 'quit' to exit

## How It Works

- **TCP Mode**: Creates a reliable, connection-oriented socket for data transmission
- **UDP Mode**: Creates a connectionless socket for lightweight message exchange
- The server scrambles all letters within each word of any received text
- The client connects to the server, sends text, and displays the scrambled result

## Example Session

```
============================================================
            🧪 Lab 4 Socket Programming CLI 🧪            
============================================================

What protocol would you like to use?
1. TCP
2. UDP

Enter your choice (number): 1

Do you want to run as a TCP server or client?
1. Server
2. Client

Enter your choice (number): 1

🔌 TCP Server started
📋 Server IP: 192.168.1.5
📋 Server Port: 54321

✅ IMPORTANT: Give these details to the client to connect!

⏳ Waiting for connections... (Press Ctrl+C to quit)
```

## Error Handling

The application includes error handling for common scenarios:
- Connection timeouts
- Connection refused errors
- Invalid inputs
- Unexpected disconnections