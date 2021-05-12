import os , boto3
import logging
from flask import Flask,Blueprint
from flask import request, session,make_response,jsonify
from flask import send_from_directory,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import Babel
from flask_cors import CORS
from flask_login import LoginManager,current_user
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from oauthlib.oauth2 import WebApplicationClient
from flask_restx import Api
from flask_ipban import IpBan
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__, static_folder='../build/static',template_folder='./views/templates')
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
babel = Babel(app)
blueprint = Blueprint('api',__name__,url_prefix='/api')
api = Api(blueprint,doc='/doc/',title = 'WhyDoThat API 문서',description = '모든 API 호출은 /api/~ 로 시작합니다.')
app.register_blueprint(blueprint)
ip_ban = IpBan(ban_seconds=200)
ip_ban.init_app(app)
ip_ban.load_nuisances()
ip_ban.ip_whitelist_add('1.223.233.222')
ip_ban.url_pattern_add('/.env',match_type='string')
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

@app.route('/')
@app.route('/index',methods=["GET","POST"])
def index() :
    if request.method == "GET" :
        if not current_user.is_authenticated :
            return send_from_directory('../build','index.html')
        else :
            if current_user.is_admin :
                return redirect('/admin')
            else :
                return send_from_directory('../build','index.html')

import admin.views.admin_view
import admin.views.loginAPI
import admin.views.dataAPI
import admin.views.google_login
import admin.views.github_login
import admin.views.restAPI_orgin
import admin.set_log