
# Client Script (client.py)
import socket

# Server Configuration
SERVER_HOST = '127.0.0.1'  # Change to server IP if running remotely
SERVER_PORT = 12345

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

# Receive and print the welcome message
welcome_message = client_socket.recv(1024).decode()
print("Server:", welcome_message)

# Receive and print the file content
file_content = client_socket.recv(1024).decode()
print("Received file content:", file_content)

# Close the connection
client_socket.close()