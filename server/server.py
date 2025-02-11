from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import os
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Ensure message file exists
MESSAGE_FILE = "messages.csv"
if not os.path.exists(MESSAGE_FILE):
    with open(MESSAGE_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['username', 'message'])

# Ensure logindata.csv exists
LOGIN_DATA_FILE = "logindata.csv"
if not os.path.exists(LOGIN_DATA_FILE):
    with open(LOGIN_DATA_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['username', 'password'])
        writer.writerow(['user1', 'pass1'])  # Example user
        writer.writerow(['user2', 'pass2'])  # Example user

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('send_message'))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    with open(LOGIN_DATA_FILE, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        for row in reader:
            if row[0] == username and row[1] == password:
                session['username'] = username
                return redirect(url_for('send_message'))
    
    return 'Invalid username or password', 401

@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if 'username' not in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = session['username']
        message = request.form['message']
        with open(MESSAGE_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([username, message])
        return redirect(url_for('send_message'))
    
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

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345, debug=True)
