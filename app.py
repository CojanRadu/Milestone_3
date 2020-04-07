import os
from flask import Flask, render_template, redirect, session, url_for, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime, date


app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'milestone3'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

app.secret_key = "randstring12345"

mongo = PyMongo(app)


@app.route('/')
def login():
    return render_template('login.html')


# ADMIN SECTION -----------------------------------------------------------------------------------------------
admin_user = mongo.db.users.find_one({"name": "admin"})

@app.route('/admin')
def admin():
    return render_template("admin/admin_base.html", admin=admin_user)

@app.route('/show_settings')
def show_settings():
    return render_template('admin/admin_show_settings.html', admin=admin_user)

@app.route('/show_users')
def show_users():
    all_users = mongo.db.users.find()
    return render_template('admin/admin_show_users.html', users = all_users)

# END ADMIN SECTION -----------------------------------------------------------------------------------------------


@app.route('/exercise/<username>')
def exercise(username):
    # return '<h1>' + username + '</h1>'
    return render_template('exercise.html', username=username)


@app.route('/login_', methods=['POST'])
def login_():
    username = request.form.get('user_name')
    session["username"] = username
    # add here update DB
    
    if (username == 'admin'):
        return redirect(url_for('show_settings'))
    else:    
        now =  datetime.now()

        if (mongo.db.users.count({ 'name': username }, limit = 1) == 0):
            """ DUPLICATE admin current settings when creating a new user """
            admin_user = mongo.db.users.find_one({"name": "admin"})
            admin_user['_id'] = ObjectId()
            admin_user['name'] = username
            admin_user['add_date'] = now
            admin_user['last_login'] = now
            insert_id = mongo.db.users.insert_one(admin_user).inserted_id
        else:
            user = mongo.db.users.find_one({"name": username})
            user['last_login'] = now

            myquery = {'_id': user['_id']}
            newvalues = { "$set": {'last_login': now}}

            mongo.db.users.update_one(myquery, newvalues)

            # mongo.db.users.update_one({'_id': user['_id']}, {'last_login': now})
            insert_id = user['_id']

        return redirect(url_for('exercise', username=username, id = insert_id))
    # return '<h1>LOGIN</h1>'


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)
