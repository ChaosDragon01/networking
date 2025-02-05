from http.server import SimpleHTTPRequestHandler, HTTPServer
import socket

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Hello, world!")

def run(server_class=HTTPServer, handler_class=MyHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
    def persistent_server(host='0.0.0.0', port=8000):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((host, port))
            server_socket.listen()
            print(f'Server listening on {host}:{port}')
            
            while True:
                client_socket, client_address = server_socket.accept()
                with client_socket:
                    print(f'Connected by {client_address}')
                    client_socket.sendall(b'Welcome to the server!')

    if __name__ == "__main__":
        persistent_server()