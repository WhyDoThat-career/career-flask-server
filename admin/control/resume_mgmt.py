from admin import app,db
from flask import request, session
from bson import ObjectId
import json
from admin.model.mysql import Resume
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
    app.logger.info(json.dumps({'info':f"Register resume {user_info[0]}"}))
    return True

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
    app.logger.info(json.dumps({'info':'Send Resume Data'}))
    return response_data

def update_resume(resume_data) :
    resume_db = ResumeMongo.conn_mongodb('resume')
    resume_in_sql = db.session.query(Resume).filter_by(id=resume_data['id']).first()
    resume_id = resume_in_sql.mongo_key
    if resume_in_sql.main_flag != resume_data['main_flag'] :
        resume_in_sql.main_flag = resume_data['main_flag']
        db.session.commit()
    resume_contents = resume_data['resume'] 
    resume_db.update_one({'_id':ObjectId(resume_id)},resume_contents)
    app.logger.info(json.dumps({'info':f"Update resume (ID : {resume_in_sql.id})"}))
    return True

def delete_resume(resume_in_sql_id) :
    resume_db = ResumeMongo.conn_mongodb('resume')
    resume_in_sql = db.session.query(Resume).filter_by(id=resume_in_sql_id).first()
    resume_id = resume_in_sql.mongo_key
    resume_db.delete_one({'_id':ObjectId(resume_id)})
    db.session.delete(resume_in_sql)
    db.session.commit()
    app.logger.info(json.dumps({'info':f"Delete resume (ID : {resume_in_sql_id})"}))
    return True
