import os
from flask import Flask, render_template, redirect, request, url_for, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId



app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'milestone3'
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo = PyMongo(app)

@app.route('/')
def hello():
    return 'Flask Running'

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)


# $ heroku login
# Create a new Git repository
# Initialize a git repository in a new or existing directory

# $ cd my-project/
# $ git init
# $ heroku git:remote -a milestone3-radu
# Deploy your application
# Commit your code to the repository and deploy it to Heroku using Git.

# $ git add .
# $ git commit -am "make it better"
# $ git push heroku master            