import json

def load_recipes():
    with open("data/recipes.json", "r", encoding="utf-8") as f:
        return json.load(f)

def scale_ingredients(ingredients, servings):
    scaled = {}
    for k, v in ingredients.items():
        try:
            qty, unit = v.split(" ", 1)
            scaled[k] = f"{float(qty) * servings} {unit}"
        except:
            scaled[k] = v
    return scaled

def get_recipe(recipe_index, servings):
    recipes = load_recipes()
    recipe = recipes[recipe_index]

    return {
        "name": recipe["name"],
        "ingredients": scale_ingredients(recipe["ingredients"], servings),
        "steps": recipe["steps"]
    }
