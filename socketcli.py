#!/usr/bin/env python
import socket
import random
import sys
import os
import time
import platform

def get_ip_address():
    """Get the local IP address of this machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()

def scramble_word(word):
    """Scrambles all characters of a word completely."""
    word_list = list(word)
    random.shuffle(word_list)
    return ''.join(word_list)

def scramble_text(text):
    """Scrambles the letters of each word in the text."""
    return ' '.join(scramble_word(word) for word in text.split())

def clear_screen():
    """Clear the terminal screen."""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def print_header():
    """Print a nice header for the CLI."""
    clear_screen()
    print("\n" + "="*60)
    print("🧪 Lab 4 Socket Programming CLI 🧪".center(60))
    print("="*60)

def start_tcp_server():
    """Start a TCP server and return its IP and port."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', 0))
    server_ip = get_ip_address()
    server_port = server_socket.getsockname()[1]
    server_socket.listen(1)
    
    clear_screen()
    print(f"\n🔌 TCP Server started")
    print(f"📋 Server IP: {server_ip}")
    print(f"📋 Server Port: {server_port}")
    print("\n✅ IMPORTANT: Give these details to the client to connect!")
    print("\n⏳ Waiting for connections... (Press Ctrl+C to quit)")
    
    try:
        while True:
            try:
                connection_socket, addr = server_socket.accept()
                client_ip, client_port = addr
                print(f"\n✅ Connected to {client_ip}:{client_port}")
                
                with connection_socket:
                    message = connection_socket.recv(1024).decode()
                    if message:
                        print(f"📥 Received from client ({client_ip}:{client_port}): {message}")
                        modified_message = scramble_text(message)
                        connection_socket.send(modified_message.encode())
                        print(f"📤 Sent back: {modified_message}")
            except Exception as e:
                print(f"❌ Error handling connection: {e}")
    except KeyboardInterrupt:
        print("\n👋 Server shutdown gracefully.")
    except socket.error as err:
        print(f"❌ Server error: {err}")
    finally:
        server_socket.close()

def start_udp_server():
    """Start a UDP server and return its IP and port."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', 0))
    server_ip = get_ip_address()
    server_port = server_socket.getsockname()[1]
    
    clear_screen()
    print(f"\n🔌 UDP Server started")
    print(f"📋 Server IP: {server_ip}")
    print(f"📋 Server Port: {server_port}")
    print("\n✅ IMPORTANT: Give these details to the client to connect!")
    print("\n⏳ Waiting for messages... (Press Ctrl+C to quit)")
    
    try:
        while True:
            message, client_address = server_socket.recvfrom(2048)
            if message:
                client_ip, client_port = client_address
                print(f"\n📥 Received from client ({client_ip}:{client_port}): {message.decode()}")
                modified_message = scramble_text(message.decode())
                server_socket.sendto(modified_message.encode(), client_address)
                print(f"📤 Sent back: {modified_message}")
    except KeyboardInterrupt:
        print("\n👋 Server shutdown gracefully.")
    except socket.error as err:
        print(f"❌ Server error: {err}")
    finally:
        server_socket.close()

def start_tcp_client(server_ip, server_port):
    """Start a TCP client connecting to the given server IP and port."""
    clear_screen()
    print(f"\n🔌 TCP Client started")
    print(f"📋 Connecting to server at {server_ip} on port {server_port}")
    print("⌨️  Type 'quit' to exit")
    
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.settimeout(5)
                try:
                    client_socket.connect((server_ip, server_port))
                    message = input("\n📝 Input text to scramble: ")
                    if message.lower() == 'quit':
                        break
                    
                    client_socket.send(message.encode())
                    modified_message = client_socket.recv(1024).decode()
                    print(f"📥 Returned from server ({server_ip}:{server_port}): {modified_message}")
                except socket.timeout:
                    print("⏱️  Connection timed out. Make sure the server is running.")
                    retry = input("Try again? (y/n): ")
                    if retry.lower() != 'y':
                        break
                except ConnectionRefusedError:
                    print("❌ Connection refused. Make sure the server is running and the IP/port are correct.")
                    retry = input("Try again? (y/n): ")
                    if retry.lower() != 'y':
                        break
        except socket.error as e:
            print(f"❌ Error: {e}")
            retry = input("Try again? (y/n): ")
            if retry.lower() != 'y':
                break

def start_udp_client(server_ip, server_port):
    """Start a UDP client connecting to the given server IP and port."""
    clear_screen()
    print(f"\n🔌 UDP Client started")
    print(f"📋 Connecting to server at {server_ip} on port {server_port}")
    print("⌨️  Type 'quit' to exit")
    
    while True:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.settimeout(5)
        message = input("\n📝 Input text to scramble: ")
        if message.lower() == 'quit':
            break
        
        try:
            client_socket.sendto(message.encode(), (server_ip, server_port))
            modified_message, server_address = client_socket.recvfrom(2048)
            print(f"📥 Returned from server ({server_ip}:{server_port}): {modified_message.decode()}")
        except socket.timeout:
            print("⏱️  Request timed out. Make sure the server is running.")
        except socket.error as e:
            print(f"❌ Error: {e}")
        finally:
            client_socket.close()

def get_user_choice(prompt, options):
    """Get a validated choice from the user."""
    while True:
        print("\n" + prompt)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        try:
            choice = int(input("\nEnter your choice (number): "))
            if 1 <= choice <= len(options):
                return choice
            else:
                print("❌ Invalid choice. Please try again.")
        except ValueError:
            print("❌ Please enter a number.")

def main():
    """Main function to interactively ask the user for options and run the appropriate server/client."""
    while True:
        print_header()
        
        # Ask protocol type
        protocol_choice = get_user_choice(
            "What protocol would you like to use?",
            ["TCP", "UDP"]
        )
        protocol = "tcp" if protocol_choice == 1 else "udp"
        
        # Ask mode
        mode_choice = get_user_choice(
            f"Do you want to run as a {protocol.upper()} server or client?",
            ["Server", "Client"]
        )
        mode = "server" if mode_choice == 1 else "client"
        
        # Execute based on choices
        if mode == "server":
            if protocol == "tcp":
                start_tcp_server()
            else:  # UDP
                start_udp_server()
        else:  # Client mode
            # Get server details
            print("\nEnter the server details:")
            server_ip = input("Server IP address: ")
            
            while True:
                try:
                    server_port = int(input("Server port number: "))
                    break
                except ValueError:
                    print("❌ Please enter a valid port number (integer).")
            
            if protocol == "tcp":
                start_tcp_client(server_ip, server_port)
            else:  # UDP
                start_udp_client(server_ip, server_port)
        
        # Ask if the user wants to continue
        print("\n" + "="*60)
        #if input("\nDo you want to run another session? (y/n): ").lower() != 'y':
        print("\n👋 Thanks for using the Socket Programming CLI! Goodbye!")
        break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Program terminated by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")