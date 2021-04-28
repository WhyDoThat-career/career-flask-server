from flask import Flask, request, session,make_response,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import Babel
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from oauthlib.oauth2 import WebApplicationClient
import os , boto3
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

print(os.getcwd())
print(os.listdir())
app = Flask(__name__, static_folder='../build/static',template_folder='./views/templates')
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
babel = Babel(app)
CORS(app,resources={
    r'*':{'origins':'*',
          'methods' : '*',
          'allow-headers':'*',
          'supports_credentials':True
          }
    })

google_oauth = app.config['GOOGLE_OAUTH']
google_client = WebApplicationClient(google_oauth['client_id'])
google_discovery_uri = "https://accounts.google.com/.well-known/openid-configuration"

github_oauth = app.config['GITHUB_OAUTH']
github_client = WebApplicationClient(github_oauth['client_id'])

from admin.model.mysql import User

def init_login():
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.session_protection='strong'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)
    
    @login_manager.unauthorized_handler
    def unauthorized() :
        return make_response(jsonify(success=False),401)

    @app.before_request
    def app_before_request() :
        if 'client_id' not in session:
            session['client_id'] = request.environ.get('HTTP_X_REAL_IP',request.remote_addr)

@babel.localeselector
def get_locale():
    override = request.args.get('lang')

    if override:
        session['lang'] = override

    return session.get('lang', 'ko')

init_login()
def downloadDirectoryFroms3(bucketName,remoteDirectoryName):
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucketName) 
    for object in bucket.objects.filter(Prefix = remoteDirectoryName):
        if not os.path.exists(os.path.dirname(object.key)):
            os.makedirs(os.path.dirname(object.key))
        bucket.download_file(object.key,object.key)

downloadDirectoryFroms3('career-client','build')

import admin.views.admin_view
import admin.views.restAPI
import admin.views.google_login
import admin.views.github_login
