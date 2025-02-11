from flask import Flask, render_template, request, redirect, jsonify
import os
import csv

app = Flask(__name__)

# Ensure message file exists
MESSAGE_FILE = "messages.csv"
if not os.path.exists(MESSAGE_FILE):
    with open(MESSAGE_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['username', 'message'])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        username = request.form['username']
        message = request.form['message']
        with open(MESSAGE_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([username, message])
        return redirect('/send_message')
    
    messages = []
    if os.path.exists(MESSAGE_FILE):
        with open(MESSAGE_FILE, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            messages = list(reader)
    
    return render_template('send_message.html', messages=messages)

@app.route('/get_messages')
def get_messages():
    messages = []
    if os.path.exists(MESSAGE_FILE):
        with open(MESSAGE_FILE, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            messages = [{'username': row[0], 'message': row[1]} for row in reader]
    return jsonify(messages=messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345, debug=True)
