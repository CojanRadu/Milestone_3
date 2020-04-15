import os
from flask import Flask, render_template, redirect, session, url_for, request, Blueprint, g
# from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime, date


from database import mongo


from login.login import login_bp
from admin.admin import admin_bp
from exercise.exercise import exercise_bp

app = Flask(__name__)

app.register_blueprint(login_bp, url_prefix='/login')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(exercise_bp, url_prefix='/exercise')

app.config["MONGO_DBNAME"] = 'milestone3'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
app.secret_key = "randstring12345"


mongo.init_app(app)


""" NOT used just an example TODO - test for blueprints """ 
@app.context_processor
def all_user_names():
    #  for post in posts.find({"date": {"$lt": d}}).sort("author")
    user_names = mongo.db.users.find({"name": {"$ne": "admin"}})
    return dict(user_names=user_names)


@app.route('/')
def login():
    return redirect('/login')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)
