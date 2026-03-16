import sqlite3
import json
import re
import os

# Per-ingredient nutrition lookup
from nutrition_data import CALORIE_MAP, VITAMIN_MAP  # type: ignore[import]

# Path to the database
DB_PATH = os.path.join(os.path.dirname(__file__), 'recipes.db')

def get_db_connection():
    """Establishes connection to SQLite database with Row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def scale_value(value_str, servings):
    """
    Takes an ingredient quantity string (e.g., '200g') and scales it.
    If no number is found (e.g., 'as needed'), returns original text.
    """
    if not value_str or value_str == "None":
        return "as needed"
    
    # Use regex to find the numeric part (including decimals)
    match = re.search(r"(\d+\.?\d*)", str(value_str))
    
    # If no number is found, it's text like "as needed", so just return it
    if not match:
        return value_str

    # Extract the unit part (e.g., 'g', 'ml', 'cups')
    unit = re.sub(r"(\d+\.?\d*)", "", str(value_str)).strip()
    
    num = float(match.group(1))
    total = num * int(servings)
    
    # Formatting: Remove .0 if it's an integer, otherwise keep 1 decimal place
    val = str(int(total)) if total.is_integer() else f"{total:.1f}"
    return f"{val} {unit}".strip()

def scale_step_text(text, servings):
    """
    Finds numbers followed by units inside a sentence and scales them.
    Example: 'Add 100g paneer' -> 'Add 200g paneer' (if servings=2)
    """
    def replace_number(match):
        number = float(match.group(1))
        unit = match.group(2)
        scaled = number * int(servings)
        # Format result
        scaled_str = str(int(scaled)) if scaled.is_integer() else f"{scaled:.1f}"
        return f"{scaled_str}{unit}"

    # Regex finds numbers followed by common cooking units
    pattern = r"(\d+\.?\d*)\s*(g|kg|ml|tbsp|tsp|cup|pieces|piece)"
    return re.sub(pattern, replace_number, text, flags=re.IGNORECASE)

def find_matching_recipes(user_ingredients):
    """
    Finds top 8 recipes that match the user's spoken/detected ingredients.
    Uses partial LIKE matching so 'head cabbage' matches 'cabbage' in the DB,
    and 'bell pepper' matches 'capsicum', etc.
    """
    if not user_ingredients:
        return []

    conn = get_db_connection()
    user_ingredients = [i.lower() for i in user_ingredients]

    # Build a WHERE clause of LIKE conditions for each ingredient word
    # We also split multi-word ingredients and match on any word
    # e.g. 'head cabbage' -> checks for 'head cabbage', 'head', 'cabbage'
    conditions = []
    params = []
    for ing in user_ingredients:
        # Full ingredient name
        conditions.append("LOWER(i.item) LIKE ?")
        params.append(f"%{ing}%")
        # Also match individual words (for 'head cabbage' -> 'cabbage')
        for word in ing.split():
            if len(word) > 3:  # skip tiny words like 'a', 'of'
                conditions.append("LOWER(i.item) LIKE ?")
                params.append(f"%{word}%")

    where_clause = " OR ".join(conditions)

    query = f'''
        SELECT r.id, r.name, COUNT(i.item) as match_count
        FROM recipes r
        JOIN ingredients i ON r.id = i.recipe_id
        WHERE {where_clause}
        GROUP BY r.id
        ORDER BY match_count DESC
        LIMIT 8
    '''

    results = conn.execute(query, params).fetchall()
    conn.close()

    return [{"index": row['id'], "name": row['name']} for row in results]

def get_recipe(recipe_id, servings):
    """
    Fetches full recipe data. Scales ingredients AND step numbers based on servings.
    """
    conn = get_db_connection()
    
    # Get recipe details
    recipe_row = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
    # Get all ingredients for this recipe
    ing_rows = conn.execute('SELECT item, quantity FROM ingredients WHERE recipe_id = ?', (recipe_id,)).fetchall()
    
    conn.close()

    if not recipe_row:
        return {"error": "Recipe not found"}

    # 1. Scale quantities for the ingredient list
    scaled_ingredients = {row['item']: scale_value(row['quantity'], servings) for row in ing_rows}
    
    # 2. Scale numbers inside the instruction steps
    raw_steps = json.loads(recipe_row['steps'])
    scaled_steps = [scale_step_text(step, servings) for step in raw_steps]

    # 3. Recipe-level nutrition (from DB)
    recipe_nutrition = json.loads(recipe_row['nutrition']) if recipe_row['nutrition'] else {}

    # 4. Per-ingredient nutrition lookup
    ingredient_nutrition = {}
    for row in ing_rows:
        item = row['item'].lower().strip()
        # Try direct lookup, then with underscores replacing spaces
        label = item.replace(' ', '_')
        cal = CALORIE_MAP.get(item) or CALORIE_MAP.get(label)
        vit = VITAMIN_MAP.get(item) or VITAMIN_MAP.get(label, {})
        if cal is not None or vit:
            ingredient_nutrition[row['item']] = {
                "calories_per_100g": cal,
                "key_vitamins": vit
            }

    return {
        "name": recipe_row['name'],
        "ingredients": scaled_ingredients,
        "steps": scaled_steps,
        "nutrition": recipe_nutrition,
        "ingredient_nutrition": ingredient_nutrition
    }

def get_step(recipe_id, step_idx):
    """
    Fetches a specific step of the recipe for the cooking phase.
    """
    conn = get_db_connection()
    recipe_row = conn.execute('SELECT steps FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
    conn.close()

    if not recipe_row:
        return {"done": True}

    steps = json.loads(recipe_row['steps'])

    if 0 <= step_idx < len(steps):
        return {
            "step": steps[step_idx], 
            "done": False
        }

    return {"done": True}