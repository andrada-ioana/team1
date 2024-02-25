import csv
import Levenshtein


def find_most_similar_ingredient(ingredient_dict, target_ingredient):
    """
    Find the most similar ingredient in the dictionary to the target ingredient.
    :param ingredient_dict: the dictionary containing the ingredients
    :param target_ingredient: the ingredient to find the most similar ingredient to
    :return:
    """
    # Initialize variables to keep track of the best match and its distance
    best_match = None
    best_distance = float('inf')  # Start with a large value

    # Iterate through each ingredient in the dictionary
    for ingredient in ingredient_dict:
        # Calculate the Levenshtein distance between the target and current ingredient
        distance = Levenshtein.distance(target_ingredient, ingredient)

        # Update the best match if the current ingredient is closer
        if distance < best_distance:
            best_match = ingredient
            best_distance = distance

    return best_match


def create_ingredient_dict():
    """
    Create a dictionary with ingredients as keys and an empty list as values.
    :return: the ingredients dictionary
    """
    file_path = r'D:\Andrada\HealthApp\repository\ingredients_data.csv'

    # Initialize an empty dictionary
    ingredients_dict = {}

    # Read the CSV file
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # Iterate through each row in the CSV file
        for row in reader:
            # 'Short_Description' is the column containing ingredient names
            ingredient_name = row['Food']
            # Add the ingredient to the dictionary with a default value of an empty list
            ingredients_dict[ingredient_name] = {"Calories": float(row["Calories"])}

    return ingredients_dict


def add_recipes_to_the_ingredients_dict():
    """
    For each ingredient, we want to add the recipes that contain that ingredient to the ingredients_dict.
    :return: the list of recipes and the updated ingredients dictionary
    """
    recipes_file_path = r'D:\Andrada\HealthApp\repository\recipes_data.csv'

    recipes_dict = {}
    ingredients_dict = {}
    # Read the second CSV file with recipes
    with open(recipes_file_path, 'r') as recipes_file:
        reader = csv.DictReader(recipes_file, delimiter=',')
        for row in reader:
            recipe_title = row['Title']
            recipe_ingredients = row['Ingredients'].split()  # Assuming ingredients are space separated
            recipes_dict[recipe_title] = recipe_ingredients  # Add the recipe to the recipes_dict

            # For each ingredient in the recipe, we add the recipe to the list of recipes for that ingredient
            for ingredient in recipe_ingredients:
                ingredient = ingredient.strip()  # Remove leading/trailing spaces
                if ingredient in ingredients_dict:
                    ingredients_dict[ingredient].append(recipe_title)
                else:
                    ingredients_dict[ingredient] = [recipe_title]

    return recipes_dict, ingredients_dict


def calculate_content_score(user_liked_ingredients, recipe_ingredients):
    """
    Calculate the content score for a recipe based on the presence of liked ingredients.
    :param user_liked_ingredients: the set of ingredients liked by the user
    :param recipe_ingredients: the list of ingredients in the recipe
    :return: the content score
    """
    common_ingredients = set(user_liked_ingredients) & set(recipe_ingredients)
    content_score = len(common_ingredients) / len(user_liked_ingredients) if user_liked_ingredients else 0
    return content_score


def calculate_nutritional_score(recipe_ingredients, ingredients_dict):
    """
    Calculate the nutritional score for a recipe based on the nutritional values of the ingredients.
    :param recipe_ingredients: the list of ingredients in the recipe
    :param ingredients_dict: the dictionary containing the nutritional values of the ingredients
    :return: the nutritional score
    """
    score = 0
    for ingredient in recipe_ingredients:
        # Calculate the nutritional score for each ingredient
        most_similar_ingredient = find_most_similar_ingredient(ingredients_dict, ingredient)
        score += float(ingredients_dict[most_similar_ingredient]["Calories"])
    return score


def select_best_recipe(user_liked_ingredients, recipes_with_an_ingredient, recipes_dict, ingredients_dict):
    """
    Select the best recipe based on the user's liked ingredients and on the nutritional values of the recipes.
    :param user_liked_ingredients: the set of ingredients liked by the user
    :param recipes_with_an_ingredient: the dictionary containing the ingredients
    :param recipes_dict: the dictionary containing the recipes
    :param ingredients_dict: the dictionary containing the nutritional values of the ingredients
    :return: the best recipe
    """
    best_recipe = None
    best_score = float('-inf')
    best_nutritional_score = float('+inf')

    for ingredient in user_liked_ingredients:
        recipes_user_liked_ingredient = recipes_with_an_ingredient[ingredient]
        for recipe_title in recipes_user_liked_ingredient:
            recipe_ingredients = recipes_dict[recipe_title]
            # Calculate content score for each recipe
            content_score = calculate_content_score(user_liked_ingredients, recipe_ingredients)
            # Calculate nutritional score for each recipe
            nutritional_score = calculate_nutritional_score(recipe_ingredients, ingredients_dict)
            # Update best recipe if a higher score is found
            if nutritional_score < best_nutritional_score:
                best_nutritional_score = nutritional_score
                if content_score > best_score:
                    best_score = content_score
                    best_recipe = recipe_title

    return best_recipe


def user_meal(id, ingredients_dict, recipes_dict, recipes_with_an_ingredient):
    """
    Select the best recipe for a user based on the user's liked ingredients and on the nutritional values of the recipes.
    :param id: the user's id
    :param ingredients_dict: the dictionary containing the nutritional values of the ingredients
    :param recipes_dict: the dictionary containing the recipes
    :param recipes_with_an_ingredient: the dictionary containing the ingredients
    :return:
    """
    user_file_path = r'D:\Andrada\HealthApp\repository\users_data.csv'
    with open(user_file_path, 'r') as user_file:
        reader = csv.DictReader(user_file, delimiter=',')
        for row in reader:
            user_name = row['NAME']
            user_id = row['ID']
            user_surname = row['SURNAME']
            user_favorite_ingredients = row['FAV_INGREDIENTS'].split()
            if user_id == id:
                best_recipe = select_best_recipe(user_favorite_ingredients, recipes_with_an_ingredient, recipes_dict,
                                                 ingredients_dict)
                if best_recipe:
                    return best_recipe
                else:
                    raise Exception("No suitable recipes found.")
        raise Exception("User not found.")


def menu():
    print("Welcome to WellWay! Please select an option:")
    print("1. Get a recipe recommendation")
    print("2. Exit")


if __name__ == '__main__':
    ingredients_dict = create_ingredient_dict()
    recipes_dict, recipes_with_an_ingredient = add_recipes_to_the_ingredients_dict()
    while True:
        menu()
        option = input("Please select an option: ")
        if option == "1":
            user_id = input("Please enter your user id: ")
            try:
                print(user_meal(user_id, ingredients_dict, recipes_dict, recipes_with_an_ingredient))
            except Exception as e:
                print(e)
        elif option == "2":
            break
        else:
            print("Invalid option. Please try again.")
