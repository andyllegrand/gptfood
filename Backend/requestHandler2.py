import json
import openai
import sqlite3
import random
import logging

RECIPES_PER_REQUEST = 5

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
      ingredient_string += ingredient + '\n'

  # Form list of used recipes in string form
  used_recipe_string = ''
  for recipe in usedRecipes:
    used_recipe_string += '{' + recipe + '}\n'

  # Form proompt
  proompt = open('proomps/genRecipeList', 'r').read()
  proompt = proompt.replace('[ingredients]', ingredient_string)
  proompt = proompt.replace('[used]', used_recipe_string)

  # Call openai api
  openai.api_key = open('key.txt', 'r').read()

  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=proompt,
    temperature=1,
    max_tokens=2339,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )

  return response.choices[0].text
  
def addRecipeToDatabase(recipe, ingredients, connection):
  """
  Adds a list of recipes to the database.
  @param recipes: string representing the recipe
  @param ingredients: list of strings representing the ingredients
  @param connection: connection to the database
  @return: None
  """
  print("here")
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
  
  connection.commit()

def generateAndAddRecipes(ingredients, usedRecipes, connection):
  """
  Generates recipes and adds them to the database.
  @param ingredients: list of ingredients representing available ingredients
  @param usedRecipes: list of recipes representing recipes that have already been used
  @param connection: connection to the database
  @return: None
  """

  completionText = None
  if not debug:
    completionText = genRecipesApiCall(ingredients, usedRecipes)
  else:
    completionText = open('sampleresponse.txt', 'r').read()
  
  # Load the text as JSON
  recipes = json.loads(completionText)

  for recipe in recipes:
    addRecipeToDatabase(recipe["name"], recipe["ingredients"], connection)

def queryDatabaseRecipes(ingredients, usedRecipes, connection):
    cursor = connection.cursor()

    # Fetch all recipe names from the database, then randomize the order
    cursor.execute('SELECT name FROM recipes')
    all_recipes = [row[0] for row in cursor.fetchall()]
    random.shuffle(all_recipes)
    print(all_recipes)

    # Fetch corresponding ingredient ids from the database
    placeholders = ', '.join('?' for ingredient in ingredients)
    cursor.execute(f"SELECT id FROM ingredients WHERE name IN ({placeholders})", ingredients)
    ingredient_ids = set(row[0] for row in cursor.fetchall())

    # Find the recipes whose ingredients are all in the provided list
    matching_recipes = []
    for recipe in all_recipes:
        if recipe in usedRecipes:
            continue

        # Fetch the ingredients for this recipe from relations
        cursor.execute('''
            SELECT ingredient_id
            FROM relations
            JOIN recipes ON relations.recipe_id = recipes.id
            WHERE recipes.name = ?
        ''', (recipe,))
        recipe_ingredient_ids = set(row[0] for row in cursor.fetchall())

        # Loop through the ingredients and check if they are all in the provided list. If so, add the recipe to matching_recipes
        if recipe_ingredient_ids.issubset(ingredient_ids):
            matching_recipes.append(recipe)

        if len(matching_recipes) == RECIPES_PER_REQUEST:
            break

    return matching_recipes

def getRecipes(ingredients, usedRecipes, databasePath):
  # Connect to the database
  conn = sqlite3.connect(databasePath)

  # Query database. If there are not enough recipes to fufill the request generate more and try again
  recipes = queryDatabaseRecipes(ingredients, usedRecipes, conn)
  
  if len(recipes) < RECIPES_PER_REQUEST:
    generateAndAddRecipes(ingredients, usedRecipes, conn)
    recipes = queryDatabaseRecipes(ingredients, usedRecipes, conn)
  
  conn.close()
  return recipes

def genDirectionsApiCall(recipe):
  """
  Calls openai api to generate directions given a recipe.
  @param recipe: string representing the recipe
  @return: raw response from openai
  """
  # Form proompt
  proompt = open('proomps/genDirections', 'r').read()
  proompt = proompt.replace('[recipe]', recipe)

  # Call openai api
  openai.api_key = open('key.txt', 'r').read()

  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=proompt,
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )

  return response.choices[0].text


def genImageApiCall(description):
  """
  Calls openai api to generate an image given a description.
  """
  pass

def generateAndAddDirections(recipe, connection):
  """
  Generates directions and adds them to the database.
  @param recipe: string representing the recipe
  @param connection: connection to the database
  @return: None
  """
  cursor = connection.cursor()

  # Add the directions to the database
  res = genDirectionsApiCall(recipe)

  # Convert to json, extract directions and image proompt
  js = json.loads(directions)
  directions = js["directions"]
  imageProompt = js["imageProompt"]

  # Generate image
  image = genImageApiCall(imageProompt)

  # Add directions and image to database
  

  cursor.execute("""
    UPDATE recipes SET directions = ? WHERE name = ?;
  """, (directions, recipe))
  connection.commit()

if __name__ == '__main__':
  ingredients = [
    "Salt",
    "Pepper",
    "Garlic (fresh or powder)",
    "Onions",
    "Olive Oil",
    "Butter",
    "Flour",
    "Sugar (white and brown)",
    "Baking Soda",
    "Baking Powder",
    "Vanilla Extract",
    "Milk",
    "Eggs",
    "Bread",
    "Pasta",
    "Rice"
  ]
  print(getRecipes(ingredients, [], 'recipes.db'))