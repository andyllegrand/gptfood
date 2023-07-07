from flask import Flask, request
import openai

import requestHandler

app = Flask(__name__)

"""
Basic backend that calls openai api to generate recipes given ingredients.
"""

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
    ingredients = requestHandler.parseToIngredients(request.get_json())

    # Get recipes from ingredients
    recipes = requestHandler.getRecipes(ingredients)

    # Encode recipes as json
    json = requestHandler.rlStringToJson(recipes)

    print(json)

    return json

if __name__ == '__main__':
    app.run()