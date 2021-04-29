from admin import app,db
from flask import request, session
import flask_admin
from flask_login import login_user,current_user
from bson import json_util, ObjectId
import json
from werkzeug.security import generate_password_hash, check_password_hash
from admin.model.mysql import User,JobSector,Resume,Social
from admin.model.mongodb import ResumeMongo
import datetime
from random import randint

def get_user() :
    if not current_user.is_authenticated :
        success = False
        send_data = '알 수 없는 사용자'
    else :
        success = True
        send_data = current_user.get_data
    print(str(datetime.datetime.now()))
    send_time = str(datetime.datetime.now())
    response_data = {
        'db_name' : 'User',
        'send_time' : send_time,
        'is_active' : success,
        'data' : send_data
    }
    app.logger.info(response_data)
    return response_data

def register_social_connection(id,name,user_id) :
    social = Social()
    social.id = id
    social.name = name
    social.user_id = user_id.hex

    db.session.add(social)
    db.session.commit()
    app.logger.info(f"soial_connection {name}")

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
    app.logger.info(f"Register resume {user_info[0]}")

def registerUser(social=False,data=None):
    user = User()
    if social :
        user_data = data
    else :
        user_data = request.get_json()
        user_data["password"] = generate_password_hash(user_data["password"])
        user_data["confirmpassword"] = generate_password_hash(user_data["confirmpassword"])

    user.auth = u'Regular'
    user.email = user_data['email']
    user.nickname = user_data['nickname']
    user.password = user_data['password']

    if user_data['thumbnail'] :
        user.thumbnail = user_data['thumbnail']

    db.session.add(user)
    db.session.flush()

    register_resume(
        user_info = [user.id.hex,user.email,user.nickname],
        main_flag = True)
    
    db.session.commit()
    login_user(user)
    app.logger.info("Resister")
    app.logger.info("Login")

def checkloginpassword():
    email = request.get_json()["email"]
    user = db.session.query(User).filter_by(email=email).first()
    password = request.get_json()["password"]
    if check_password_hash(user.password,password) :
        login_user(user,remember=True, duration=datetime.timedelta(days=30))
        app.logger.info("Login")
        return True
    else:
        return False
    
def checkemail():
    email = request.get_json(force=True)["email"]
    user = db.session.query(User).filter_by(email=email).first()
    if user is not None and email == user.email :
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

def social_login(social_data,platform) :
    connection_check = db.session.query(Social).filter_by(id=social_data['unique_id']).first()
    if connection_check is not None :
        user = db.session.query(User).filter_by(id=connection_check.user_id).first()
        login_user(user)
        app.logger.info("Login")
    
    elif connection_check is None :
        user = db.session.query(User).filter_by(email=social_data['user_email']).first()
        if user is not None :
            login_user(user)
            register_social_connection(social_data['unique_id'],platform,user.id)
            app.logger.info("Login")
        elif user is None :
            user_data = dict()
            user_data['email'] = social_data['user_email']
            user_data['nickname'] = social_data['user_name']
            user_data['password'] = str(randint(100000,999999))
            user_data['thumbnail'] = social_data['thumbnail']
            registerUser(social=True,data=user_data)
            register_social_connection(social_data['unique_id'],platform,current_user.id)