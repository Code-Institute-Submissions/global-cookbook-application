import os
from flask import Flask, render_template, redirect, request, url_for, session, Blueprint
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId
from flask_bcrypt import bcrypt
import pygal
from pygal.style import DefaultStyle

# Basic setup for the application - Flask Logic and connecting Pymongo to the MongoDB instance
app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'cookbook-database'
app.config['MONGO_URI'] = "mongodb://admin1234:admin1234@ds233238.mlab.com:33238/cookbook-database"
mongo = PyMongo(app)

# Base route for the application - It will show the login page if there is no username available in the browsers session
@app.route('/')
def index():
    if 'username' in session:
        return render_template('home.html')
    return render_template('authentication/login.html')
    
# Login route to enable users to add their username to the browsers session    
@app.route('/login', methods = ['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})
    if login_user:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('home'))
    # Error handling for Login - if the user does not have login details or enters the wrong password it will display this page
    return render_template('authentication/loginfail.html')

# Route to enable new users to Register to the application
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})
        # Error handling to check that user does not already exist in the database
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name': request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('get_cookbook'))
        return render_template('authentication/registerfail.html')
    return render_template('authentication/register.html')

# Route to enable the user to clear their session and Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
    
# Route to display the links to 'Continent' pages    
@app.route('/home')
def home():
    return render_template('home.html')

# Route to display all of the recipes available on the application
@app.route('/cookbook', methods=["POST","GET"])
def get_cookbook():
    offset= 1
    return render_template('recipes/food.html',
    continents = mongo.db.continents.find(),
    allergies = mongo.db.allergies.find(),
    foods = mongo.db.foods.find(),
    offset = offset,
    count = mongo.db.recipes.find().count(),
    recipes = mongo.db.recipes.find().sort('recipe_name', pymongo.ASCENDING).limit(4))
    
# Route to enable users to see a detailed view of each recipe    
@app.route('/view_recipe/<recipe_id>', methods=["POST", "GET"])
def view_recipe(recipe_id):
    # Adds a like and dislike system to the application
    voted = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)},
        {
            "likes" : 1,
            'dislikes': 1
        })
    vote_storage = []
    vote_storage.append(voted)
    # If the user presses Like or Dislike it will add one like or dislike to the recipes entry on the database
    if request.method == "POST":
        if request.form['likesdislikes'] == "like":
            likes = vote_storage[0]["likes"] + 1
            mongo.db.recipes.update_one({'_id': ObjectId(recipe_id) }, { '$set' : { "likes" : likes}})
            return redirect(url_for('get_cookbook'))
        elif request.form['likesdislikes'] == "dislike":
            dislikes = vote_storage[0]['dislikes'] + 1
            mongo.db.recipes.update_one( {'_id': ObjectId(recipe_id) },  {'$set': { 'dislikes' : dislikes }} )
            return redirect(url_for('get_cookbook'))
    return render_template('recipes/viewrecipe.html',
    recipes = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)}))
    
# Route to enable user to add a new recipe to the database    
@app.route('/add_recipe')
def add_recipe():
    return render_template('recipes/addrecipe.html', 
    allergies = mongo.db.allergies.find(),
    continents = mongo.db.continents.find(),
    foods = mongo.db.foods.find(),
    users = mongo.db.users.find())
    
# Logic to ensure the users input is correctly added to the database    
@app.route('/insert_recipe', methods=["POST"])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(
    {
        'continent_name': request.form.get("continent_name"),
        'recipe_name': request.form.get("recipe_name"),
        'food_type': request.form.get("food_type"),
        'recipe_time': request.form.get('recipe_time'),
        'recipe_servings': request.form.get('recipe_servings'),
        'recipe_ingredients': request.form.get('recipe_ingredients'),
        'recipe_instructions1': request.form.get('recipe_instructions1'),
        'recipe_instructions2': request.form.get('recipe_instructions2'),
        'recipe_instructions3': request.form.get('recipe_instructions3'),
        'recipe_instructions4': request.form.get('recipe_instructions4'),
        'allergy_name': request.form.get('allergy_name'),
        'users': request.form.get('users'),
        'likes': 0,
        'dislikes': 0
    })
    return redirect(url_for('get_cookbook'))
    
# Route to enable users to edit recipe entries    
@app.route('/edit_recipe/<recipe_name>')
def edit_recipe(recipe_name):
    recipes = mongo.db.recipes.find_one({"_id": ObjectId(recipe_name)})
    return render_template('recipes/editrecipe.html', 
    continents = mongo.db.continents.find(),
    foods = mongo.db.foods.find(),
    users = mongo.db.users.find(),
    allergies = mongo.db.allergies.find(),
    recipes=recipes)

# Route to enable user input to successfully update in the database    
@app.route('/update_recipe/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    recipe = mongo.db.recipes
    recipe.update({"_id": ObjectId(recipe_id)},
    {
        'continent_name': request.form.get("continent_name"),
        'recipe_name': request.form.get("recipe_name"),
        'food_type': request.form.get("food_type"),
        'recipe_time': request.form.get('recipe_time'),
        'recipe_servings': request.form.get('recipe_servings'),
        'recipe_ingredients': request.form.get('recipe_ingredients'),
        'recipe_instructions1': request.form.get('recipe_instructions1'),
        'recipe_instructions2': request.form.get('recipe_instructions2'),
        'recipe_instructions3': request.form.get('recipe_instructions3'),
        'recipe_instructions4': request.form.get('recipe_instructions4'),
        'allergy_name': request.form.get('allergy_name'),
        'users': request.form.get('users'),
        'likes': 0,
        'dislikes' : 0
    })
    return redirect(url_for('get_cookbook'))
    
# Route to allow users to delete a recipe from the application
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id":ObjectId(recipe_id)})
    return redirect(url_for('get_cookbook'))
    
# Route to allow users to view all allergens to the application   
@app.route('/allergies')
def allergies():
    return render_template('allergies/allergies.html',
    count = mongo.db.allergies.find().count(),
    allergies = mongo.db.allergies.find())
    
# Route to allow users to add new allergens to the application    
@app.route('/new_allergy')
def new_allergy():
    return render_template('allergies/addallergy.html',
    allergies = mongo.db.allergies.find())
    
#Logic to track when a user has added a new allergen    
@app.route('/insert_allergy', methods=["POST"])
def insert_allergy():
    allergies = mongo.db.allergies
    allergies.insert_one(request.form.to_dict())
    return redirect(url_for('allergies'))
    
# Allows a user to remove an unnecessary allergen from the application   
@app.route('/delete_allergy/<allergy_name>')
def delete_allergy(allergy_name):
    mongo.db.allergies.remove({"_id": ObjectId(allergy_name)})
    return redirect(url_for('allergies'))

# Individual routes for the continent pages    
@app.route('/europe')
def europe():
    offset= 1
    return render_template('continents/europe.html',
    offset = offset,
    count = mongo.db.recipes.find({"continent_name" : "Europe"}).count(),
    recipes = mongo.db.recipes.find({"continent_name" : "Europe"}).sort('recipe_name', pymongo.ASCENDING).limit(4))
    
@app.route('/namerica')
def namerica():
    offset = 1
    return render_template('continents/namerica.html',
    offset = offset,
    count = mongo.db.recipes.find({"continent_name" : "North America"}).count(),
    recipes = mongo.db.recipes.find({"continent_name" : "North America"}).sort('recipe_name', pymongo.ASCENDING).limit(4))

@app.route('/samerica')
def samerica():
    offset = 1
    return render_template('continents/samerica.html',
    offset = offset,
    count = mongo.db.recipes.find({"continent_name" : "South America"}).count(),
    recipes = mongo.db.recipes.find({"continent_name" : "South America"}).sort('recipe_name', pymongo.ASCENDING).limit(4))
    
@app.route('/asia')
def asia():
    offset = 1
    return render_template('continents/asia.html',
    offset = offset,
    count = mongo.db.recipes.find({"continent_name" : "Asia"}).count(),
    recipes = mongo.db.recipes.find({"continent_name" : "Asia"}).sort('recipe_name', pymongo.ASCENDING).limit(4))
    
@app.route('/africa')
def africa():
    offset = 1
    return render_template('continents/africa.html',
    offset = offset,
    count = mongo.db.recipes.find({"continent_name" : "Africa"}).count(),
    recipes = mongo.db.recipes.find({"continent_name" : "Africa"}).sort('recipe_name', pymongo.ASCENDING).limit(4))
    
@app.route('/australia')
def australia():
    offset = 1
    return render_template('continents/australia.html',
    offset = offset,
    count = mongo.db.recipes.find({"continent_name" : "Australia"}).count(),
    recipes = mongo.db.recipes.find({"continent_name" : "Australia"}).sort('recipe_name', pymongo.ASCENDING).limit(4))
    
    
# individual routes for the foodtype pages
@app.route('/chicken')
def chicken():
    offset = 1
    return render_template('foodtype/chicken.html',
    offset = offset,
    count = mongo.db.recipes.find({"food_type" : "Chicken"}).count(),
    recipes = mongo.db.recipes.find({"food_type" : "Chicken"}).sort('recipe_name', pymongo.ASCENDING).limit(4))
    
@app.route('/beef')
def beef():
    offset = 1
    return render_template('foodtype/beef.html',
    offset = offset,
    count = mongo.db.recipes.find({"food_type" : "Beef"}).count(),
    recipes = mongo.db.recipes.find({"food_type" : "Beef"}).sort('recipe_name', pymongo.ASCENDING).limit(4))

@app.route('/lamb')
def lamb():
    offset = 1
    return render_template('foodtype/lamb.html',
    offset = offset,
    count = mongo.db.recipes.find({"food_type" : "Lamb"}).count(),
    recipes = mongo.db.recipes.find({"food_type" : "Lamb"}).sort('recipe_name', pymongo.ASCENDING).limit(4))
    
@app.route('/pork')
def pork():
    offset = 1
    return render_template('foodtype/pork.html',
    offset = offset,
    count = mongo.db.recipes.find({"food_type" : "Pork"}).count(),
    recipes = mongo.db.recipes.find({"food_type" : "Pork"}).sort('recipe_name', pymongo.ASCENDING).limit(4))
    
@app.route('/fish')
def fish():
    offset = 1
    return render_template('foodtype/fish.html',
    offset = offset,
    count = mongo.db.recipes.find({"food_type" : "Fish"}).count(),
    recipes = mongo.db.recipes.find({"food_type" : "Fish"}).sort('recipe_name', pymongo.ASCENDING).limit(4))
    
@app.route('/vegetarian')
def vegetarian():
    offset = 1
    return render_template('foodtype/vegetarian.html',
    offset = offset,
    count = mongo.db.recipes.find({"food_type" : "Vegetarian"}).count(),
    recipes = mongo.db.recipes.find({"food_type" : "Vegetarian"}).sort('recipe_name', pymongo.ASCENDING).limit(4))
    
@app.route('/vegan')
def vegan():
    offset = 1
    return render_template('foodtype/vegan.html',
    offset = offset,
    count = mongo.db.recipes.find({"food_type" : "Vegan"}).count(),
    recipes = mongo.db.recipes.find({"food_type" : "Vegan"}).sort('recipe_name', pymongo.ASCENDING).limit(4))
    
#Route to display the users recipes that they have added to the application    
@app.route('/myrecipes')
def myrecipes():
    offset = 1
    return render_template('recipes/myrecipes.html',
    offset = offset,
    count = mongo.db.recipes.find({'users': session['username']}).count(),
    recipes = mongo.db.recipes.find({'users': session['username']}).sort('recipe_name', pymongo.ASCENDING).limit(4))
    
# Basic pagination logic for each page that requires pagination    
@app.route('/page<offset>', methods=['POST', 'GET'])
def next_page(offset):
    count = mongo.db.recipes.find().count()
    recipes = mongo.db.recipes.find().skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('recipes/food.html', recipes=recipes, offset=offset, count=count)

@app.route('/page<offset>', methods=['POST', 'GET'])
def prev_page(offset):
    count = mongo.db.recipes.find().count()
    recipes = mongo.db.recipes.find().skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('recipes/food.html', recipes=recipes, offset=offset, count=count)
    
@app.route('/europe<offset>', methods=['POST', 'GET'])
def next_europe_page(offset):
    count = mongo.db.recipes.find({"continent_name" : "Europe"}).count()
    recipes = mongo.db.recipes.find({"continent_name" : "Europe"}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('continents/europe.html', recipes=recipes, offset=offset, count=count)

@app.route('/europe<offset>', methods=['POST', 'GET'])
def prev_europe_page(offset):
    count = mongo.db.recipes.find({"continent_name" : "Europe"}).count()
    recipes = mongo.db.recipes.find({"continent_name" : "Europe"}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('continents/europe.html', recipes=recipes, offset=offset, count=count)
    
@app.route('/namerica<offset>', methods=['POST', 'GET'])
def next_namerica_page(offset):
    count = mongo.db.recipes.find({"continent_name" : "North America"}).count()
    recipes = mongo.db.recipes.find({"continent_name" : "North America"}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('continents/namerica.html', recipes=recipes, offset=offset, count=count)

@app.route('/namerica<offset>', methods=['POST', 'GET'])
def prev_namerica_page(offset):
    count = mongo.db.recipes.find({"continent_name" : "North America"}).count()
    recipes = mongo.db.recipes.find({"continent_name" : "North America"}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('continents/namerica.html', recipes=recipes, offset=offset, count=count)
    
@app.route('/samerica<offset>', methods=['POST', 'GET'])
def next_samerica_page(offset):
    count = mongo.db.recipes.find({"continent_name" : "South America"}).count()
    recipes = mongo.db.recipes.find({"continent_name" : "South America"}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('continents/samerica.html', recipes=recipes, offset=offset, count=count)

@app.route('/samerica<offset>', methods=['POST', 'GET'])
def prev_samerica_page(offset):
    count = mongo.db.recipes.find({"continent_name" : "South America"}).count()
    recipes = mongo.db.recipes.find({"continent_name" : "South America"}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('continents/samerica.html', recipes=recipes, offset=offset, count=count)
    
@app.route('/asia<offset>', methods=['POST', 'GET'])
def next_asia_page(offset):
    count = mongo.db.recipes.find({"continent_name" : "Asia"}).count()
    recipes = mongo.db.recipes.find({"continent_name" : "Asia"}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('continents/asia.html', recipes=recipes, offset=offset, count=count)

@app.route('/asia<offset>', methods=['POST', 'GET'])
def prev_asia_page(offset):
    count = mongo.db.recipes.find({"continent_name" : "Asia"}).count()
    recipes = mongo.db.recipes.find({"continent_name" : "Asia"}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('continents/asia.html', recipes=recipes, offset=offset, count=count)
    
@app.route('/africa<offset>', methods=['POST', 'GET'])
def next_africa_page(offset):
    count = mongo.db.recipes.find({"continent_name" : "Africa"}).count()
    recipes = mongo.db.recipes.find({"continent_name" : "Africa"}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('continents/africa.html', recipes=recipes, offset=offset, count=count)

@app.route('/africa<offset>', methods=['POST', 'GET'])
def prev_africa_page(offset):
    count = mongo.db.recipes.find({"continent_name" : "Africa"}).count()
    recipes = mongo.db.recipes.find({"continent_name" : "Africa"}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('continents/africa.html', recipes=recipes, offset=offset, count=count)
    
@app.route('/australia<offset>', methods=['POST', 'GET'])
def next_australia_page(offset):
    count = mongo.db.recipes.find({"continent_name" : "Australia"}).count()
    recipes = mongo.db.recipes.find({"continent_name" : "Australia"}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('continents/australia.html', recipes=recipes, offset=offset, count=count)

@app.route('/australia<offset>', methods=['POST', 'GET'])
def prev_australia_page(offset):
    count = mongo.db.recipes.find({"continent_name" : "Australia"}).count()
    recipes = mongo.db.recipes.find({"continent_name" : "Australia"}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('continents/australia.html', recipes=recipes, offset=offset, count=count)
    
@app.route('/beef<offset>', methods=['POST', 'GET'])
def next_beef_page(offset):
    count = mongo.db.recipes.find({"food_type" : "Beef"}).count()
    recipes = mongo.db.recipes.find({"food_type" : "Beef"}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('foodtype/beef.html', recipes=recipes, offset=offset, count=count)

@app.route('/beef<offset>', methods=['POST', 'GET'])
def prev_beef_page(offset):
    count = mongo.db.recipes.find({"food_type" : "Beef"}).count()
    recipes = mongo.db.recipes.find({"food_type" : "Beef"}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('foodtype/beef.html', recipes=recipes, offset=offset, count=count)

@app.route('/chicken<offset>', methods=['POST', 'GET'])
def next_chicken_page(offset):
    count = mongo.db.recipes.find({"food_type" : "Chicken"}).count()
    recipes = mongo.db.recipes.find({"food_type" : "Chicken"}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('foodtype/chicken.html', recipes=recipes, offset=offset, count=count)

@app.route('/chicken<offset>', methods=['POST', 'GET'])
def prev_chicken_page(offset):
    count = mongo.db.recipes.find({"food_type" : "Chicken"}).count()
    recipes = mongo.db.recipes.find({"food_type" : "Chicken"}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('foodtype/chicken.html', recipes=recipes, offset=offset, count=count)
    
@app.route('/fish<offset>', methods=['POST', 'GET'])
def next_fish_page(offset):
    count = mongo.db.recipes.find({"food_type" : "Fish"}).count()
    recipes = mongo.db.recipes.find({"food_type" : "Fish"}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('foodtype/fish.html', recipes=recipes, offset=offset, count=count)

@app.route('/fish<offset>', methods=['POST', 'GET'])
def prev_fish_page(offset):
    count = mongo.db.recipes.find({"food_type" : "Fish"}).count()
    recipes = mongo.db.recipes.find({"food_type" : "Fish"}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('foodtype/fish.html', recipes=recipes, offset=offset, count=count)
    
@app.route('/lamb<offset>', methods=['POST', 'GET'])
def next_lamb_page(offset):
    count = mongo.db.recipes.find({"food_type" : "Lamb"}).count()
    recipes = mongo.db.recipes.find({"food_type" : "Lamb"}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('foodtype/lamb.html', recipes=recipes, offset=offset, count=count)

@app.route('/lamb<offset>', methods=['POST', 'GET'])
def prev_lamb_page(offset):
    count = mongo.db.recipes.find({"food_type" : "Lamb"}).count()
    recipes = mongo.db.recipes.find({"food_type" : "Lamb"}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('foodtype/lamb.html', recipes=recipes, offset=offset, count=count)
    
@app.route('/pork<offset>', methods=['POST', 'GET'])
def next_pork_page(offset):
    count = mongo.db.recipes.find({"food_type" : "Pork"}).count()
    recipes = mongo.db.recipes.find({"food_type" : "Pork"}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('foodtype/pork.html', recipes=recipes, offset=offset, count=count)

@app.route('/pork<offset>', methods=['POST', 'GET'])
def prev_pork_page(offset):
    count = mongo.db.recipes.find({"food_type" : "Pork"}).count()
    recipes = mongo.db.recipes.find({"food_type" : "Pork"}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('foodtype/pork.html', recipes=recipes, offset=offset, count=count)
    
@app.route('/vegan<offset>', methods=['POST', 'GET'])
def next_vegan_page(offset):
    count = mongo.db.recipes.find({"food_type" : "Vegan"}).count()
    recipes = mongo.db.recipes.find({"food_type" : "Vegan"}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('foodtype/vegan.html', recipes=recipes, offset=offset, count=count)

@app.route('/vegan<offset>', methods=['POST', 'GET'])
def prev_vegan_page(offset):
    count = mongo.db.recipes.find({"food_type" : "Vegan"}).count()
    recipes = mongo.db.recipes.find({"food_type" : "Vegan"}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('foodtype/vegan.html', recipes=recipes, offset=offset, count=count)
    
@app.route('/vegetarian<offset>', methods=['POST', 'GET'])
def next_vegetarian_page(offset):
    count = mongo.db.recipes.find({"food_type" : "Vegetarian"}).count()
    recipes = mongo.db.recipes.find({"food_type" : "Vegetarian"}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('foodtype/vegetarian.html', recipes=recipes, offset=offset, count=count)

@app.route('/vegertarian<offset>', methods=['POST', 'GET'])
def prev_vegetarian_page(offset):
    count = mongo.db.recipes.find({"food_type" : "Vegetarian"}).count()
    recipes = mongo.db.recipes.find({"food_type" : "Vegetarian"}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('foodtype/vegetarian.html', recipes=recipes, offset=offset, count=count)
    
@app.route('/myrecipes<offset>', methods=['POST', 'GET'])
def next_myrecipes_page(offset):
    count = mongo.db.recipes.find({'users': session['username']}).count()
    recipes = mongo.db.recipes.find({'users': session['username']}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('recipes/myrecipes.html', recipes=recipes, offset=offset, count=count)

@app.route('/myrecipes<offset>', methods=['POST', 'GET'])
def prev_myrecipes_page(offset):
    count = mongo.db.recipes.find({'users': session['username']}).count()
    recipes = mongo.db.recipes.find({'users': session['username']}).skip((int(offset)-1) * 4).sort("recipe_name", pymongo.ASCENDING).limit(4)
    return render_template('recipes/myrecipes.html', recipes=recipes, offset=offset, count=count)
    
# Route to display statistics for the users    
@app.route('/stats')
def stats():
    a_chart = pygal.Bar(print_values=True, style=DefaultStyle(
                  value_font_family='helvetica',
                  value_font_size=30))
    a_chart.title = "Recipes By Continent"
    a_chart.add("Europe", mongo.db.recipes.find({"continent_name" : "Europe"}).count())
    a_chart.add("North America", mongo.db.recipes.find({"continent_name" : "North America"}).count())
    a_chart.add("South America", mongo.db.recipes.find({"continent_name" : "South America"}).count())
    a_chart.add("Asia", mongo.db.recipes.find({"continent_name" : "Asia"}).count())
    a_chart.add("Africa", mongo.db.recipes.find({"continent_name" : "Africa"}).count())
    a_chart.add("Australia", mongo.db.recipes.find({"continent_name" : "Australia"}).count())
    chart1 = a_chart.render_data_uri()
    
    b_chart = pygal.HorizontalBar(print_values=True, style=DefaultStyle(
                  value_font_family='helvetica',
                  value_font_size=30))
    b_chart.title = "Recipes By Food Type"
    b_chart.add("Beef", mongo.db.recipes.find({"food_type" : "Beef"}).count())
    b_chart.add("Chicken", mongo.db.recipes.find({"food_type" : "Chicken"}).count())
    b_chart.add("Fish", mongo.db.recipes.find({"food_type" : "Fish"}).count())
    b_chart.add("Lamb", mongo.db.recipes.find({"food_type" : "Lamb"}).count())
    b_chart.add("Pork", mongo.db.recipes.find({"food_type" : "Pork"}).count())
    b_chart.add("Vegan", mongo.db.recipes.find({"food_type" : "Vegan"}).count())
    b_chart.add("Vegetarian", mongo.db.recipes.find({"food_type" : "Vegetarian"}).count())
    chart2 = b_chart.render_data_uri()
    
    c_chart = pygal.Bar(print_values=True, style=DefaultStyle(
                  value_font_family='helvetica',
                  value_font_size=30))
    c_chart.title = "Allergens in recipes"
    c_chart.add("Lactose", mongo.db.recipes.find({'allergy_name': 'Lactose'}).count())
    c_chart.add("Peanuts", mongo.db.recipes.find({'allergy_name': 'Peanuts'}).count())
    c_chart.add("Gluten", mongo.db.recipes.find({'allergy_name': 'Gluten'}).count())
    c_chart.add("Sesemee Seeds", mongo.db.recipes.find({'allergy_name': 'Sessemee seeds'}).count())
    c_chart.add("Seafood", mongo.db.recipes.find({'allergy_name': 'Seafood'}).count())
    c_chart.add("Beans", mongo.db.recipes.find({'allergy_name' : 'Beans'}).count())
    
    chart3 = c_chart.render_data_uri()
    
    return render_template( 'stats.html', chart1 = chart1, chart2 = chart2, chart3 = chart3)
    
if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)
    

