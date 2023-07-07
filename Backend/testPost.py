import requests

#url = 'https://192.168.1.27'
url = 'http://127.0.0.1:5000/recipe'

response = requests.post(url, json=
    [
      {
        "id": 1,
        "name": "apple"
      },
      {
        "id": 2,
        "name": "bannana"
      },
      {
        "id": 3,
        "name": "carrot"
      }
    ])

print(response.text)