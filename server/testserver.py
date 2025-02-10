import socket

# Server Configuration
HOST = '0.0.0.0'  # Listen on all available network interfaces
PORT = 12345       # Choose any available port

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server listening on {HOST}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"New client connected from {client_address}")
    
    # Send welcome message to client
    welcome_message = "Welcome to the server!"
    client_socket.sendall(welcome_message.encode())
    
    # Extra Credit: Send message.txt file
    try:
        with open("message.txt", "r") as file:
            file_content = file.read()
            client_socket.sendall(file_content.encode())
    except FileNotFoundError:
        print("message.txt not found!")
    
    client_socket.close()
