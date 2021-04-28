from admin import api
from flask_restx import fields

checkemail_model = api.model('checkemail',{
    'email':fields.String(required=True,description = '이메일')
    })

login_model = api.model('login',{
    'email':fields.String(required=True,description = '이메일'),
    'password':fields.String(required=True,description = '비밀번호')
    })

register_model = api.model('register',{
    'email':fields.String(required=True,description = '이메일'),
    'nickname':fields.String(required=True,description = '닉네임'),
    'password':fields.String(required=True,description = '비밀번호'),
    'confirmpassword':fields.String(required=True,description = '비밀번호 확인')
    })