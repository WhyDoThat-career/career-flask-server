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

active_model = api.model('log',{
    'activity':fields.String(required=True,
    description='''
    유저가 특정 행동을 할 경우 유저의 행동 이름을 작성
    행동 이름 및 설명
    - bookmark : 유저가 해당 공고의 북마크 버튼 클릭시
    - click : 유저가 공고를 클릭할때마다 전송
    - filtering : 유저가 검색 또는 필터링 동작을 했을경우
    - recurite_apply : 유저가 공고에서 지원하기 버튼을 눌러 확인한 경우
    - resume_sector : 유저가 개인 이력서에서 직군을 선택한 경우
    - resume_skill : 유저가 개인 이력서에서 기술스택을 선택한 경우
    '''),
    'recurite_id':fields.Integer(required=False,description='공고 ID, 공고 관련 행동일 경우만 전송'),
    'filter_text' : fields.String(required=False,description='검색 또는 필터링 내용, 검색또는 필터링 행동일 경우만 전송'),
    'resume_select':fields.String(required=False,description='직군 또는 스택이름,이력서 관련 행동일 경우만 전송')
})