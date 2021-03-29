from admin import app,db
from flask import request, session
import flask_admin
from flask_login import login_user
from bson import json_util, ObjectId
import json
from admin.model.mysql import User,JobDetail,JobSector
import datetime

def create_query(selector,page,per_page) :
    if selector == 'smallcompany' :
        return db.session.query(JobDetail).filter_by(big_company=0).paginate(page,per_page=per_page,error_out=True)
    elif selector == 'bigcompany' :
        return db.session.query(JobDetail).filter_by(big_company=1).paginate(page,per_page=per_page,error_out=True)
    else :
        return db.session.query(JobDetail).filter_by(platform=selector).paginate(page,per_page=per_page,error_out=True)

def get_data(selector) :
    page = int(request.args.get('page'))
    if request.args.get('per_page') :
        per_page = int(request.args.get('per_page'))
    else :
        per_page = 20
    
    query = create_query(selector,page,per_page)
    data = query.items

    print(f'LOG: 데이터 길이 {len(data)}')
    print('LOG: 데이터 전송 시간',str(datetime.datetime.now()))
    send_time = str(datetime.datetime.now())
    response_data = {
        'current_page_number': query.page,
        'last_page_number': query.pages,
        'db_name' : 'JobDetail',
        'send_time' : send_time,
        'data_length': len(data),
        'data' : [cl.get_data for cl in data],
    }
    
    return json.dumps(response_data, ensure_ascii=False)

def get_sector() :
    data = db.session.query(JobSector).all()
    print(f'LOG: 데이터 길이 {len(data)}')
    print(str(datetime.datetime.now()))
    send_time = str(datetime.datetime.now())
    response_data = {
        'db_name' : 'JobSector',
        'send_time' : send_time,
        'data_length': len(data),
        'data' : [cl.get_data for cl in data],
    }
    
    return json.dumps(response_data, ensure_ascii=False)