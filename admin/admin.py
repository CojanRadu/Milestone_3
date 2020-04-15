from flask import Blueprint, render_template, redirect, session, url_for, request
from datetime import datetime, date
from bson.objectid import ObjectId
from six.moves import urllib
from urllib.parse import urlparse

from database import mongo

admin_bp = Blueprint('admin_bp', __name__,
    template_folder='templates',
    static_folder='static', static_url_path='assets')




# @admin_bp.route('/')
# def admin_home():
#     user = 'aa'
#     return render_template('admin/show_settings.html', user=user)

@admin_bp.route('/admin/show_users')
def show_users():
    all_users = mongo.db.users.find()
    return render_template('show_users.html', users=all_users)

@admin_bp.route('/admin/show_settings')
def show_settings():
    admin_user = mongo.db.users.find_one({"name": "admin"})
    return render_template('show_settings.html', user=admin_user)    

@admin_bp.route('/admin/edit_user_settings/<user_id>')
def edit_user_settings(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return render_template('show_settings.html', user=user)    


@admin_bp.route('/admin/delete_user', methods=['POST'])
def delete_user():
    mongo.db.users.remove({'_id': ObjectId(request.form['user_id'])})
    mongo.db.exercise.remove({'user_id': request.form['user_id']})
    return 'Deleted'    

@admin_bp.route('/update_settings', methods=['POST'])
def update_settings():

    admin_user = mongo.db.users.find_one({"name": "admin"})
    # print(str(request.form))
    my_dict = urllib.parse.parse_qs(request.form['str'])

    """ form doesn't send any values, add manually """
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
        user['mult_opt_nr'][str(i)] = True if str(
            my_dict['switch-'+str(i)]) == "['on']" else False

    user['mult_opt_enabled'] = True if str(my_dict['enabled']) == "['on']" else False
    user['mult_opt_can_be_inverted'] = True if str(my_dict['inverted']) == "['on']" else False
    user['mult_opt_show_hint'] = True if str(my_dict['show_hint']) == "['on']" else False
    user['mult_opt_auto_submit'] = True if str(my_dict['auto_submit']) == "['on']" else False
    user['mult_opt_show_answer'] = True if str(my_dict['show_answer']) == "['on']" else False

    """" Have to update rest or wont refresh TODO  find a solution Maybe fetch user again """

    user['mult_opt_answer_type'] = int(tuple(my_dict['mult_opt'])[0])
    user['mult_opt_exercise_nr'] = int(tuple(my_dict['ex_nr'])[0])
    user['mult_opt_retry_nr'] = int(tuple(my_dict['mult_retry_opt'])[0])

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

    # return 'Update'  
    return str(newvalues) 