from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import find_matching_recipes, get_recipe, get_step

app = Flask(__name__)
CORS(app)

@app.route("/suggest-recipes", methods=["POST"])
def suggest_recipes():
    data = request.json
    ingredients = data.get("ingredients", [])
    return jsonify(find_matching_recipes(ingredients))

@app.route("/start-cooking", methods=["POST"])
def start_cooking():
    data = request.json
    return jsonify(get_recipe(data["recipe_index"], data["servings"]))

@app.route("/next-step", methods=["POST"])
def next_step():
    data = request.json
    return jsonify(get_step(data["recipe_index"], data["step"]))

if __name__ == "__main__":
    app.run(debug=True, port=5000)