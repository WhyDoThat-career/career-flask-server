from admin import app, api
from flask import request, redirect, url_for, session
from admin.control import user_mgmt
from flask_login import logout_user
from flask_restx import Namespace,Resource
from admin.model.swagger import checkemail_model,login_model,register_model
import json

LoginFunc = Namespace('Login',description='로그인을 위한 API')
CheckFunc = Namespace('Check',description='이메일, 비밀번호 체크 API')
OtherFunc = Namespace('Other',description='로그아웃,회원가입,비밀번호 찾기 API')

@LoginFunc.route('')
class Login(Resource) :
    @LoginFunc.expect(login_model)
    def post(self) :
        '''Form으로 부터 데이터를 받아 로그인 세션을 생성'''
        return user_mgmt.checkloginpassword()
api.add_namespace(LoginFunc,'/login')

@CheckFunc.route('/email')
class CheckEmail(Resource) :
    @CheckFunc.expect(checkemail_model)
    def post(self) :
        '''이메일 중복검사, 존재여부 검사 API'''
        return user_mgmt.checkemail()
@CheckFunc.route('/password')
class CheckPassword(Resource) :
    @CheckFunc.expect(login_model)
    def post(self) :
        '''패스워드 체크 API (\'/login\' POST와 같은 동작)'''
        return user_mgmt.checkloginpassword()
api.add_namespace(CheckFunc,'/check')

RegisterFunc = Namespace('Other')
@RegisterFunc.route('')
class Register(Resource) :
    @RegisterFunc.expect(register_model)
    def post(self) :
        '''회원가입 동작을 한 후 로그인까지 진행됩니다.'''
        user_mgmt.registerUser()
        return redirect(url_for('index'))
api.add_namespace(RegisterFunc,'/register')

LogoutFunc = Namespace('Other')
@LogoutFunc.route('')
class Logout(Resource) :
    def get(self) :
        '''로그아웃 API'''
        app.logger.info(json.dumps({'info':'Logout'}))
        logout_user()
        return redirect(url_for('index'))
api.add_namespace(LogoutFunc,'/logout')

ForgotPasswordFunc = Namespace('Other')
@ForgotPasswordFunc.route('')
class FortgotPassword(Resource) :
    @ForgotPasswordFunc.expect(checkemail_model)
    def post(self) :
        '''Email로 비밀번호 변경 페이지를 전송'''
        return '구현안함'
api.add_namespace(ForgotPasswordFunc,'/forgot-password')