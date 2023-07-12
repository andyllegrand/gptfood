import unittest
import logging

import flaskapp

logging.basicConfig(level=logging.DEBUG)

url = 'http://127.0.0.1:5000'
data = [
  {
    "id": 1,
    "name": "chicken",
  },
  {
    "id": 2,
    "name": "beef",
  },
  {
    "id": 3,
    "name": "pork",
  },
]

class flaskApp(unittest.TestCase):
  def test_getRecipePost(self):
    # send a post request to the flask app
    logging.debug("Sending post request to flask app...")
    response = flaskApp.app.test_client().post(url + '/recipe', json=data)
    logging.debug("Response received")

    # check that the response is valid
    self.assertEqual(response.status_code, 200)

    # check that the response is valid json
    self.assertEqual(response.is_json, True)

    # stop the flask app
    flaskApp.app.terminate()




