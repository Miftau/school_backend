import sqlite3
import bcrypt
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from config import DB_PATH

app = Flask(__name__)
CORS(app)

def get_connection():
    return sqlite3.connect(DB_PATH)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the School Backend!"})

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not username or not email or not password or not role:
        return jsonify({"message": "All fields are required."}), 400

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Check if user already exists
        cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
        if cursor.fetchone():
            return jsonify({"message": "Username or email already taken."}), 409

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Insert new user
        cursor.execute("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
                       (username, email, hashed_password, role))
        conn.commit()

    return jsonify({"message": "User created successfully."}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, password, role FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
        return jsonify({"status": "success", "role": user[2], "user_id": user[0]})
    return jsonify({"status": "fail", "message": "Invalid credentials"}), 401

@app.route('/get_user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, role FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()

    if user:
        return jsonify({
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "role": user[3]
        }), 200
    else:
        return jsonify({"message": "User not found."}), 404

@app.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not username or not email or not password or not role:
        return jsonify({"message": "All fields are required."}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET username = ?, email = ?, password = ?, role = ? WHERE id = ?",
            (username, email, hashed_password, role, user_id)
        )
        conn.commit()

    return jsonify({"message": "User updated successfully."}), 200

if __name__ == '__main__':
    app.run(debug=True)
