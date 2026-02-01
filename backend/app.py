from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from utils import find_matching_recipes, get_recipe, get_step

app = Flask(__name__)
CORS(app)

# Path to your SQLite database
DB_PATH = os.path.join(os.path.dirname(__file__), 'recipes.db')

# --- AUTHENTICATION ROUTE ---

@app.route("/auth", methods=["POST"])
def auth():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if user already exists
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()

    if user:
        # User exists, check if password is correct
        # Note: Index 2 is the password column in our 'users' table
        if user[2] == password:
            conn.close()
            return jsonify({"message": "Login successful"}), 200
        else:
            conn.close()
            return jsonify({"error": "Incorrect password for this email"}), 401
    else:
        # New user, register them
        try:
            cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
            conn.commit()
            conn.close()
            return jsonify({"message": "Account created successfully"}), 201
        except Exception as e:
            conn.close()
            return jsonify({"error": "Database error"}), 500

# --- RECIPE ROUTES ---

@app.route("/suggest-recipes", methods=["POST"])
def suggest_recipes():
    data = request.json
    ingredients = data.get("ingredients", [])
    return jsonify(find_matching_recipes(ingredients))

@app.route("/start-cooking", methods=["POST"])
def start_cooking():
    data = request.json
    return jsonify(get_recipe(data["recipe_index"], data["servings"]))

@app.route("/next-step", methods=["POST"])
def next_step():
    data = request.json
    return jsonify(get_step(data["recipe_index"], data["step"]))

if __name__ == "__main__":
    app.run(debug=True, port=5000)