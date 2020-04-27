from flask import Blueprint, render_template, redirect, session, url_for, request
from datetime import datetime, date
from bson.objectid import ObjectId
from database import mongo
import uuid


login_bp = Blueprint('login_bp', __name__,
    template_folder='templates',
    static_folder='static', static_url_path='assets')
    

@login_bp.route('/')
def show_login():
    return render_template('/login/login.html')


""" used from admin to login as user - does not update login date """
@login_bp.route('/admin_as_user/<user_id>/<user_name>')
def login_as_admin(user_id, user_name):
    session["u_id"] = user_id
    return redirect(url_for('exercise_bp.exercise', username=user_name))

@login_bp.route('/_logout_action')
def do_logout():
    session.clear()
    return redirect('/login')
 
@login_bp.route('/_login_action',  methods=["POST"])
def do_login():

    username = request.form.get('user_name').lower()
    session["u_name"] = username

    if (username == 'admin'):
        return redirect(url_for('admin_bp.show_settings'))
    else:
        now = datetime.now()

        if (mongo.db.users.count({'name': username}, limit=1) == 0):
            """ DUPLICATE admin current settings when creating a new user """
            admin_user = mongo.db.users.find_one({"name": "admin"})
            admin_user['_id'] = ObjectId()
            admin_user['name'] = username
            admin_user['add_date'] = now
            admin_user['last_login'] = now
            admin_user['points'] = 0
            insert_id = mongo.db.users.insert_one(admin_user).inserted_id
            session["u_new"] = True
        else:
            user = mongo.db.users.find_one({"name": username})
            user['last_login'] = now

            myquery = {'_id': user['_id']}
            newvalues = {"$set": {'last_login': now}}
            mongo.db.users.update_one(myquery, newvalues)

            insert_id = user['_id']

        session["u_id"] = str(insert_id)
        session["s_id"] = uuid.uuid4() 
        return redirect(url_for('exercise_bp.exercise', username=username))
   