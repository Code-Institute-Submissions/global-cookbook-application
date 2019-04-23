import os
from flask import Flask, render_template, redirect, request, url_for, session, Blueprint
from flask_pymongo import PyMongo, pymongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'cookbook-database'
app.config['MONGO_URI'] = "mongodb://admin1234:admin1234@ds233238.mlab.com:33238/cookbook-database"
mongo = PyMongo(app)