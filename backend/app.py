from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
# Importing the standardized functions from utils.py
from utils import find_matching_recipes, get_recipe, get_step

app = Flask(__name__)
# CORS is essential for your frontend to communicate with this local server
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), 'recipes.db')

def get_db_connection():
    """Helper to create a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- 1. AUTHENTICATION ROUTES ---

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
        conn.commit()
        return jsonify({"message": "Account created successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "This email is already registered"}), 400
    finally:
        conn.close()

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', 
                        (email, password)).fetchone()
    conn.close()
    
    if user:
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid email or password"}), 401

# --- 2. RECIPE & COOKING ROUTES ---

@app.route("/suggest-recipes", methods=["POST"])
def suggest_recipes():
    """Matches spoken ingredients to recipes in the DB."""
    data = request.json
    ingredients = data.get("ingredients", [])
    # find_matching_recipes now returns 'index' to match JS expectations
    return jsonify(find_matching_recipes(ingredients))

@app.route("/start-cooking", methods=["POST"])
def start_cooking():
    """
    Returns scaled ingredients and all steps.
    Used by startCookingFlow() in voice.js to display ingredients first.
    """
    data = request.json
    recipe_idx = data.get("recipe_index")
    servings = data.get("servings")
    
    if recipe_idx is None or servings is None:
        return jsonify({"error": "Missing recipe index or servings"}), 400
        
    return jsonify(get_recipe(recipe_idx, servings))

@app.route("/next-step", methods=["POST"])
def next_step():
    """Fetches a specific step for voice navigation."""
    data = request.json
    recipe_idx = data.get("recipe_index")
    step_num = data.get("step")
    
    if recipe_idx is None or step_num is None:
        return jsonify({"error": "Missing data"}), 400
        
    return jsonify(get_step(recipe_idx, step_num))

# --- 3. SERVER START ---

if __name__ == "__main__":
    # Check if DB exists to prevent runtime errors
    if not os.path.exists(DB_PATH):
        print(f"CRITICAL ERROR: {DB_PATH} not found. Ensure your database is in the same folder.")
    else:
        print("--- Recipe Lens Backend Running ---")
        print("Listening on http://127.0.0.1:5000")
        app.run(debug=True, port=5000)