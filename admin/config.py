import json
import pymongo
from elasticsearch import Elasticsearch

def load_key(key_file) :
    with open(key_file) as key_file :
        key = json.load(key_file)
    return key

FLASK_ADMIN_SWATCH = 'journal'

flask_key = load_key(key_file,'./keys/flask_secret.json')
ADMIN_KEY = flask_key['admin_key']
SECRET_KEY = flask_key['secret_key']
GOOGLE_OAUTH = load_key('./keys/google_client_secret.json')
GITHUB_OAUTH = load_key('./keys/github_client_secret.json')

db = load_key(key_file='./keys/aws_sql_key.json')
database = "crawl_job"
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{database}?charset=utf8mb4"
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

mongo = load_key(key_file='./keys/aws_mongo_key.json')
MONGO_CONN = pymongo.MongoClient(f"mongodb://{mongo['host']}:{mongo['port']}",
                                    username=mongo['user'],password=mongo['password'])

JOB_SECTOR = ['Back-end','Front-end','WEB/Full-stack','Android','IOS',
              'Mobile','Data-analyst','Data-engineer','Data-scientist',
              'Machine-learning','DevOps','Game','Embedded/Robotics',
              'Project-manager','Web-publisher','Security','Computer-vision',
              'Block-chain','Hardware','CTO','Unity/AR/VR/3D',
              'JAVA-dev','Anonymous','QA/QC','C#/C++/C','PHP-dev']

es = load_key(key_file='./keys/aws_elastic_key.json')
ELASTIC = Elasticsearch(f"http://{es['host']}:{es['port']}")