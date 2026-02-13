import sqlite3
import json
import os

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
            steps TEXT NOT NULL
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

    # 2. Clear existing data (Only for recipes/ingredients, keep users)
    cursor.execute('DELETE FROM recipes')
    cursor.execute('DELETE FROM ingredients')

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
                cursor.execute(
                    'INSERT INTO recipes (name, steps) VALUES (?, ?)',
                    (r['name'], json.dumps(r['steps']))
                )
                recipe_id = cursor.lastrowid

                # Insert Ingredients
                for ing in r['ingredients']:
                    # Support both simple string lists and complex objects
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