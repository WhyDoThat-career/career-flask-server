from flask import Flask, request, session,make_response,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import Babel
from flask_cors import CORS
from flask_login import LoginManager

app = Flask(__name__, static_folder='./build/static',template_folder='./views/templates')
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
CORS(app)

# Initialize babel
babel = Babel(app)

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

import admin.views.admin_view
import admin.views.restAPI
