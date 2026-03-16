import sqlite3
import json
import os

# ── Import your new nutrition data ──
# nutrition_data.py must be in the same directory as database_setup.py
from nutrition_data import CALORIE_MAP, VITAMIN_MAP  # type: ignore[import]

def setup_database():
    # Paths
    db_path = os.path.join(os.path.dirname(__file__), 'recipes.db')
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'recipes.json')

    # Connect to Database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Create Tables
    # Users table for your new Sign Up / Log In interface
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            email TEXT UNIQUE NOT NULL, 
            password TEXT NOT NULL
        )
    ''')
    
    # Recipes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL, 
            steps TEXT NOT NULL,
            nutrition TEXT NOT NULL DEFAULT '{}'
        )
    ''')
    
    # Ingredients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            recipe_id INTEGER, 
            item TEXT NOT NULL, 
            quantity TEXT, 
            FOREIGN KEY (recipe_id) REFERENCES recipes (id)
        )
    ''')

    # ── NEW: Nutrition table ──────────────────────────────────────────────────
    # Stores per-100g calorie + vitamin data for each ingredient.
    # ingredient_label matches raw_label values from detector.py / NUTRITION_MAP.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nutrition (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingredient_label TEXT UNIQUE NOT NULL,
            calories_per_100g INTEGER,
            key_vitamins TEXT NOT NULL DEFAULT '{}'
        )
    ''')
    # ─────────────────────────────────────────────────────────────────────────

    # 2. Clear existing data (Only for recipes/ingredients, keep users)
    cursor.execute('DELETE FROM recipes')
    cursor.execute('DELETE FROM ingredients')

    # ── NEW: Repopulate nutrition table on every run ──────────────────────────
    cursor.execute('DELETE FROM nutrition')
    all_labels = set(CALORIE_MAP.keys()) | set(VITAMIN_MAP.keys())
    for label in all_labels:
        cal = CALORIE_MAP.get(label)
        vit = VITAMIN_MAP.get(label, {})
        cursor.execute(
            'INSERT OR REPLACE INTO nutrition (ingredient_label, calories_per_100g, key_vitamins) VALUES (?, ?, ?)',
            (label, cal, json.dumps(vit))
        )
    print(f"Nutrition table populated with {len(all_labels)} ingredients.")
    # ─────────────────────────────────────────────────────────────────────────

    # 3. Load and Insert JSON Data
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Handle if JSON is a list or wrapped in a 'recipes' key
            if isinstance(data, list):
                recipes = data
            else:
                recipes = data.get('recipes', [])

            for r in recipes:
                # Insert Recipe (Steps stored as a JSON string)
                nutrition_json = json.dumps(r.get('nutrition', {}))
                cursor.execute(
                    'INSERT INTO recipes (name, steps, nutrition) VALUES (?, ?, ?)',
                    (r['name'], json.dumps(r['steps']), nutrition_json)
                )
                recipe_id = cursor.lastrowid

                # Insert Ingredients
                if isinstance(r.get('ingredients'), dict):
                    # If it's a mapping of "ingredient_name" : "quantity_string"
                    for item_key, qty_value in r['ingredients'].items():
                        item = item_key.lower()
                        qty = str(qty_value)
                        cursor.execute(
                            'INSERT INTO ingredients (recipe_id, item, quantity) VALUES (?, ?, ?)',
                            (recipe_id, item, qty)
                        )
                else: # Assume it's a list (of strings or dicts)
                    for ing in r.get('ingredients', []):
                        if isinstance(ing, dict):
                            item = ing.get('item', '').lower()
                            qty = ing.get('quantity', 'as needed')
                        else:
                            item = str(ing).lower()
                            qty = 'as needed'
                        cursor.execute(
                            'INSERT INTO ingredients (recipe_id, item, quantity) VALUES (?, ?, ?)',
                            (recipe_id, item, qty)
                        )
        
        print(f"Successfully imported {len(recipes)} recipes!")
    else:
        print(f"Warning: JSON file not found at {json_path}. Skipping data import.")

    conn.commit()
    conn.close()
    print("Database Rebuilt and Users Table Checked!")

if __name__ == "__main__":
    setup_database()
