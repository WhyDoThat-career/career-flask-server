from admin import app
from flask import request
import datetime

def pagination(page,per_page):
    if page == 0 :
        return 0
    else :
        return page*per_page+1

def make_query(domain,term,sort,page,per_page) :
    if domain != 'all' and domain is not None :
        #string_query = f'{domain}:{term}'
        bool_query = {'must':{'match':{domain:term}}}
    else :
        #string_query = f'title:{term} OR main_text:{term} OR skill_tag:{term}'
        bool_query = {'should':[{'match':{'title':term}},
                                {'match':{'main_text':term}},
                                {'match':{'skill_tag':term}}],
                      'minimum_should_match':1}
    if sort == '정확도순' :
        sort_query = ['_score',{'crawl_date':{'order':'desc'}}]
    else : 
        sort_query = [{'crawl_date':{'order':'desc'}},'_score']
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
    Elastic = app.config['ELASTIC']

    Elastic.indices.refresh(index='mysql-jobdetail*')
    domain = request.args.get('domain')
    term = request.args.get('term')
    sort = request.args.get('sort')
    if request.args.get('page') :
        page = int(request.args.get('page'))
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
    response_data = {
        'current_page_number': page+1,
        'last_page_number': last_page+1,
        'db_name' : 'JobDetail',
        'send_time' : send_time,
        'data_length': per_page,
        'data' : [hits['_source'] for hits in search_result['hits']['hits']],
    } 
    return response_data