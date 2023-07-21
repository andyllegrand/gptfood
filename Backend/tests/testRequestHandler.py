import unittest
import sqlite3
import json
import logging
import os

import requestHandler
from resetdb import resetdb

DATABASE_PATH = 'tests/test_recipes.db'

logging.basicConfig(level=logging.DEBUG)

class testRequestHandler(unittest.TestCase):
    def test_recipeDatabase(self):
      recipes = [
         #  recipe with 2 ingredients
         {
            "name":"Recipe 1",
            "ingredients":["ingredient 1", "ingredient 2"],
         },

          #  recipe with 3 ingredients. superset of recipe 1.
          {
            "name":"Recipe 2",
            "ingredients":["ingredient 1", "ingredient 2", "ingredient 3"],
          },

          #  recipe with 2 unique ingredients
          {
            "name":"Recipe 3",
            "ingredients":["ingredient 3", "ingredient 4"],
          },
      ]
      logging.debug("Testing recipe database...")
      
      # setup database
      logging.debug("Setting up database...")
      resetdb(DATABASE_PATH)
      logging.debug("Done")


      # add some recipes to the database
      logging.debug("Adding recipes to database...")
      connection = sqlite3.connect(DATABASE_PATH)
      cursor = connection.cursor()
      for recipe in recipes:
        requestHandler.addRecipeToDatabase(recipe["name"], recipe["ingredients"], connection)
      logging.debug("Done")

      # check that recipes were added to the database
      logging.debug("verifying recipes were added to database...")
      cursor.execute('SELECT name FROM recipes')
      database_recipes = [row[0] for row in cursor.fetchall()]
      self.assertEqual(len(database_recipes), 3)
      allrecipes = []

      for recipe in recipes:
        allrecipes.append(recipe["name"])

      self.assertEqual(set(database_recipes), set(allrecipes))
      logging.debug("Done")

      # check that ingredients were added to the database
      logging.debug("verifying ingredients were added to database...")
      cursor.execute('SELECT name FROM ingredients')
      database_ingredients = [row[0] for row in cursor.fetchall()]
      self.assertEqual(len(database_ingredients), 4)

      allingredients = []
      for recipe in recipes:
        for ingredient in recipe["ingredients"]:
          allingredients.append(ingredient)
      
      self.assertEqual(set(database_ingredients), set(allingredients))
      logging.debug("Done")

      # check that relations were added to the database
      logging.debug("verifying relations were added to database...")
      for recipe in recipes:
        cursor.execute('''
            SELECT ingredient_id
            FROM relations
            JOIN recipes ON relations.recipe_id = recipes.id
            WHERE recipes.name = ?
        ''', (recipe["name"],))
        database_ingredients = [row[0] for row in cursor.fetchall()]
        self.assertEqual(len(database_ingredients), len(recipe["ingredients"]))
      logging.debug("Done")

      # query with no ingredients. Should retrurn no recipes.
      expectedRes = []
      res = requestHandler.queryDatabaseRecipes([], [], connection)
      self.assertEqual(sorted(expectedRes), sorted(res))

      # query with ingredients for recipe 1. Should only return recipe 1.
      expectedRes = ["Recipe 1"]
      res = requestHandler.queryDatabaseRecipes(["ingredient 1", "ingredient 2"], [], connection)
      self.assertEqual(sorted(expectedRes), sorted(res))

      # query with ingredients for recipe 2. Should return recipe 1 and 2.
      expectedRes = ["Recipe 1", "Recipe 2"]
      res = requestHandler.queryDatabaseRecipes(["ingredient 1", "ingredient 2", "ingredient 3"], [], connection)
      self.assertEqual(sorted(expectedRes), sorted(res))

      # query with ingredients for recipe 3. Should return recipe 3.
      expectedRes = ["Recipe 3"]
      res = requestHandler.queryDatabaseRecipes(["ingredient 3", "ingredient 4"], [], connection)
      self.assertEqual(sorted(expectedRes), sorted(res))

      # query for all ingredients. Should return recipes 1 2 and 3.
      expectedRes = ["Recipe 1", "Recipe 2","Recipe 3"]
      res = requestHandler.queryDatabaseRecipes(["ingredient 1", "ingredient 2", "ingredient 3", "ingredient 4"], [], connection)
      self.assertEqual(sorted(expectedRes), sorted(res))

      # query for ingredients for recipe 1 and 2, but mark 1 as used. Should return recipe 2.
      usedRecipes = ["Recipe 1"]
      expectedRes = ["Recipe 2"]
      res = requestHandler.queryDatabaseRecipes(["ingredient 1", "ingredient 2", "ingredient 3"], usedRecipes, connection)
      self.assertEqual(sorted(expectedRes), sorted(res))

    # makes sure the api call to gpt-3 is working. The main issue here is the response not being in proper json format, so run 5 times to make sure it works.
    def test_genRecipesApiCall(self):
      # example recipe list
      ingredients = [
        "shredded cheese",
        "tortilla",
        "salsa",
        "refried beans",
        "pizza dough",
        "pizza sauce",
      ]
      usedRecipes = []

      logging.debug("path: " + os.getcwd())

      for i in range(5):
        res = requestHandler.genRecipesApiCall(ingredients, usedRecipes, proomptPath="./proomps/genRecipeList.txt")
        logging.debug("res: ")
        logging.debug(res)

        passed = True
        try:
          js = json.loads(res)
          logging.debug()
        except:
          passed = False
          logging.debug("failed to parse json")

        self.assertEqual(len(js), 5)


    def test_getRecipes(self):
      # example recipe list
      ingredients = [
        "shredded cheese",
        "tortilla",
        "salsa",
        "refried beans",
        "pizza dough",
        "pizza sauce",
      ]

      ingredients2 = [
        "shredded cheese",
        "tortilla",
        "salsa",
        "refried beans",
        "pizza dough",
        "pizza sauce",
      ]
      usedRecipes = []

      # reset database
      resetdb(DATABASE_PATH)

      # call generate recipes. This should call gpt and generate 5 new recipes
      response = requestHandler.getRecipes(ingredients, usedRecipes, DATABASE_PATH)

      logging.debug("response: ")
      logging.debug(response)

      # check that the response is a list of 5 recipes
      self.assertEqual(len(response), 5)

      # make the same call again. This should return the same 5 recipes
      response2 = requestHandler.getRecipes(ingredients, usedRecipes, DATABASE_PATH)
      self.assertEqual(sorted(response), sorted(response2))

      # mark the first recipe as used, and call again. This should return 4 recipes from the original 5 and 1 new recipe
      usedRecipes = [response[0]]
      response3 = requestHandler.getRecipes(ingredients, usedRecipes, DATABASE_PATH)
      self.assertEqual(len(response3), 5)

      shared_recipes = 0
      for recipe in response:
        if recipe in response3:
          shared_recipes += 1
      self.assertEqual(shared_recipes, 4)

    def test_imageSaving(self):
      image_url = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
      requestHandler.downloadImage(image_url, "tests/images/test.png")
      self.assertTrue(os.path.exists("tests/images/test.png"))

    def test_imageGenerationAndSaving(self):
      description = "Yeti eating ice cream on a boat in Antarctica."

      # call api
      response = requestHandler.genImageApiCall(description)

      # make sure that response is a valid url
      self.assertTrue(response.startswith("https://"))

      # save image
      requestHandler.downloadImage(response, "tests/images/test2.png")

      # make sure image was saved
      self.assertTrue(os.path.exists("tests/images/test2.png"))

    def test_addDirectionsToDb(self):
      # reset database
      resetdb(DATABASE_PATH)

      # add a recipe to the database
      connection = sqlite3.connect(DATABASE_PATH)
      cursor = connection.cursor()
      requestHandler.addRecipeToDatabase("test recipe", ["ingredient 1", "ingredient 2"], connection)

      # add directions and image for this recipe
      requestHandler.addDirectionsToDatabase("test recipe", "test directions", "tests/images/test.png", connection)

      # check that the directions and image were added to the database
      cursor.execute('SELECT directions, imagePath FROM recipes WHERE name = "test recipe"')
      directions, image_path = cursor.fetchone()
      self.assertEqual(directions, "test directions")
    
    def testRecipeAndImageGeneration(self):
      # reset database
      resetdb(DATABASE_PATH)

      # add a recipe to the database
      connection = sqlite3.connect(DATABASE_PATH)
      cursor = connection.cursor()
      requestHandler.addRecipeToDatabase("pizza", ["crust", "sauce", "cheese"], connection)

      # generate directions and image for this recipe
      requestHandler.generateAndAddDirections("pizza", connection, "tests/images/")

      # check that the directions and image were added to the database
      cursor.execute('SELECT directions, imagePath FROM recipes WHERE name = "pizza"')
      directions, image_path = cursor.fetchone()
      self.assertTrue(directions != "")
      self.assertTrue(os.path.exists(image_path))

      
    

      




