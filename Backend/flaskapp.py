from flask import Flask, request
import json

from classDefinitions import ingredient, recipe
import requestHandler

app = Flask(__name__)

"""
Basic backend that calls openai api to generate recipes given ingredients.
"""
# Parse json to list of ingredients
def parseToIngredients(data_list):
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

    # Parse ingredients to list of strings
    ingredients = [ingredient.name for ingredient in ingredients]

    # Get recipes from ingredients
    recipes = requestHandler.getRecipes(ingredients)

    # Form list of recipes from strings
    recipes = [recipe(data) for data in recipes]

    # Encode recipes as json
    json = requestHandler.rlStringToJson(recipes)

    return json

if __name__ == '__main__':
    app.run()