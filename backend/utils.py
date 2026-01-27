import json
import re

def load_recipes():
    try:
        with open("data/recipes.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def scale_value(value_str, servings):
    # Separates "300g" into 300 and "g"
    match = re.match(r"(\d+\.?\d*)\s*(.*)", str(value_str))
    if match:
        num, unit = match.groups()
        total = float(num) * int(servings)
        clean_num = int(total) if total.is_integer() else total
        return f"{clean_num} {unit}".strip()
    return value_str

def find_matching_recipes(user_ingredients):
    recipes = load_recipes()
    results = []
    for i, recipe in enumerate(recipes):
        recipe_ings = [k.lower() for k in recipe.get("ingredients", {}).keys()]
        match_count = sum(1 for ing in user_ingredients if ing.lower() in recipe_ings)
        results.append((match_count, i))
    results.sort(reverse=True, key=lambda x: x[0])
    return [{"index": i, "name": recipes[i]["name"]} for count, i in results[:3] if count > 0]

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
    steps = recipe.get("steps", [])
    if 0 <= step_idx < len(steps):
        return {"step": steps[step_idx], "done": False}
    return {"done": True}