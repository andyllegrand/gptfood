import sqlite3

def resetdb(path):
  conn = sqlite3.connect(path)
  cursor = conn.cursor()

  cursor.execute("DROP TABLE IF EXISTS relations;")
  cursor.execute("DROP TABLE IF EXISTS recipes;")
  cursor.execute("DROP TABLE IF EXISTS ingredients;")

  cursor.execute("""
      CREATE TABLE recipes (
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL UNIQUE,
          directions TEXT,
          imagePath TEXT UNIQUE
      );
  """)

  cursor.execute("""
      CREATE TABLE ingredients (
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL UNIQUE
      );
  """)

  cursor.execute("""
      CREATE TABLE relations (
          id INTEGER PRIMARY KEY,
          recipe_id INTEGER,
          ingredient_id INTEGER,
          FOREIGN KEY (recipe_id) REFERENCES recipes (id),
          FOREIGN KEY (ingredient_id) REFERENCES ingredients (id)
      );
  """)

  conn.commit()
  conn.close()
  print("done")


if __name__ == "__main__":
  resetdb("/Users/andylegrand/xcode/gptfood/Backend/recipes.db")
