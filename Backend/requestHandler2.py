import re
import json
import openai
import sqlite3

RECIPES_PER_REQUEST = 5
DATABASE_PATH = 'my_database.db'

debug = False

def genRecipesApiCall(ingredients, usedRecipes):
  """
  Calls openai api to generate recipes given ingredients.
  @param ingredients: list of ingredients representing available ingredients
  @param usedRecipes: list of recipes representing recipes that have already been used
  @return: raw response from openai
  """
# Form list of ingredients in string form
  ingredient_string = ''
  for ingredient in ingredients:
      ingredient_string += '{' + ingredient + '}\n'

  # Form list of used recipes in string form
  used_recipe_string = ''
  for recipe in usedRecipes:
    used_recipe_string += '{' + recipe + '}\n'

  # Form proompt
  proompt = open('proomps/genRecipeList', 'r').read()
  proompt = proompt.replace('[ingredients]', ingredient_string)

  # Call openai api
  openai.api_key = open('key.txt', 'r').read()

  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=proompt,
    suffix="\n\n",
    temperature=1,
    max_tokens=256,
    top_p=0.5,
    frequency_penalty=0,
    presence_penalty=0
  )

  return response
  
def addRecipeToDatabase(recipe, ingredients, connection):
  """
  Adds a list of recipes to the database.
  @param recipes: string representing the recipe
  @param ingredients: list of strings representing the ingredients
  @param connection: connection to the database
  @return: None
  """

  cursor = connection.cursor()

  # Add the recipe to the database
  cursor.execute("""
    INSERT INTO recipes (name, directions) VALUES (?, NULL);
  """, (recipe,))
  recipeId = cursor.lastrowid

  # Add the ingredients to the database
  ingredientIds = []
  for ingredient in ingredients:
    cursor.execute("""
      INSERT OR IGNORE INTO ingredients (name) VALUES (?);
    """, (ingredient,))
    ingredientIds.append(cursor.lastrowid)

  # Add the relations to the database
  for ingredientId in ingredientIds:
      cursor.execute("""
        INSERT INTO relations (recipe_id, ingredient_id) VALUES (?, ?);
      """, (recipeId, ingredientId))

def generateAndAddRecipes(ingredients, usedRecipes, connection):
  """
  Generates recipes and adds them to the database.
  @param ingredients: list of ingredients representing available ingredients
  @param usedRecipes: list of recipes representing recipes that have already been used
  @param connection: connection to the database
  @return: None
  """

  response = None
  if not debug:
    response = genRecipesApiCall(ingredients, usedRecipes)
  else:
    response = ""

  

  return

def queryDatabase(ingredients, usedRecipes, connection):
  return

def getRecipes(ingredients, usedRecipes):
  return
    


