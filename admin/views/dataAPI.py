from admin import app, api
from flask import request, redirect, url_for, session,abort
from admin.control import user_mgmt,data_mgmt
from flask_login import current_user
from flask_restx import Namespace,Resource
import json
from admin.model.swagger import active_model

UserFunc = Namespace('User Data',description='유저 관련 데이터 API')
DataFunc = Namespace('Job Data',description='공고 및 기업 관련 데이터 API')
ActiveFunc = Namespace('Active log',description='유저 활동 log 저장을 위한 API')

@UserFunc.route('')
class UserData(Resource) :
    def get(self) :
        '''현재 로그인중인 유저 정보 API'''
        return user_mgmt.get_user()
@UserFunc.route('/resume')
class UserResume(Resource) :
    def get(self) :
        '''현재 로그인중인 유저의 이력서목록 API'''
        if current_user.is_active :
            user_id = current_user.get_id().hex
            return data_mgmt.get_resume(user_id)
        else :
            return abort(404)
api.add_namespace(UserFunc,'/getuser')

@DataFunc.route('/<selector>')
class GetData(Resource) :
    @DataFunc.doc(params={
        'selector': '→플랫폼이름 (ex. wanted,naver)\n→회사 규모 (ex. smallcompany, bigcompany)',
        'page' : '페이지 요청 (ex. ?page=3), default=1',
        'per_page' : '데이터 표시개수 요청 (ex. ?per_page=40), default=20'
        })
    def get(self, selector) :
        '''페이지에 표시되는 데이터 API'''
        return data_mgmt.get_data(selector)
@DataFunc.route('/company/<company_name>')
class GetCompany(Resource) :
    @DataFunc.doc(params={'company_name': '기업 이름'})
    def get(self, company_name) :
        '''기업이름을 통해 JobPlanet 정보 검색 API'''
        return data_mgmt.get_company_data(company_name)
@DataFunc.route('/sector')
class GetSector(Resource) :
    def get(self) :
        '''직군 목록 API'''
        return data_mgmt.get_sector()
@DataFunc.route('/skills')
class GetSkills(Resource) :
    def get(self) :
        '''자주언급 되는 상위 300개 기술스택 API'''
        return data_mgmt.get_skills()
api.add_namespace(DataFunc,'/getdata')

@ActiveFunc.route('')
class GetActiveLog(Resource) :
    @ActiveFunc.expect(active_model)
    def post(self) :
        '''특정 활동의 로그를 보고하는 API 입니다.'''
        log_data = request.get_json()
        app.logger.info(json.dumps(log_data))
        return 200,'Data saved'
api.add_namespace(ActiveFunc,'/active_log')