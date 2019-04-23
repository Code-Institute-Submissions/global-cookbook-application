import os
from flask import Flask, render_template, redirect, request, url_for, session, Blueprint
from flask_pymongo import PyMongo, pymongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'cookbook-database'
app.config['MONGO_URI'] = "mongodb://admin1234:admin1234@ds233238.mlab.com:33238/cookbook-database"
mongo = PyMongo(app)

@app.route('/home')
def home():
    return render_template('home.html')
    
@app.route('/cookbook', methods=["POST","GET"])
def get_cookbook():
    return render_template('recipes/food.html',
    continents = mongo.db.continents.find(),
    allergies = mongo.db.allergies.find(),
    foods = mongo.db.foods.find(),
    recipes = mongo.db.recipes.find().sort('recipe_name', pymongo.ASCENDING).limit(4))
    
@app.route('/add_recipe')
def add_recipe():
    return render_template('recipes/add_recipe.html', 
    allergies = mongo.db.allergies.find(),
    continents = mongo.db.continents.find(),
    foods = mongo.db.foods.find())
    
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
    })
    return redirect(url_for('get_cookbook'))