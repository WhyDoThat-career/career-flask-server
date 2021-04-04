from admin import app,db
from flask import request, session
import flask_admin
from flask_login import login_user
from bson import ObjectId
import json
from admin.model.mysql import User,JobDetail,JobSector,CompanyInfo,Resume
from admin.model.mongodb import ResumeMongo
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

def get_company_data(company_name) :
    data = db.session.query(CompanyInfo).filter_by(name=company_name).first()
    if data is None :
        success = False
        send_data = '잡플래닛에서 검색할 수 없는 기업명 입니다.'
    else :
        success = True
        send_data = data.get_data
    print(str(datetime.datetime.now()))
    send_time = str(datetime.datetime.now())
    response_data = {
        'db_name' : 'CompanyInfo',
        'send_time' : send_time,
        'success' : success,
        'data' : send_data
    }
    return json.dumps(response_data, ensure_ascii=False)

def get_resume(user_id) :
    data = db.session.query(Resume).filter_by(user_id=user_id).all()
    data_dict = [cl.get_data for cl in data]
    print(str(datetime.datetime.now()))
    send_time = str(datetime.datetime.now())
    for index,item in enumerate(data) :
        resume_db = ResumeMongo.conn_mongodb('resume')
        result = resume_db.find_one({"_id":ObjectId(item.mongo_key)})
        data_dict[index]['resume'] = result['resume']

    response_data = {
        'db_name' : 'Resume',
        'send_time' : send_time,
        'data_length': len(data),
        'data' : data_dict,
    }
    return json.dumps(response_data, ensure_ascii=False)