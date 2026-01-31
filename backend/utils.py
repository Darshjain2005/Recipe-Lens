import sqlite3
import json
import re
import os

# This ensures the script finds the DB in the same folder (backend/)
DB_PATH = os.path.join(os.path.dirname(__file__), 'recipes.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name like row['name']
    return conn

def scale_value(value_str, servings):
    """Scales ingredient quantities based on number of servings."""
    if not value_str:
        return ""
    match = re.match(r"(\d+\.?\d*)\s*(.*)", str(value_str))
    if match:
        num, unit = match.groups()
        total = float(num) * int(servings)
        clean_num = int(total) if total.is_integer() else total
        return f"{clean_num} {unit}".strip()
    return value_str

def find_matching_recipes(user_ingredients):
    """Searches the SQL database for recipes matching the user's voice input."""
    if not user_ingredients:
        return []

    conn = get_db_connection()
    
    # We create a SQL query that counts how many ingredient matches each recipe has
    placeholders = ', '.join(['?'] * len(user_ingredients))
    query = f'''
        SELECT r.id, r.name, COUNT(i.item) as match_count
        FROM recipes r
        JOIN ingredients i ON r.id = i.recipe_id
        WHERE i.item IN ({placeholders})
        GROUP BY r.id
        ORDER BY match_count DESC
        LIMIT 3
    '''
    
    results = conn.execute(query, user_ingredients).fetchall()
    conn.close()
    
    # Note: We return 'id' as 'index' so your voice.js doesn't need to change!
    return [{"index": row['id'], "name": row['name']} for row in results]

def get_recipe(recipe_id, servings):
    """Fetches full recipe details and scales ingredients."""
    conn = get_db_connection()
    
    # Get recipe name and steps
    recipe_row = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
    
    # Get all ingredients for this recipe
    ing_rows = conn.execute('SELECT item, quantity FROM ingredients WHERE recipe_id = ?', (recipe_id,)).fetchall()
    conn.close()

    if not recipe_row:
        return {"error": "Recipe not found"}

    # Format ingredients for the frontend
    scaled_ingredients = {}
    for row in ing_rows:
        scaled_ingredients[row['item']] = scale_value(row['quantity'], servings)

    return {
        "name": recipe_row['name'],
        "ingredients": scaled_ingredients,
        "steps": json.loads(recipe_row['steps']) # Convert string back to list
    }

def get_step(recipe_id, step_idx):
    """Fetches a specific cooking step from the database."""
    conn = get_db_connection()
    recipe_row = conn.execute('SELECT steps FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
    conn.close()

    if not recipe_row:
        return {"done": True}

    steps = json.loads(recipe_row['steps'])
    
    if 0 <= step_idx < len(steps):
        return {"step": steps[step_idx], "done": False}
    
    return {"done": True}