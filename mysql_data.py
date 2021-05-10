from elasticsearch import Elasticsearch
import json
from datetime import datetime
import pymysql
import json
from pymysql.cursors import DictCursor

def arr2str(array) :
    if array is not None :
        return ','.join(array)
    else :
        return None
class MySQL :
    def __init__(self,key_file,database) :
        KEY = self.load_key(key_file)
        self.MYSQL_HOST = KEY['host']
        self.MYSQL_CONN = pymysql.connect(
                                host = self.MYSQL_HOST,
                                user=KEY['user'],
                                passwd=KEY['password'],
                                db=database,
                                charset='utf8mb4')

    def create_sql_item(self,item,dtype) :
        if dtype == 'string' or 'datetime':
            return "'{}'".format(item)
        elif dtype == 'bool' or 'int':
            return "{}".format(item)
    def dict_list2string(self,items,dtype_map) :
        key_arr = []
        item_arr = []
        for key, item in items.items() :
            if item != None :
                key_arr.append(key)
                item_arr.append(self.create_sql_item(item,dtype=dtype_map[key]))
        return arr2str(key_arr),arr2str(item_arr)
    
    def load_key(self,key_file) :
        with open(key_file) as key_file :
            key = json.load(key_file)
        return key
    def conn_mysqldb(self) :
        if not self.MYSQL_CONN.open :
            self.MYSQL_CONN.ping(reconnect=True)
        return self.MYSQL_CONN
    
    def conn_data_center(self) :
        if not self.data_center.open :
            self.data_center.ping(reconnect=True)
        return self.data_center
    
    def insert_data(self,table,items,dtype_map) :
        skey,sdata = self.dict_list2string(items,dtype_map)
        db = self.conn_mysqldb()
        db_cursor = db.cursor()
        sql_query = f"INSERT INTO {table} ({skey}) VALUES ({sdata})"
        db_cursor.execute(sql_query)
        db.commit()
        

def load_key(key_file) :
    with open(key_file) as key_file :
        key = json.load(key_file)
    return key

def pagination(page,per_page):
    if page == 0 :
        return 0
    else :
        return page*per_page+1

def make_query(page,per_page) :
    sort_query = [{'crawl_date':{'order':'asc'}},'_score']
    es_query = {
            'from':pagination(page,per_page),
            'size':per_page,
            'query':{
                'match_all':{}
            },
            'sort' :sort_query
        }
    return es_query


es = load_key(key_file='./keys/aws_elastic_key.json')
Elastic = Elasticsearch(f"http://{es['host']}:{es['port']}")

Elastic.indices.refresh(index='mysql-jobdetail*')

es_query = make_query(0,5000)
search_result = Elastic.search(body=es_query,
                                   index='mysql-jobdetail*')
tmp = []
for hits in search_result['hits']['hits'] :
    data = hits['_source']
    del data['@timestamp']
    del data['@version']
    data['crawl_date'] = data['crawl_date'].split('.')[0].replace('T',' ')
    if data['deadline'] != None:
        data['deadline'] = data['crawl_date'].split('T')[0]
    if data['newbie'] :
        data['newbie'] = 1
    else :
        data['newbie'] = 0
    if data['big_company'] :
        data['big_company'] = 1
    else :
        data['big_company'] = 0
    tmp.append(data)

dtype_map = {
    "id" : "int",
    "title" : "string",
    "href" : "string",
    "main_text" : "string",
    "salary" : "string",    
    "skill_tag" : "string",
    "sector" : "string",
    "newbie" : "bool",
    "career" : "string",
    "deadline" : "datetime",
    "company_name" : "string",
    "company_address" : "string",
    "platform" : "string",
    "logo_image" : "string",
    "crawl_date" : "string",
    "big_company" : "bool"
}

sql_db = MySQL(key_file='./keys/aws_sql_key.json',database='crawl_job')

for input_data in tmp :
    sql_db.insert_data('job_detail',input_data,dtype_map)