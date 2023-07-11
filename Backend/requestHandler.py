import re
import json
import openai
import sqlite3

RECIPES_PER_REQUEST = 5

debug = False

conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

class ingredient:
    def __init__(self, name):
        self.name = name

    @classmethod
    def fromDict(cls, data):
        return cls(data['name']) 

class recipe:
    def __init__(self, name):
        self.name = name

    def toDict(self):
        return {'name': self.name}

def parseToIngredients(data_list):
    print(data_list)
    ingredients = [ingredient.fromDict(data) for data in data_list]
    return ingredients

def rlStringToJson(string):
    # Extract recipe from response using regex
    pattern = r'\{(.*?)\}'
    matches = re.findall(pattern, string.choices[0].text, re.MULTILINE | re.DOTALL)

    rlList = []
    for m in matches:
        rlList.append(recipe(m))

    print("rllist: " + str(rlList))

    # convert list of recipes to json
    return rlListToJson(rlList)

def rlListToJson(recipe_list):
    dl = []
    for recipe in recipe_list:
        dl.append(recipe.toDict())
    return json.dumps(dl)

def addRecipesToDatabase(recipes, cursor):
    return

# Use openai to generate recipes
def genRecipes(ingredients):
    # Form list of ingredients in string form
    ingredient_string = ''
    for ingredient in ingredients:
        ingredient_string += '{' + ingredient.name + '}\n'

    # Form proompt
    proompt = open('proomps/genRecipeList', 'r').read()
    proompt = proompt.replace('[ingredients]', ingredient_string)

    # Call openai api
    openai.api_key = open('key.txt', 'r').read()

    response = None

    if not debug:
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
    else:
        response = ['{r1}{r2}{r3}']

    # Extract recipes

    # Add recipes to database

def queryDatabase(ingredients):
    return []

"""
inputs a list of string representing available ingredients. First looks at cached 
recipes, then calls openai to generate recipes. Returns a list of recipes.
"""
def getRecipes(ingredients, used_recipes=[]):
    # Query database for recipes
    recipes = queryDatabase(ingredients)

    # If no recipes found, generate more recipes and try again
    if len(recipes) < RECIPES_PER_REQUEST:
        genRecipes(ingredients, cursor)
        recipes = queryDatabase(ingredients)

    # Return recipes
    return recipes
    

if __name__ == '__main__':
    with open('test.json', 'r') as f:
      ingredients = jsonToIngredients_list(f)

    recipes = getRecipes(ingredients)

    json = rlStringToJson(recipes)
