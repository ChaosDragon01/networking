from flask import Flask, render_template, request, redirect, session, url_for, jsonify, flash
import os
import csv
from datetime import datetime
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'secretkey' # anything goes here honestly since it's a local server anyway
UPLOAD_FOLDER = 'static/profile_pics'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# This ensures logindata.csv exists
LOGIN_DATA_FILE = "logindata.csv"
if not os.path.exists(LOGIN_DATA_FILE):
    with open(LOGIN_DATA_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['username', 'password', 'profile_pic'])

# This ensures data.csv exists
DATA_FILE = "data.csv"
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['request_time', 'request_method', 'ip_address', 'city', 'state', 'country', 'zip', 'local_time'])

# Test variable to override IP address for testing purposes. Because ipinfo.io has a limit on requests. plus it's a local server anyway
USE_TEST_IP = True
TEST_IP = '8.8.8.8'  # Google's public DNS IP address

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def log_request(method, endpoint):
    # Use test IP if the test variable is set to True. This was used for if the ipinfo.io API is working.
    if USE_TEST_IP:
        ip = TEST_IP
    else:
        ip = request.remote_addr
    
    try:
        response = requests.get(f'http://ipinfo.io/{ip}/json')
        data = response.json()
        city = data.get('city', 'Unknown')
        state = data.get('region', 'Unknown')
        country = data.get('country', 'Unknown')
        zip_code = data.get('postal', 'Unknown')
        local_time = data.get('timezone', 'Unknown')
    except Exception as e:
        city = 'Unknown'
        state = 'Unknown'
        country = 'Unknown'
        zip_code = 'Unknown'
        local_time = 'Unknown'
        print(f"Error fetching data from ipinfo.io: {e}")
    
    request_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open(DATA_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([request_time, method, ip, city, state, country, zip_code, local_time])

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
                session['profile_pic'] = row[2]
                log_request('POST', '/login')
                return redirect(url_for('send_message'))
    
    return 'Invalid username or password', 401

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        profile_pic = request.files['profile_pic']
        
        if profile_pic and allowed_file(profile_pic.filename):
            filename = secure_filename(profile_pic.filename)
            profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = 'profilepic.jpg'
        
        with open(LOGIN_DATA_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([username, password, filename])
        
        flash('Account created successfully!', 'success')
        return redirect(url_for('home'))
    
    return render_template('register.html')

@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if 'username' not in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = session['username']
        message = request.form['message']
        with open('messages.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([username, message])
        log_request('POST', '/send_message')
        return redirect(url_for('send_message'))
    
    messages = []
    if os.path.exists('messages.csv'):
        with open('messages.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            messages = list(reader)
    
    log_request('GET', '/send_message')
    return render_template('send_message.html', messages=messages)

@app.route('/get_messages')
def get_messages():
    messages = []
    if os.path.exists('messages.csv'):
        with open('messages.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            messages = [{'username': row[0], 'message': row[1]} for row in reader]
    
    log_request('GET', '/get_messages')
    return jsonify(messages=messages)

@app.route('/logout')
def logout():
    username = session.pop('username', None)
    session.pop('profile_pic', None)
    if username:
        # Remove all messages from the user
        messages = []
        if os.path.exists('messages.csv'):
            with open('messages.csv', 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header row
                messages = [row for row in reader if row[0] != username]
        
        with open('messages.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['username', 'message'])
            writer.writerows(messages)
        
        log_request('GET', '/logout')
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345, debug=True)
