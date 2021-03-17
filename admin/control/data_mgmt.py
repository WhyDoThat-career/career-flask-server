from admin import app,db
from flask import request, session
import flask_admin
from flask_login import login_user
from bson import json_util, ObjectId
import json
from admin.model.mysql import User,JobDetail
import datetime

def get_data() :
    data = db.session.query(JobDetail).all()
    print(f'LOG: 데이터 길이 {len(data)}')
    print([cl.get_data for cl in data])
    print(str(datetime.datetime.now()))
    send_time = str(datetime.datetime.now())
    response_data = {
        'data' : [cl.get_data for cl in data],
        'db_name' : 'Job_Detail',
        'send_time' : send_time,
    }
    
    return json.dumps(response_data)