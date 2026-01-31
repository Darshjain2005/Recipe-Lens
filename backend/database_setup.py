import sqlite3
import json
import os

def setup_database():
    # This ensures the DB is created in the same folder as this script
    db_path = os.path.join(os.path.dirname(__file__), 'recipes.db')
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'recipes.json')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create Tables
    cursor.execute('DROP TABLE IF EXISTS ingredients')
    cursor.execute('DROP TABLE IF EXISTS recipes')
    
    cursor.execute('''
        CREATE TABLE recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            steps TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER,
            item TEXT NOT NULL,
            quantity TEXT,
            FOREIGN KEY (recipe_id) REFERENCES recipes (id)
        )
    ''')

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            recipes_data = json.load(f)
            for r in recipes_data:
                cursor.execute('INSERT INTO recipes (name, steps) VALUES (?, ?)', 
                               (r['name'], json.dumps(r['steps'])))
                recipe_id = cursor.lastrowid
                for item, qty in r['ingredients'].items():
                    cursor.execute('INSERT INTO ingredients (recipe_id, item, quantity) VALUES (?, ?, ?)',
                                   (recipe_id, item.lower().strip(), qty))
        print(f"Success! Database created at {db_path}")
    except FileNotFoundError:
        print(f"Error: Could not find JSON at {json_path}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()