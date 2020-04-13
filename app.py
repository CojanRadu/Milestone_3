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

@app.context_processor
def all_user_names():
    #  for post in posts.find({"date": {"$lt": d}}).sort("author")
    user_names = mongo.db.users.find({"name":{ "$ne": "admin" }})
    return dict(user_names=user_names)
# MATH HELPERS ------------------------------------------------------------------------------------------


def make_exercise(action, user):

    use_nr = []
    # print(str(user['mult_opt_nr']))
    for nr in user['mult_opt_nr']:
        if (user['mult_opt_nr'][nr]):
            use_nr.append(nr)

    a_temp = random.randint(0, len(use_nr)-1)
    a = use_nr[a_temp]
    b = random.randint(1, 12)

    hint = int(a)
    keep_b = int(b)

    if user['mult_opt_can_be_inverted']:
        x = random.randint(0, 1)
        if x:
            a, b = b, a

    c = int(a)*int(b)

    """ generate options """
    if user['mult_opt_answer_type'] > 1:
        rand_range =  2*user['mult_opt_answer_type']
        range_low = hint - random.randint(1,rand_range)
        low = range_low if range_low > 0 else 1
        options = random.sample(range(low, low+rand_range), user['mult_opt_answer_type'])
        if not (keep_b in options):
            options.pop(0)
            options.insert(0, keep_b)
            random.shuffle(options)
        new_list = [x*hint for x in options]

    mult_tuple = [int(a), int(b), c, hint, new_list] if action == 'multiply' else [4, 5, 6]
    return mult_tuple


@app.route('/get_exercise')
def get_exercise():
    user = mongo.db.users.find_one({"_id": ObjectId(session['u_id'])})
    a = make_exercise('multiply', user)
    return json.dumps(a)


@app.route('/submit_answer', methods=['POST', 'GET'])
def submit_answer():
    my_dict = urllib.parse.parse_qs(request.form['str'])
    print(str(my_dict))
    exercise_doc = {'user_name': session["u_name"], 'user_id': session['u_id'] ,'date': datetime.now(
    ), 'type': 'multiply', 'nr_1': 1, 'nr_2': 2, 'nr_3': 3, 'answer': 4, 'is_correct': True, 'nr_of_tries': 1, 'session': "aaa"}
    mongo.db.exercise.insert_one(exercise_doc)
    return 'Answer was submitted'

# END HElpers -------------------------------------------------------------------------------------------------

# HOME ROUTE -------------------------------------------------------------------------------------------------
@app.route('/')
def login():
    return render_template('login.html')


# ADMIN SECTION -----------------------------------------------------------------------------------------------
admin_user = mongo.db.users.find_one({"name": "admin"})



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
    mongo.db.exercise.remove({'user_id': request.form['user_id']})
    print(str(ObjectId(request.form['user_id'])))
    return 'Deleted'    

@app.route('/update_settings', methods=['POST', 'GET'])
def update_settings():

    print(str(request.form))
    my_dict = urllib.parse.parse_qs(request.form['str'])

    """ form doesn't send any values, have to manually add """
    my_dict.setdefault('enabled', '[off]')
    my_dict.setdefault('inverted', '[off]')
    my_dict.setdefault('show_hint', '[off]')
    my_dict.setdefault('auto_submit', '[off]')
    my_dict.setdefault('show_answer', '[off]')
    my_dict.setdefault('mult_retry_opt', "['1']")

    user = admin_user if str(my_dict['user_name']) == "['admin']" else mongo.db.users.find_one(
        {"_id": ObjectId(tuple(my_dict['user_id'])[0])})

    for i in range(13):
        my_dict.setdefault('switch-'+str(i), '[off]')
        user['mult_opt_nr'][str(i)] = True if str(my_dict['switch-'+str(i)]) == "['on']" else False

    user['mult_opt_enabled'] = True if str(my_dict['enabled']) == "['on']" else False
    user['mult_opt_can_be_inverted'] = True if str(my_dict['inverted']) == "['on']" else False
    user['mult_opt_show_hint'] = True if str(my_dict['show_hint']) == "['on']" else False
    user['mult_opt_auto_submit'] = True if str(my_dict['auto_submit']) == "['on']" else False
    user['mult_opt_show_answer'] = True if str(my_dict['show_answer']) == "['on']" else False

    """" Have to update rest or wont refresh TODO  find a solution """
    """ Maybe fetch user again """

    user['mult_opt_answer_type'] = int(tuple(my_dict['mult_opt'])[0])
    user['mult_opt_exercise_nr'] = int(tuple(my_dict['ex_nr'])[0])
    user['mult_opt_retry_nr'] = int(tuple(my_dict['mult_retry_opt'])[0])

    # print (str(user_name))
    # print (str(my_dict))

    myquery = {'_id': user['_id']}

    newvalues = {"$set": {'mult_opt_enabled': user['mult_opt_enabled'],
                          'mult_opt_can_be_inverted': user['mult_opt_can_be_inverted'],
                          'mult_opt_answer_type': user['mult_opt_answer_type'],
                          'mult_opt_exercise_nr': user['mult_opt_exercise_nr'],
                          'mult_opt_retry_nr': user['mult_opt_retry_nr'],
                          'mult_opt_show_hint': user['mult_opt_show_hint'],
                          'mult_opt_auto_submit': user['mult_opt_auto_submit'],
                          'mult_opt_show_answer': user['mult_opt_show_answer'],
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
    return '--pdate'

# END ADMIN SECTION -----------------------------------------------------------------------------------------------

# User ---- SECTION -----------------------------------------------------------------------------------------------
@app.route('/exercise/<username>')
def exercise(username):
    # return '<h1>' + username + '</h1>'
    user = mongo.db.users.find_one({"_id": ObjectId(session['u_id'])})
    return render_template('exercise.html', user=user, make_exercise=make_exercise)


# TODO - FIX this
@app.route('/dologin')
def login_as_get():
    # return render_template('index.html', name="")
    return redirect(url_for('exercise', username=""))

@app.route('/dologin', methods=["POST"])
def login_as_post():
    name = request.form.get('user_name').lower()
    # return render_template('index.html', name=name)
    return redirect(url_for('exercise', username=name))

@app.route('/login_', methods=['POST', 'GET'])
def login_():

    # if request.method == 'POST':
    username = request.form.get('user_name').lower()
    # else: username = name

    session["u_name"] = username

    if (username == 'admin'):
        return redirect(url_for('show_settings'))
    else:
        now = datetime.now()

        if (mongo.db.users.count({'name': username}, limit=1) == 0):
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
            newvalues = {"$set": {'last_login': now}}

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

