from flask import Flask, request, jsonify, send_file
import json
import logging

from customError import CustomError
from classDefinitions import ingredient, recipe
import requestHandler

app = Flask(__name__)
app.config["DATABASE_PATH"] = "/Users/andylegrand/xcode/gptfood/Backend/tests/recipes.db"

errorCodes = json.loads(open('errorCodes.json', 'r').read())

"""
Basic backend that calls openai api to generate recipes given ingredients.
"""
# Parse json to list of ingredients
def parseToIngredients(data_list):
  logging.debug(f"Data list: {data_list}")
  logging.debug(type(data_list))

  ingredients = [ingredient.fromDict(data) for data in data_list]
  logging.debug("done")
  return ingredients

def parseToRecipe(data_list):
  recipes = [recipe.fromDict(data) for data in data_list]
  return recipes

# Parse list of recipes to json
def rlListToJson(recipe_list):
  dl = []
  for recipe in recipe_list:
      dl.append(recipe.toDict())
  return jsonify(dl)

@app.route('/recipeList', methods=['GET', 'POST'])
def recipeList():
    # Handle generic get request
    if request.method == 'GET':
        return 'hi'
    
    try: 
      # Get ingredients and used recipes from request
      js = request.get_json()

      ingredients = parseToIngredients(js["ingredients"])
      used = parseToRecipe(js["used"])

      # Parse ingredients and used recipes to lists of strings
      ingredients = [ingredient.name for ingredient in ingredients]
      used = [recipe.name for recipe in used]

      logging.debug(f"parsed: {ingredients}")
      logging.debug(f"parsed: {used}")

      # Get recipes from ingredients. If the backend fails, return and log error message
      try:
        recipes = requestHandler.getRecipes(ingredients, used, app.config["DATABASE_PATH"])
      except CustomError as e:
        logging.error("Error in backend")
        e.log()
        return None, e.error_code
      
  
      logging.debug(f"Recipesresponse: {recipes}")

      # Form list of recipes from strings
      recipes = [recipe(data) for data in recipes]

      # Encode recipes as json
      json = rlListToJson(recipes)

      return json, errorCodes["SUCCESS"]
    except:
       logging.error("Error in flaskapp.py")
       return None, errorCodes["FLASK_APP"] 


@app.route('/recipeDirections', methods=['GET', 'POST'])
def recipeDirections():
  # Handle generic get request
  if request.method == 'GET':
      return 'slatt'

  try:
    # Get recipe name from request
    js = request.get_json()
    rec = recipe.fromDict(js["recipe"])
    recipe_name = rec.name

    # Get directions from recipe name
    try:
      directions = requestHandler.getDirections(recipe_name, app.config["DATABASE_PATH"])
    except CustomError as e:
      e.log()
      return None, e.error_code

    return directions, errorCodes["SUCCESS"]
  except:
    logging.error("Error in flaskapp.py")
    return None, errorCodes["FLASK_APP"]



@app.route('/recipeImage', methods=['GET', 'POST'])
def getImage():
  # Handle generic get request
  if request.method == 'GET':
      return 'slatt'

  try:
    # Get recipe name from request
    js = request.get_json()
    rec = recipe.fromDict(js["recipe"])
    recipe_name = rec.name

    # Get directions from recipe name
    imagePath = requestHandler.getImage(recipe_name, app.config["DATABASE_PATH"])

    return send_file(imagePath, 'image/png'), errorCodes["SUCCESS"]
  
  except:
    logging.error("Error in flaskapp.py")

if __name__ == '__main__':
    app.run()