import requests
import sqlite3

# Define database name
DATABASE_NAME = 'C:/Users/betul/PycharmProjects/upschool-gpt-app/homework_cat_facts.db'

def get_cat_facts():
  """Retrieves cat facts from the API and saves them to the database."""
  try:
    response = requests.get("https://cat-fact.herokuapp.com/facts")
    if response.status_code == 200:
      data = response.json()
      print("API Response:", data)

      for fact in data:
        cat_fact_text = fact["text"]
        save_cat_fact(cat_fact_text)

      return "Cat facts retrieved and saved!"
    else:
      print(f"Error retrieving data. Status code: {response.status_code}")
      return None
  except requests.exceptions.RequestException as e:
    print(f"Error making API request: {e}")
    return None

def save_cat_fact(fact):
  """Saves a cat fact to the database."""
  try:
    with sqlite3.connect(DATABASE_NAME) as connection:
      cursor = connection.cursor()

      # Create the table if it doesn't exist
      cursor.execute('''CREATE TABLE IF NOT EXISTS cat_facts (fact)''')

      # Insert the cat fact into the table
      cursor.execute("INSERT INTO cat_facts VALUES (?)", (fact,))
      print("Data inserted:", fact)
  except sqlite3.Error as e:
      print(f"Database error: {e}")

def view_cat_facts():
  """Retrieves and displays saved cat facts."""
  try:
    with sqlite3.connect(DATABASE_NAME) as connection:
      cursor = connection.cursor()

      # Execute query to retrieve facts
      cursor.execute("SELECT * FROM cat_facts")

      # Fetch all facts as a list of tuples
      facts = cursor.fetchall()

      # Print each fact
      if facts:
        print("Saved Cat Facts:")
        for fact in facts:
          print(fact[0])
      else:
        print("No cat facts found in the database.")
  except sqlite3.Error as e:
      print(f"Database error: {e}")

# Get and save cat facts
get_cat_facts()

# View the saved cat facts
view_cat_facts()
