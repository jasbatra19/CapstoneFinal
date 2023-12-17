# app.py
from datetime import datetime
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # for react

# File to store user data
user_data_file = 'user_data.json'

# Load user data from file
try:
    with open(user_data_file, 'r') as file:
        users = json.load(file)
except FileNotFoundError:
    # If the file doesn't exist, initialize with an empty list
    users = []

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = next((user for user in users if user['username'] == username and user['password'] == password), None)

    if user:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if any(user['username'] == username for user in users):
        return jsonify({'success': False, 'message': 'Username is already taken'})

    users.append({'username': username, 'password': password})

    # Save user data to file
    with open(user_data_file, 'w') as file:
        json.dump(users, file, indent=2)

    return jsonify({'success': True, 'message': 'User registered successfully'})

# Add this to your Flask app.py

@app.route('/api/saveQuizData', methods=['POST'])
def save_quiz_data():
    data = request.get_json()
    username = data.get('username')
    quiz_type =data.get('quesType')  # Assuming this is a True/False quiz; modify accordingly
    score = data.get('score')

    user = next((user for user in users if user['username'] == username), None)

    if user:
        # Add quiz data to the user
        quiz_data_entry = {
            'quiz_type': quiz_type,
            'score': score,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        user.setdefault('quiz_data', []).append(quiz_data_entry)

        # Save user data to file
        with open(user_data_file, 'w') as file:
            json.dump(users, file, indent=2)

        return jsonify({'success': True, 'message': 'Quiz data saved successfully'})
    else:
        return jsonify({'success': False, 'message': 'User not found'})


@app.route('/api/user_quiz_data/<username>', methods=['GET'])
def get_user_quiz_data(username):
    user = next((u for u in users if u['username'] == username), None)

    if user:
        quiz_data = user.get('quiz_data', [])
        last_5_scores = quiz_data[-5:]
        return jsonify(last_5_scores)
    else:
        return jsonify({'message': 'User not found'}), 404


if __name__ == '__main__':
    app.run(port=5000,debug=True)
