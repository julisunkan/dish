from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
from api import search_recipes_by_name, get_recipe_by_id, parse_ingredients
from models import Base, engine

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')

Base.metadata.create_all(engine)

@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('.', 'service-worker.js', mimetype='application/javascript')

@app.route('/')
def index():
    return redirect(url_for('search'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    recipes = []
    search_query = ''
    
    if request.method == 'POST':
        search_query = request.form.get('query', '').strip()
        if search_query:
            recipes = search_recipes_by_name(search_query)
    
    return render_template('search.html', recipes=recipes, search_query=search_query)

@app.route('/recipe/<meal_id>')
def recipe_detail(meal_id):
    meal = get_recipe_by_id(meal_id)
    if not meal:
        return 'Recipe not found', 404
    
    ingredients = parse_ingredients(meal)
    
    return render_template('recipe_detail.html', meal=meal, ingredients=ingredients)

@app.route('/add-to-grocery-list/<meal_id>', methods=['POST'])
def add_to_grocery_list(meal_id):
    meal = get_recipe_by_id(meal_id)
    if not meal:
        return redirect(url_for('search'))
    
    ingredients = parse_ingredients(meal)
    
    if 'grocery_list' not in session:
        session['grocery_list'] = []
    
    grocery_list = session['grocery_list']
    
    for ingredient in ingredients:
        item_text = f"{ingredient['measure']} {ingredient['name']}".strip()
        if item_text not in grocery_list:
            grocery_list.append(item_text)
    
    session['grocery_list'] = grocery_list
    session.modified = True
    
    return redirect(url_for('recipe_detail', meal_id=meal_id))

@app.route('/grocery-list')
def grocery_list():
    grocery_items = session.get('grocery_list', [])
    return render_template('grocery_list.html', grocery_items=grocery_items)

@app.route('/clear-grocery-list', methods=['POST'])
def clear_grocery_list():
    session['grocery_list'] = []
    session.modified = True
    return redirect(url_for('grocery_list'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
