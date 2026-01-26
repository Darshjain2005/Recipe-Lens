import json
import re

def load_recipes():
    with open("data/recipes.json", "r") as f:
        return json.load(f)

def scale_value(value_str, servings):
    # Regex to separate number from unit (e.g., "300g" -> 300, "g")
    match = re.match(r"(\d+\.?\d*)\s*(.*)", str(value_str))
    if match:
        num, unit = match.groups()
        return f"{float(num) * servings} {unit}".strip()
    return value_str

def find_matching_recipes(user_ingredients):
    recipes = load_recipes()
    results = []
    for i, recipe in enumerate(recipes):
        # Check if user ingredients are in the recipe keys
        match_count = sum(1 for ing in user_ingredients if ing.lower() in recipe["ingredients"])
        results.append((match_count, i))

    results.sort(reverse=True, key=lambda x: x[0])
    return [{"index": i, "name": recipes[i]["name"]} for _, i in results[:3]]

def get_recipe(index, servings):
    recipes = load_recipes()
    recipe = recipes[index]
    
    scaled_ingredients = {k: scale_value(v, servings) for k, v in recipe["ingredients"].items()}
    
    return {
        "name": recipe["name"],
        "ingredients": scaled_ingredients,
        "steps": recipe["steps"]
    }

def get_step(index, step_idx):
    recipes = load_recipes()
    recipe = recipes[index]
    if 0 <= step_idx < len(recipe["steps"]):
        return {"step": recipe["steps"][step_idx], "done": False}
    return {"done": True}