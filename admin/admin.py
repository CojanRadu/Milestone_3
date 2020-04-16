from flask import Blueprint, render_template, redirect, session, url_for, request
from datetime import datetime, date
from bson.objectid import ObjectId
from six.moves import urllib
from urllib.parse import urlparse

from database import mongo

admin_bp = Blueprint('admin_bp', __name__,
    template_folder='templates',
    static_folder='static', static_url_path='assets')


ex_types = list(('add', 'substract', 'multiply', 'divide'))  

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
    # print(type(admin_user))
    return render_template('show_settings.html', user=admin_user, ex=ex_types)    

@admin_bp.route('/admin/edit_user_settings/<user_id>')
def edit_user_settings(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return render_template('show_settings.html', user=user,  ex=ex_types)    


@admin_bp.route('/admin/delete_user', methods=['POST'])
def delete_user():
    mongo.db.users.remove({'_id': ObjectId(request.form['user_id'])})
    mongo.db.exercise.remove({'user_id': request.form['user_id']})
    return 'Deleted'    

@admin_bp.route('/update_settings', methods=['POST'])
def update_settings():

    # admin_user = mongo.db.users.find_one({"name": "admin"})
    # print(str(request.form))
    my_dict = urllib.parse.parse_qs(request.form['str'])

    # """ form doesn't send any values, add manually """
    my_dict.setdefault('enabled', '[off]')
    my_dict.setdefault('show_answer', '[off]')
    my_dict.setdefault('inverted', '[off]')
    my_dict.setdefault('show_hint', '[off]')
    my_dict.setdefault('auto_submit', '[off]')
    
    my_dict.setdefault('retry_nr', "['1']")
    my_dict.setdefault('answer_type', "['1']")

    user =  mongo.db.users.find_one({"_id": ObjectId(tuple(my_dict['user_id'])[0])})
    ex_type = str(my_dict['ex_type']).replace("['", "").replace("']", "")

    for i in range(13):
        my_dict.setdefault('switch_'+str(i), '[off]')
        user['exercise'][ex_type]['opt_nr'][str(i)] = True if str(my_dict['switch_'+str(i)]) == "['on']" else False

    # user['exercise'][ex_type]['opt_nr']['1'] = True

    user['opt_enabled'] = True if str(my_dict['enabled']) == "['on']" else False
    user['opt_can_be_inverted'] = True if str(my_dict['inverted']) == "['on']" else False
    user['opt_show_hint'] = True if str(my_dict['show_hint']) == "['on']" else False
    user['opt_auto_submit'] = True if str(my_dict['auto_submit']) == "['on']" else False
    user['opt_show_answer'] = True if str(my_dict['show_answer']) == "['on']" else False

    # """" Have to update rest or wont refresh TODO  find a solution Maybe fetch user again """

    user['opt_answer_type'] = int(tuple(my_dict['answer_type'])[0])
    user['opt_exercise_nr'] = int(tuple(my_dict['ex_nr'])[0])
    user['opt_retry_nr'] = int(tuple(my_dict['retry_nr'])[0])

    myquery = {'_id': user['_id']}
    arr_key = 'exercise.'+ex_type

    new_values = {"$set": { arr_key: {'opt_enabled': user['opt_enabled'],
                          'opt_can_be_inverted': user['opt_can_be_inverted'],
                          'opt_answer_type': user['opt_answer_type'],
                          'opt_exercise_nr': user['opt_exercise_nr'],
                          'opt_retry_nr': user['opt_retry_nr'],
                          'opt_show_hint': user['opt_show_hint'],
                          'opt_auto_submit': user['opt_auto_submit'],
                          'opt_show_answer': user['opt_show_answer'],
                          "opt_nr": {
                          '0': user['exercise'][ex_type]['opt_nr']['0'] ,
                          '1': user['exercise'][ex_type]['opt_nr']['1'] ,
                          '2': user['exercise'][ex_type]['opt_nr']['2'] ,
                          '3': user['exercise'][ex_type]['opt_nr']['3'] ,
                          '4': user['exercise'][ex_type]['opt_nr']['4'] ,
                          '5': user['exercise'][ex_type]['opt_nr']['5'] ,
                          '6': user['exercise'][ex_type]['opt_nr']['6'] ,
                          '7': user['exercise'][ex_type]['opt_nr']['7'] ,
                          '8': user['exercise'][ex_type]['opt_nr']['8'] ,
                          '9': user['exercise'][ex_type]['opt_nr']['9'] ,
                          '10': user['exercise'][ex_type]['opt_nr']['10'] ,
                          '11': user['exercise'][ex_type]['opt_nr']['11'] ,
                          '12': user['exercise'][ex_type]['opt_nr']['12'] 
                                    }
                          }
                     }
                }

    mongo.db.users.update_one(myquery, new_values)

    return str(new_values)  
    # return str(user) 