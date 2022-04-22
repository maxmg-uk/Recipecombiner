import sqlite3

"""
tool to combine various recipes and give you a totalled up shopping list

sqlite3 for database

default recipes are for 2 people 
 
"""

USER_CHOICE = """
Enter: 
1 - To list all recipes
2 - To select your chosen recipes 
3 - Get shopping list
4 - Duplicate the shopping list (default for two people) 
5 - Export shopping list to a text file
q - To quit

Your choice: """

s_list = {}


def create_recipe_table():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS recipes(ID integer primary key, name text, ing1 text, quant1 integer, ing2 text, quant2 integer, ing3 text, quant3 integer, ing4 text, quant4 integer, ing5 text, quant5 integer, ing6 text, quant6 integer, ing7 text, quant7 integer, ing8 text, quant8 integer, ing9 text, quant9 integer, ing10 text, quant10 integer)')
    connection.commit()
    connection.close()


def list_recipes():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM recipes')
    recipes = [{'ID': row[0], 'name': row[1]} for row in cursor.fetchall()]
    connection.commit()
    connection.close()
    return recipes


def get_ingredients(recipe_id):
    # gets the ingredients for a specific recipe
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM recipes WHERE ID=:id", {"id": recipe_id})
    ingredients = cursor.fetchone()
    connection.commit()
    connection.close()
    return ingredients


def menu():
    create_recipe_table()
    user_input = input(USER_CHOICE)
    while user_input != 'q':
        if user_input == '1':
            list_recipes()
        elif user_input == '2':
            select_recipes()
        elif user_input == '3':
            print(s_list)
        elif user_input == '4':
            duplicate_shopping_list(s_list)
        elif user_input == '5':
            make_shopping_list(s_list)
        else:
            print("unknown option chosen")

        user_input = input(USER_CHOICE)


def list_recipes():
    # pull IDs and names for all recipes
    recipes = list_recipes()
    if len(recipes) > 0:
        print("The recipes in the database are:")
        for recipe in recipes:
            print(f"ID: {recipe['ID']}. Name: {recipe['name']}")
    else:
        print("No recipes yet")


def select_recipes():
    global s_list
    # get user input on recipe IDs
    recipe_choices = input("What recipes do you want? Separate Ids with spaces ").split(' ')

    # get ingredients list and amounts from database
    for i in recipe_choices:
        ingredients = list(get_ingredients(i))
        ingredients = ingredients[2:]
        ingredients = [i for i in ingredients if i]
        ing_list = list(zip(ingredients[::2], ingredients[1::2]))

        # for loop to turn list of lists into dict
        ing_dict = {}

        # loops through all ingredient and amount pairs and turns into a dictionary
        for ing in ing_list:
            key, value = ing[0], ing[1]
            ing_dict[key] = value
            if key in s_list:
                ing_dict[key] = s_list[key] + value
        s_list.update(ing_dict)


def duplicate_shopping_list(shopping_list):
    for key, value in shopping_list.items():
        shopping_list[key] = value * 2


def make_shopping_list(shopping_list):
    # clean up formatting of shopping list (remove { and ', add new lines after quantities
    shopping_list = str(shopping_list)
    shopping_list = shopping_list.replace(',', '\n').replace('{', ' ').replace('}', '')
    shopping_list = shopping_list.replace(':', '').replace("'", '').replace('"', '')

    # create/overwrite a list.txt file
    with open("list.txt", 'w') as file:
        file.write(shopping_list)


menu()
