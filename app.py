import os
import random
import json
from flask import Flask, render_template, redirect, session, url_for, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime, date
from six.moves import urllib
from urllib.parse import urlparse


app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'milestone3'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

app.secret_key = "randstring12345"

mongo = PyMongo(app)

# HELPERS ----------------------------------------------------------------------------------------------------
def make_exercise(action, user):
    
    use_nr = []
    # print(str(user['mult_opt_nr']))
    for nr in user['mult_opt_nr']:
        if (user['mult_opt_nr'][nr]):
            use_nr.append(nr)

    a_temp = random.randint(0, len(use_nr)-1)
    a = use_nr[a_temp]
    b = random.randint(1, 12)

    if user['mult_opt_can_be_inverted']:
        x = random.randint(0,1)
        if x:
            c=b
            b=a
            a=c

    c = int(a)*int(b)
    mult_tuple = [int(a), int(b), c] if action == 'multiply' else [4,5,6]
    return mult_tuple

@app.route('/get_exercise')
def get_exercise():
    user = mongo.db.users.find_one({"_id": ObjectId(session['u_id'])})
    a = make_exercise('multiply', user)
    return json.dumps(a)


@app.route('/submit_answer', methods=['POST', 'GET'])
def submit_answer():
    return 'Answer was submitted'

# END HElpers -------------------------------------------------------------------------------------------------    

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
    return render_template('admin/admin_show_settings.html', user=admin_user)


@app.route('/edit_user_settings/<user_id>')
def edit_user_settings(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return render_template('admin/admin_show_settings.html', user=user)


@app.route('/show_users')
def show_users():
    all_users = mongo.db.users.find()
    return render_template('admin/admin_show_users.html', users=all_users)


@app.route('/delete_user', methods=['POST'])
def delete_user():
    # return '<h1>DELETED ' + request.form['user_id'] + ' !</h1>'
    mongo.db.users.remove({'_id': ObjectId(request.form['user_id'])})


@app.route('/update_settings', methods=['POST', 'GET'])
def update_settings():

    my_dict = urllib.parse.parse_qs(
        request.form['str'], keep_blank_values=True)

    my_dict.setdefault('enabled', '[off]')
    my_dict.setdefault('inverted', '[off]')

    user = admin_user if str(my_dict['user_name']) == "['admin']" else mongo.db.users.find_one(
        {"_id": ObjectId(tuple(my_dict['user_id'])[0])})

    for i in range(13):
        my_dict.setdefault('switch-'+str(i), '[off]')
        user['mult_opt_nr'][str(i)] = True if str(
            my_dict['switch-'+str(i)]) == "['on']" else False
    user['mult_opt_enabled'] = True if str(
        my_dict['enabled']) == "['on']" else False
    user['mult_opt_can_be_inverted'] = True if str(
        my_dict['inverted']) == "['on']" else False

    """" Have to update rest or wont refresh TODO  find a solution """

    user['mult_opt_answer_type'] = int(tuple(my_dict['mult_opt'])[0])
    user['mult_opt_exercise_nr'] = int(tuple(my_dict['ex_nr'])[0])

    # print (str(user_name))
    # print (str(my_dict))

    myquery = {'_id': user['_id']}

    newvalues = {"$set": {'mult_opt_enabled': user['mult_opt_enabled'],
                        'mult_opt_can_be_inverted': user['mult_opt_can_be_inverted'],
                        'mult_opt_answer_type': user['mult_opt_answer_type'],
                        'mult_opt_exercise_nr': user['mult_opt_exercise_nr'],
                        "mult_opt_nr.0": user['mult_opt_nr']['0'],
                        "mult_opt_nr.1": user['mult_opt_nr']['1'],
                        "mult_opt_nr.2": user['mult_opt_nr']['2'],
                        "mult_opt_nr.3": user['mult_opt_nr']['3'],
                        "mult_opt_nr.4": user['mult_opt_nr']['4'],
                        "mult_opt_nr.5": user['mult_opt_nr']['5'],
                        "mult_opt_nr.6": user['mult_opt_nr']['6'],
                        "mult_opt_nr.7": user['mult_opt_nr']['7'],
                        "mult_opt_nr.8": user['mult_opt_nr']['8'],
                        "mult_opt_nr.9": user['mult_opt_nr']['9'],
                        "mult_opt_nr.10": user['mult_opt_nr']['10'],
                        "mult_opt_nr.11": user['mult_opt_nr']['11'],
                        "mult_opt_nr.12": user['mult_opt_nr']['12']
                }}

    mongo.db.users.update_one(myquery, newvalues)

    # return  str(user['mult_opt_nr']) + '\n' + str(newvalues)
    return None
    
# END ADMIN SECTION -----------------------------------------------------------------------------------------------

# User ---- SECTION -----------------------------------------------------------------------------------------------
@app.route('/exercise/<username>')
def exercise(username):
    # return '<h1>' + username + '</h1>'
    user = mongo.db.users.find_one({"_id": ObjectId(session['u_id'])})
    return render_template('exercise.html', user=user, make_exercise=make_exercise)


@app.route('/login_', methods=['POST'])
def login_():
    username = request.form.get('user_name').lower()
    session["u_name"] = username
    
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
            session["u_new"] = True
        else:
            user = mongo.db.users.find_one({"name": username})
            user['last_login'] = now

            myquery = {'_id': user['_id']}
            newvalues = { "$set": {'last_login': now}}

            mongo.db.users.update_one(myquery, newvalues)
            insert_id = user['_id']

        # return redirect(url_for('exercise', username=username, id = insert_id))
        session["u_id"] = str(insert_id)
        return redirect(url_for('exercise', username=username))
    # return '<h1>LOGIN</h1>'
# END User SECTION -----------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)
