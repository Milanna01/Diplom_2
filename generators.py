import random
from faker import Faker

faker = Faker()

def generate_email():
    return faker.email()

def generate_password():
    return faker.password()

def generate_name():
    return faker.first_name()

def generate_ingredients_list(ingredients_count, available_ingredients):
    """Генерирует список ингредиентов из доступных"""
    if len(available_ingredients) < ingredients_count:
        ingredients_count = len(available_ingredients)
    ingredients = random.sample(available_ingredients, ingredients_count)
    return ingredients