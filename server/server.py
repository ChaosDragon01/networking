"""from flask import Flask, send_file
import socket

app = Flask(__name__)

# Server Configuration
HOST = '0.0.0.0'  # Listen on all available network interfaces
PORT = 12345       # Choose any available port

@app.route('/')
def home():
    return "Welcome to the Web Accessible Server!"

@app.route('/connect')
def connect_client():
    return "New client connected!"

@app.route('/message')
def send_message():
    try:
        return send_file("message.txt", as_attachment=True)
    except FileNotFoundError:
        return "message.txt not found!", 404

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
    """


from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Ensure message file exists
MESSAGE_FILE = "messages.txt"
if not os.path.exists(MESSAGE_FILE):
    open(MESSAGE_FILE, 'w').close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        message = request.form.get('message')
        if message:
            with open(MESSAGE_FILE, 'a') as file:
                file.write(message + "\n")
        return render_template('confirmation.html', message=message)
    return render_template('send_message.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)
