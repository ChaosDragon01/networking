from flask import Flask, render_template, request, redirect, jsonify
import os
import csv
import sqlite3

app = Flask(__name__)

# Ensure data.csv exists
DATA_FILE = "data.csv"
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['method', 'endpoint'])

# Initialize SQLite database
DATABASE = 'messages.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        username = request.form['username']
        message = request.form['message']
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO messages (username, message) VALUES (?, ?)', (username, message))
        conn.commit()
        conn.close()
        
        # Log POST request to data.csv
        with open(DATA_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['POST', '/send_message'])
        
        return redirect('/send_message')
    
    # Log GET request to data.csv
    with open(DATA_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['GET', '/send_message'])
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT username, message FROM messages')
    messages = cursor.fetchall()
    conn.close()
    
    return render_template('send_message.html', messages=messages)

@app.route('/get_messages')
def get_messages():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT username, message FROM messages')
    messages = [{'username': row[0], 'message': row[1]} for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(messages=messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345, debug=True)