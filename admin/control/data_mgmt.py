from admin import app,db
from flask import request, session
import flask_admin
from flask_login import login_user
from bson import json_util, ObjectId
import json
from admin.model.mysql import User,JobDetail,JobSector
import datetime

def get_data_small_company() :
    data = db.session.query(JobDetail).filter_by(big_company=0).all()
    print(f'LOG: 데이터 길이 {len(data)}')
    print([cl.get_data for cl in data])
    print(str(datetime.datetime.now()))
    send_time = str(datetime.datetime.now())
    response_data = {
        'data' : [cl.get_data for cl in data],
        'db_name' : 'JobDetail',
        'send_time' : send_time,
    }
    
    return json.dumps(response_data, ensure_ascii=False)

def get_data_big_company() :
    data = db.session.query(JobDetail).filter_by(big_company=1).all()
    print(f'LOG: 데이터 길이 {len(data)}')
    print([cl.get_data for cl in data])
    print(str(datetime.datetime.now()))
    send_time = str(datetime.datetime.now())
    response_data = {
        'data' : [cl.get_data for cl in data],
        'db_name' : 'JobDetail',
        'send_time' : send_time,
    }
    
    return json.dumps(response_data, ensure_ascii=False)

def get_data_sector() :
    data = db.session.query(JobSector).all()
    print(f'LOG: 데이터 길이 {len(data)}')
    print([cl.get_data for cl in data])
    print(str(datetime.datetime.now()))
    send_time = str(datetime.datetime.now())
    response_data = {
        'data' : [cl.get_data for cl in data],
        'db_name' : 'JobSector',
        'send_time' : send_time,
    }
    
    return json.dumps(response_data, ensure_ascii=False)