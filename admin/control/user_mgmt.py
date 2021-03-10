from admin import app,db
from flask import request, session
import flask_admin
from flask_login import login_user
from bson import json_util, ObjectId
import json
from werkzeug.security import generate_password_hash, check_password_hash
from admin.model.mysql import User
import datetime

def checkloginpassword():
    email = request.form["email"]
    user = db.session.query(User).filter_by(email=email).first()
    password = request.form["password"]
    if check_password_hash(user.password,password) :
        login_user(user,remember=True, duration=datetime.timedelta(days=30))
        return "correct"
    else:
        return "wrong"
    
def checkemail():
    email = request.form["email"]
    user = db.session.query(User).filter_by(email=email).first()
    if user is not None and email == user.email :
        print('Exist')
        return "Exist"
    elif user is None and '@' in email :
        if email.split('@')[1] != '' :
            print('No User')
            return "No User"
    else:
        print('Not@')
        return "Not@"

def registerUser():
    user = User()
    fields = [k for k in request.form]               
    values = [request.form[k] for k in request.form]
    data = dict(zip(fields, values))
    user_data = json.loads(json_util.dumps(data))
    user_data["password"] = generate_password_hash(user_data["password"])
    user_data["confirmpassword"] = generate_password_hash(user_data["confirmpassword"])

    user.auth = u'Regular'
    user.email = user_data['email']
    user.nickname = user_data['nickname']
    user.password = user_data['password']

    db.session.add(user)
    db.session.commit()
    print("[Notice]User Resister Done")

def registerAdmin():
    if db.session.query(User).filter_by(email='admin@admin').first() is None :
        user = User()

        user.auth = u'admin'
        user.email = 'admin@admin'
        user.nickname = 'admin'
        user.password = generate_password_hash('wdt210309')

        db.session.add(user)
        db.session.commit()
        print('Create Admin account')
    else :
        print('Already Exist Admin account')