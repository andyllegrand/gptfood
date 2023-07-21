import unittest
import sqlite3
import json
import logging
import os

from flaskapp import app
from resetdb import resetdb

DATABASE_PATH = 'tests/test_recipes.db'

logging.basicConfig(level=logging.DEBUG)

data = [
  {
    "id": 1,
    "name": "shredded cheese",
  },
  {
    "id": 2,
    "name": "tortilla",
  },
  {
    "id": 3,
    "name": "salsa",
  },
  {
    "id": 4,
    "name": "refried beans",
  },
  {
    "id": 5,
    "name": "pizza dough",
  },
  {
    "id": 6,
    "name": "pizza sauce",
  },
  {
    "id": 7,
    "name": "rice",
  },
  {
    "id": 8,
    "name": "pasta",
  },
  {
    "id": 9,
    "name": "bread",
  },
  {
    "id": 10,
    "name": "eggs",
  },
  {
    "id": 11,
    "name": "milk",
  },
  {
    "id": 12,
    "name": "butter",
  },
  {
    "id": 13,
    "name": "flour",
  },
  {
    "id": 14,
    "name": "sugar",
  },
  {
    "id": 15,
    "name": "salt",
  },
  {
    "id": 16,
    "name": "pepper",
  },
  {
    "id": 17,
    "name": "olive oil",
  },
  {
    "id": 18,
    "name": "garlic",
  },
  {
    "id": 19,
    "name": "onions",
  },
  {
    "id": 20,
    "name": "tomatoes",
  },
]

json_data = json.dumps(data)

class testRequestHandler(unittest.TestCase):

    def setUp(self):
      self.app = app.test_client()

    def test_get(self):
      res = self.app.get('/recipeList')
      assert res.data.decode() == 'hi'

    def test_recipeList(self):
      logging.debug("test_recipeList")
      
      # reset database
      resetdb(DATABASE_PATH)
      app.config['DATABASE_PATH'] = DATABASE_PATH

      used = []

      # send example request
      d = {"ingredients": data, "used": used}
      res = self.app.post('/recipeList', json=d)

      # check that the status code is valid
      self.assertEqual(res.status_code, 200)

      # extract info
      response = res.get_json()

      # check that the response has length 5
      self.assertEqual(len(response), 5)

      # check that the response is a list of dictionaries
      for recipe in response:
        self.assertTrue(isinstance(recipe, dict))

      # verification beyond this point is difficult because the response is ai generated. log the response and check it manually
      for recipe in response:
        logging.debug(recipe)

      # call again and run same tests with used recipes
      used = response
      d = {"ingredients": data, "used": used}
      res = self.app.post('/recipeList', json=d)
      self.assertEqual(res.status_code, 200)
      response = res.get_json()
      self.assertEqual(len(response), 5)

    def test_getDirectionsAndImage(self):
       # reset database
      resetdb(DATABASE_PATH)
      app.config['DATABASE_PATH'] = DATABASE_PATH

      # generate some recipes
      used = []
      d = {"ingredients": data, "used": used}
      res = self.app.post('/recipeList', json=d)
      self.assertEqual(res.status_code, 200)

      # get the first recipe
      response = res.get_json()
      recipe = response[0]

      # get directions
      d = {"recipe": recipe}
      res = self.app.post('/recipeDirections', json=d)

      # check that the status code is valid
      self.assertEqual(res.status_code, 200)

      # send image request
      d = {"recipe": recipe}
      res = self.app.post('/recipeImage', json=d)

      # check that the status code is valid
      self.assertEqual(res.status_code, 200)

      # Get the first 8 bytes of the image
      im = res.data
      magic_number = im[:8]

      # Check if the magic number matches PNG
      assert magic_number == b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A', 'Response is not a PNG image'
      

