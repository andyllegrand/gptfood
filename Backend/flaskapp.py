from flask import Flask, request
import json

import classDefinitions
import requestHandler

app = Flask(__name__)

"""
Basic backend that calls openai api to generate recipes given ingredients.
"""
# Parse json to list of ingredients
def parseToIngredients(data_list):
    print(data_list)
    ingredients = [ingredient.fromDict(data) for data in data_list]
    return ingredients

# Parse list of recipes to json
def rlListToJson(recipe_list):
    dl = []
    for recipe in recipe_list:
        dl.append(recipe.toDict())
    return json.dumps(dl)

@app.route('/genRecipe', methods=['GET'])
def genRecipes():
    data = request.args.get_json()
    return 'Hello, World!'

@app.route('/recipe', methods=['GET', 'POST'])
def recipe():
    # Handle generic get request
    if request.method == 'GET':
        return 'hi'
    
    # Get ingredients from request
    ingredients = parseToIngredients(request.get_json())

    # Get recipes from ingredients
    recipes = requestHandler.getRecipes(ingredients)

    # Encode recipes as json
    json = requestHandler.rlStringToJson(recipes)

    return json

if __name__ == '__main__':
    app.run()