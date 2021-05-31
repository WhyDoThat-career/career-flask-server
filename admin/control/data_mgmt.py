from admin import app,db
from flask import request, session
import flask_admin
from flask_login import login_user
import json
from admin.model.mysql import User,JobDetail,JobSector,CompanyInfo,Resume,JobSkill
from admin.model.mongodb import ResumeMongo
import datetime

def create_query(selector,page,per_page) :
    if selector == 'smallcompany' :
        return (db.session.query(JobDetail)
                    .filter_by(big_company=0)
                    .order_by(JobDetail.crawl_date.desc())
                    .paginate(page,per_page=per_page,error_out=True))
    elif selector == 'bigcompany' :
        return (db.session.query(JobDetail)
                    .filter_by(big_company=1)
                    .order_by(JobDetail.crawl_date.desc())
                    .paginate(page,per_page=per_page,error_out=True))
    elif selector in ['wanted','roketpunch','programmers','naver','kakao'] :
        return (db.session.query(JobDetail)
                    .filter_by(platform=selector)
                    .order_by(JobDetail.crawl_date.desc())
                    .paginate(page,per_page=per_page,error_out=True))
    else :
        return (db.session.query(JobDetail)
                    .filter_by(sector=selector)
                    .order_by(JobDetail.crawl_date.desc())
                    .paginate(page,per_page=per_page,error_out=True))

def get_data(selector) :
    if request.args.get('page') :
        page = int(request.args.get('page'))
    else :
        page = 1
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
    json.dumps({'info':f'Send Data list From {selector}'})
    return response_data

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
    app.logger.info(json.dumps({'info':'Send Sector list'}))
    return response_data

def get_skills() :
    data = db.session.query(JobSkill).all()
    print(f'LOG: 데이터 길이 {len(data)}')
    print(str(datetime.datetime.now()))
    send_time = str(datetime.datetime.now())
    response_data = {
        'db_name' : 'JobSkill',
        'send_time' : send_time,
        'data_length': len(data),
        'data' : [cl.get_data for cl in data],
    }
    app.logger.info(json.dumps({'info':'Send Skill list'}))
    return response_data

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
    app.logger.info(json.dumps({'info':'Send Company Data'}))
    return response_data

def search_recommend_data(recommend_list) :
    data = db.session.query(JobDetail).filter(JobDetail.id.in_(recommend_list)).all()
    data_dict = [cl.get_data for cl in data]
    print(str(datetime.datetime.now()))
    send_time = str(datetime.datetime.now())

    response_data = {
        'db_name' : 'JobDetail',
        'send_time' : send_time,
        'data_length': len(data),
        'data' : data_dict,
    }
    app.logger.info(json.dumps({'info':'Send Recommand list'}))
    return response_data
