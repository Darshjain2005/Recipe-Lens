import sqlite3
import json
import os

def setup_database():
    db_path = os.path.join(os.path.dirname(__file__), 'recipes.db')
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'recipes.json')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # (Keep your existing recipes and ingredients table code here)
    cursor.execute('CREATE TABLE IF NOT EXISTS recipes (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, steps TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS ingredients (id INTEGER PRIMARY KEY AUTOINCREMENT, recipe_id INTEGER, item TEXT, quantity TEXT)')

    conn.commit()
    conn.close()
    print("Database Updated with Users Table!")

if __name__ == "__main__":
    setup_database()