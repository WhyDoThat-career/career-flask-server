from admin import app,db
from flask import request, session
import flask_admin
from flask_login import login_user
from bson import json_util, ObjectId
import json
from werkzeug.security import generate_password_hash, check_password_hash
from admin.model.mysql import User,JobSector,Resume
from admin.model.mongodb import ResumeMongo
import datetime

def register_mongo_resume(user_info,resume_data) :
    resume_db = ResumeMongo.conn_mongodb('resume')
    result = resume_db.insert_one({
        'user_id' : user_info[0],
        'user_email' : user_info[1],
        'user_nickname' : user_info[2],
        'resume' : resume_data
    }).inserted_id
    return str(result)

def register_resume(user_info,main_flag,resume_data={'title':'제목 없음'}) :
    resume = Resume()
    resume.main_flag = main_flag
    resume.mongo_key = register_mongo_resume(user_info,resume_data)
    resume.user_id = user_info[0]

    db.session.add(resume)
    db.session.commit()
    print("[Notice]Resume Resister Done")

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
    db.session.flush()

    register_resume(
        user_info = [user.id.hex,user.email,user.nickname],
        main_flag = True)
    
    db.session.commit()
    print("[Notice]User Resister Done")

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

def registerAdmin():
    if db.session.query(User).filter_by(email='admin@admin').first() is None :
        user = User()

        user.auth = u'admin'
        user.email = 'admin@admin'
        user.nickname = 'admin'
        user.password = generate_password_hash('wdt210309')

        db.session.add(user)

        if db.session.query(JobSector).all() is None :
            for sector_name in app.config['JOB_SECTOR'] :
                sector = JobSector()
                sector.name = sector_name
                db.session.add(sector)
            
        db.session.commit()
        print('Create Admin account')
        return ""
    else :
        print('Already Exist Admin account')
        return ""