from admin import app, db
from flask import request
from admin.model.mysql import JobSkill,JobDetail
import datetime
Elastic = app.config['ELASTIC']

def pagination(page,per_page):
    if page == 0 :
        return 0
    else :
        return page*per_page+1

def make_query(domain,term,sort,page,per_page) :
    # To Do : 토크나이저 setting 또는 ngram 이용해서 검색 쿼리 개선 필요
    term = term.replace(' ','*')
    if domain != 'all' and domain is not None :
        #string_query = f'{domain}:{term}'
        bool_query = {'must':{'wildcard':{domain:f'*{term}*'}}}
    else :
        #string_query = f'title:{term} OR main_text:{term} OR skill_tag:{term}'
        bool_query = {'should':[{'wildcard':{'title':f'*{term}*'}},
                                {'wildcard':{'main_text':f'*{term}*'}},
                                {'wildcard':{'skill_tag':f'*{term}*'}},
                                {'wildcard':{'company_name':f'*{term}*'}}],
                      'minimum_should_match':1}
    if sort == '최신순' :
        sort_query = [{'crawl_date':{'order':'desc'}}]
    else : 
        sort_query = ['_score',{'crawl_date':{'order':'desc'}}]
    es_query = {
            'from':pagination(page,per_page),
            'size':per_page,
            'query':{
                'bool' : bool_query
            },
            'sort' :sort_query
        }
    return es_query

def get_search_result():
    Elastic.indices.refresh(index='mysql-jobdetail*')
    domain = request.args.get('domain')
    term = request.args.get('term')
    sort = request.args.get('sort')
    if request.args.get('page') :
        page = int(request.args.get('page'))-1
    else :
        page = 0
    if request.args.get('per_page') :
        per_page = int(request.args.get('per_page'))
    else :
        per_page = 20
    es_query = make_query(domain,term,sort,page,per_page)
    search_result = Elastic.search(body=es_query,
                                   index='mysql-jobdetail*')
    last_page = int(search_result['hits']['total']['value']/per_page)
    send_time = str(datetime.datetime.now())
    send_data = [hits['_source'] for hits in search_result['hits']['hits'] if db.session.query(JobDetail).filter_by(id=hits['_source']['id']).first() is not None]

    for index,item in enumerate(send_data) :
        if item['skill_tag'] is not None :
            send_data[index]['skill_tag'] = item['skill_tag'].split(',')

    response_data = {
        'current_page_number': page+1,
        'last_page_number': last_page+1,
        'db_name' : 'JobDetail',
        'send_time' : send_time,
        'data_length': len(send_data),
        'data' : send_data,
    } 
    return response_data

def get_autotyping() :
    term = request.args.get('term')
    send_time = str(datetime.datetime.now())
    company_name = db.session.query(JobDetail).filter(JobDetail.company_name.like(f'{term}%')).all()
    if company_name == [] :
        company_name = db.session.query(JobDetail).filter(JobDetail.company_name.like(f'%{term}%')).all()
    skill_tag = db.session.query(JobSkill).filter(JobSkill.name.like(f'%{term}%')).all()

    send_company_data = list(set([c.company_name for c in company_name]))
    send_skill_tag_data = list(set([s.name for s in skill_tag]))
    send_company_data.sort(key=lambda i:len(i))
    send_skill_tag_data.sort(key=lambda i:len(i))

    response_data = {
        'db_name' : 'JobDetail',
        'send_time' : send_time,
        'company_result' : send_company_data[:3],
        'skill_result' : send_skill_tag_data[:3]
    } 
    return response_data