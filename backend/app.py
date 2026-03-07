"""
Recipe Lens — Unified Backend
Combines:
  • Voice Chef  : ingredient matching, recipe steps, user auth  (app.py)
  • Vision Chef : multi-model food detection via image upload    (vision.py)
"""

from flask import Flask, request, jsonify, send_from_directory, redirect
from flask_cors import CORS
import sqlite3
import os
import uuid
import time
import base64

# Vision Chef — FoodDetector (used by Vision routes)
from detector import FoodDetector

# Voice Chef — utility functions
from utils import find_matching_recipes, get_recipe, get_step

# ─────────────────────────────────────────────
# App setup
# ─────────────────────────────────────────────
app = Flask(__name__)
CORS(app)  # Allow all for local dev to avoid port issues

# ── Upload / file config (Vision Chef) ──
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32 MB

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'bmp'}

# ── Database (Voice Chef) ──
DB_PATH = os.path.join(os.path.dirname(__file__), 'recipes.db')

# ── Frontend directory (two levels up from backend/) ──
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'home'))

# ── Initialise detector once at startup ──
detector = FoodDetector()


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ─────────────────────────────────────────────
# Frontend static file serving
# ─────────────────────────────────────────────
@app.route("/")
def index():
    """Redirect root to Vision Chef page."""
    return redirect("/vision.html")

@app.route("/<path:filename>", methods=["GET"])
def serve_frontend(filename):
    """Serve any frontend asset (HTML, CSS, JS, images) from frontend/home/."""
    filepath = os.path.join(FRONTEND_DIR, filename)
    if os.path.isfile(filepath):
        return send_from_directory(FRONTEND_DIR, filename)
    # File not found — let Flask return its normal 404
    from flask import abort
    abort(404)


@app.route("/health", methods=["GET"])
def health_check():
    """Simple endpoint for frontend to check if backend is reachable."""
    return jsonify({"status": "ok", "message": "Backend is running"}), 200


def get_db_connection():
    """Return a SQLite connection with row-dict access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ─────────────────────────────────────────────
# 1. AUTHENTICATION ROUTES  (Voice Chef)
# ─────────────────────────────────────────────

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
    user = conn.execute(
        'SELECT * FROM users WHERE email = ? AND password = ?',
        (email, password)
    ).fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid email or password"}), 401


# ─────────────────────────────────────────────
# 2. RECIPE & COOKING ROUTES  (Voice Chef)
# ─────────────────────────────────────────────

@app.route("/suggest-recipes", methods=["POST"])
def suggest_recipes():
    """Match spoken ingredients to recipes in the DB."""
    data = request.json
    ingredients = data.get("ingredients", [])
    return jsonify(find_matching_recipes(ingredients))


@app.route("/start-cooking", methods=["POST"])
def start_cooking():
    """
    Return scaled ingredients and all steps.
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
    """Fetch a specific step for voice navigation."""
    data = request.json
    recipe_idx = data.get("recipe_index")
    step_num = data.get("step")

    if recipe_idx is None or step_num is None:
        return jsonify({"error": "Missing data"}), 400

    return jsonify(get_step(recipe_idx, step_num))


@app.route("/start-cooking-by-name", methods=["POST"])
def start_cooking_by_name():
    """
    Look up a recipe by name using LIKE search and return its data.
    Used by Vision Chef where we have dish names but not IDs.
    """
    data = request.json
    recipe_name = data.get("recipe_name", "").strip()
    servings = data.get("servings", 2)

    if not recipe_name:
        return jsonify({"error": "Missing recipe name"}), 400

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # First try exact match, then LIKE
    row = conn.execute('SELECT id FROM recipes WHERE name = ?', (recipe_name,)).fetchone()
    if not row:
        row = conn.execute('SELECT id FROM recipes WHERE name LIKE ?', (f"%{recipe_name}%",)).fetchone()
    conn.close()

    if not row:
        return jsonify({"error": f"Recipe '{recipe_name}' not found in database"}), 404

    return jsonify(get_recipe(row['id'], servings))


# ─────────────────────────────────────────────
# 3. VISION DETECTION ROUTES  (Vision Chef)
# ─────────────────────────────────────────────

@app.route("/detect", methods=["POST"])
def detect():
    """Accept a multipart image upload and run the detector."""
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Use PNG, JPG, JPEG, WEBP or BMP'}), 400

    # Save uploaded file
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        print(f"\n📸 Vision Request: {filename}")
        start = time.time()
        results = detector.analyze(filepath)
        elapsed = round(time.time() - start, 2)
        
        # Ensure results is a valid dict and has expected keys
        if not isinstance(results, dict):
            print(f"  ⚠️ Error: detector.analyze returned non-dict: {type(results)}")
            results = {"success": False, "error": "Internal detector error"}
        
        results['processing_time'] = elapsed
        results['image_url'] = f'/uploads/{filename}'
        
        n_found = results.get('total_found', 0)
        print(f"  ✅ Detection complete in {elapsed}s. Found {n_found} ingredients.")
        
        return jsonify(results)
    except Exception as e:
        print(f"  ❌ Backend Error in /detect: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route("/detect_base64", methods=["POST"])
def detect_base64():
    """Accept a base64-encoded webcam snapshot and run the detector."""
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({'error': 'No image data'}), 400

    img_data = data['image']
    # Strip the data-URL prefix if present (e.g. "data:image/jpeg;base64,...")
    if ',' in img_data:
        img_data = img_data.split(',')[1]

    filename = f"{uuid.uuid4().hex}.jpg"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    with open(filepath, 'wb') as f:
        f.write(base64.b64decode(img_data))

    try:
        print(f"\n📸 Vision Request (Base64): {filename}")
        start = time.time()
        results = detector.analyze(filepath)
        elapsed = round(time.time() - start, 2)
        
        if not isinstance(results, dict):
            print(f"  ⚠️ Error: detector.analyze returned non-dict: {type(results)}")
            results = {"success": False, "error": "Internal detector error"}

        results['processing_time'] = elapsed
        results['image_url'] = f'/uploads/{filename}'
        
        n_found = results.get('total_found', 0)
        print(f"  ✅ Detection complete in {elapsed}s. Found {n_found} ingredients.")
        
        return jsonify(results)
    except Exception as e:
        print(f"  ❌ Backend Error in /detect_base64: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# ─────────────────────────────────────────────
# 4. STATIC FILE ROUTES  (Vision Chef)
# ─────────────────────────────────────────────

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve original uploaded images back to the frontend."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/annotated/<filename>')
def annotated_file(filename):
    """Serve annotated result images back to the frontend."""
    return send_from_directory('results', filename)


# ─────────────────────────────────────────────
# 5. SERVER START
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # Create required directories for Vision Chef
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('results', exist_ok=True)

    # Warn early if the Voice Chef database is missing
    if not os.path.exists(DB_PATH):
        print(f"⚠️  WARNING: {DB_PATH} not found.")
        print("   Voice Chef recipe routes will not work until recipes.db is present.")
    
    print("\n🍽️  Recipe Lens — Unified Backend")
    print("   Voice Chef  : /suggest-recipes · /start-cooking · /next-step")
    print("   Vision Chef : /detect · /detect_base64")
    print("   Auth        : /register · /login")
    print("   Open http://localhost:5000 in your browser\n")

    app.run(debug=False, host='0.0.0.0', port=5000)