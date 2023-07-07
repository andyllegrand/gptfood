import re
import json
import openai

debug = False

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

def getRecipes(ingredients):
    # Form list of ingredients in string form
    ingredient_string = ''
    for ingredient in ingredients:
        ingredient_string += '{' + ingredient.name + '}\n'

    # Form proompt
    proompt = open('proomps/genRecipeList', 'r').read()
    proompt = proompt.replace('[ingredients]', ingredient_string)
    
    print(proompt)

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

    return response

if __name__ == '__main__':
    with open('test.json', 'r') as f:
      ingredients = jsonToIngredients_list(f)

    recipes = getRecipes(ingredients)

    json = rlStringToJson(recipes)
