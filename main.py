from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
from api import search_recipes_by_name, get_recipe_by_id, parse_ingredients, extract_youtube_id
from models import Base, engine

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour

Base.metadata.create_all(engine)

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

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
    error_message = None
    
    if request.method == 'POST':
        search_query = request.form.get('query', '').strip()
        if search_query:
            try:
                recipes = search_recipes_by_name(search_query)
                if recipes is None:
                    recipes = []
                    error_message = "Unable to fetch recipes. Please try again."
            except Exception as e:
                recipes = []
                error_message = "An error occurred while searching. Please try again."
                print(f"Search error: {e}")
    
    return render_template('search.html', recipes=recipes, search_query=search_query, error_message=error_message)

@app.route('/recipe/<meal_id>')
def recipe_detail(meal_id):
    try:
        meal = get_recipe_by_id(meal_id)
        if not meal:
            return render_template('error.html', message='Recipe not found'), 404
        
        ingredients = parse_ingredients(meal)
        youtube_id = extract_youtube_id(meal.get('strYoutube'))
        
        return render_template('recipe_detail.html', meal=meal, ingredients=ingredients, youtube_id=youtube_id)
    except Exception as e:
        print(f"Error fetching recipe {meal_id}: {e}")
        return render_template('error.html', message='Unable to load recipe. Please try again.'), 500

@app.route('/add-to-grocery-list/<meal_id>', methods=['POST'])
def add_to_grocery_list(meal_id):
    try:
        meal = get_recipe_by_id(meal_id)
        if not meal:
            return redirect(url_for('search'))
        
        ingredients = parse_ingredients(meal)
        
        # Initialize grocery list if it doesn't exist
        if 'grocery_list' not in session:
            session['grocery_list'] = []
        
        # Get current list and ensure it's a list
        grocery_list = list(session.get('grocery_list', []))
        
        # Add new ingredients
        for ingredient in ingredients:
            if ingredient['name']:  # Only add if ingredient name exists
                item_text = f"{ingredient['measure']} {ingredient['name']}".strip()
                if item_text not in grocery_list:
                    grocery_list.append(item_text)
        
        # Update session
        session['grocery_list'] = grocery_list
        session.modified = True
        
        return redirect(url_for('recipe_detail', meal_id=meal_id))
    except Exception as e:
        print(f"Error adding to grocery list: {e}")
        return redirect(url_for('recipe_detail', meal_id=meal_id))

@app.route('/grocery-list')
def grocery_list():
    grocery_items = list(session.get('grocery_list', []))
    return render_template('grocery_list.html', grocery_items=grocery_items)

@app.route('/clear-grocery-list', methods=['POST'])
def clear_grocery_list():
    session['grocery_list'] = []
    session.modified = True
    return redirect(url_for('grocery_list'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
