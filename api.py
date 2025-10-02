import requests

BASE_URL = 'https://www.themealdb.com/api/json/v1/1'

def search_recipes_by_name(name):
    try:
        response = requests.get(f'{BASE_URL}/search.php', params={'s': name})
        response.raise_for_status()
        data = response.json()
        return data.get('meals', [])
    except requests.exceptions.RequestException as e:
        print(f'Error fetching recipes: {e}')
        return []

def get_recipe_by_id(meal_id):
    try:
        response = requests.get(f'{BASE_URL}/lookup.php', params={'i': meal_id})
        response.raise_for_status()
        data = response.json()
        meals = data.get('meals', [])
        return meals[0] if meals else None
    except requests.exceptions.RequestException as e:
        print(f'Error fetching recipe details: {e}')
        return None

def parse_ingredients(meal):
    ingredients = []
    for i in range(1, 21):
        ingredient_key = f'strIngredient{i}'
        measure_key = f'strMeasure{i}'
        
        ingredient = meal.get(ingredient_key, '').strip()
        measure = meal.get(measure_key, '').strip()
        
        if ingredient:
            ingredients.append({
                'name': ingredient,
                'measure': measure
            })
    
    return ingredients
