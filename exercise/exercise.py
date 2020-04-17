from flask import Blueprint, render_template, redirect, session, url_for, request
from datetime import datetime, date
from bson.objectid import ObjectId
import json
from six.moves import urllib
from urllib.parse import urlparse, parse_qs

from database import mongo
from exercise.exercise_funct import make_exercise
# from app import make_exercise


exercise_bp = Blueprint('exercise_bp', __name__,
    template_folder='templates',
    static_folder='static', static_url_path='assets')

@exercise_bp.route('/')
def show_login():
    return render_template('login/login.html')

@exercise_bp.route('/get_exercise', methods=['POST', 'GET'])
def get_exercise():
    parsed = urlparse(str(request))

    ex_type = str(parse_qs(parsed.query)['ex_type'][0]).replace("' [GET]>", "")
    user = mongo.db.users.find_one({"_id": ObjectId(session['u_id'])})
    a = make_exercise(ex_type, user)
    return json.dumps(a)



@exercise_bp.route('/submit_answer', methods=['POST', 'GET'])
def submit_answer():
    parsed = str(urllib.parse.parse_qs(request.form['data_object'])).replace("'", '"').replace("[", "").replace("]", "")
    json_form = (json.loads(parsed))

    json_form.setdefault('hint_nr', 0)
    json_form.setdefault('ex_retry', 0)
    json_form.setdefault('ex_curr_nr', 0)
    json_form.setdefault('total_exercise', 0)

    print(json_form)
    is_correct = True if json_form['correct_answer'] == json_form['answer'] else False
    is_hint = True if int(json_form['hint_nr']) != 0 else False

    exercise_doc = {'user_name': session["u_name"], 'user_id': session['u_id'], 'type': json_form['ex_type'],
                    'date': datetime.now(), 'nr_1': int(json_form['nr_1']), 'nr_2': int(json_form['nr_2']), 'correct': int(json_form['correct_answer']),
                    'answer': int(json_form['answer']), 'is_correct': is_correct, 'nr_of_tries': int(json_form['ex_retry']), 'used_hint': is_hint,
                    'exercise_nr': int(json_form['ex_curr_nr']), 'total_exercise': int(json_form['total_exercise'])
                    }

    print(str(exercise_doc))
    mongo.db.exercise.insert_one(exercise_doc)

    return 'Answer was submitted'

@exercise_bp.route('/<username>')
def exercise(username):
    # return '<h1>' + username + '</h1>'
    user = mongo.db.users.find_one({"_id": ObjectId(session['u_id'])})
    return render_template('exercise.html', user=user, make_exercise=make_exercise)    
