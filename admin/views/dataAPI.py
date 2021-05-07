from admin import app, api
from flask import request, redirect, url_for, session,abort
from admin.control import user_mgmt,data_mgmt,search_mgmt
from flask_login import current_user
from flask_restx import Namespace,Resource,fields
import json
from admin.model.swagger import active_model

UserFunc = Namespace('User Data',description='유저 관련 데이터 API')
DataFunc = Namespace('Job Data',description='공고 및 기업 관련 데이터 베이스 접근 API')
SearchFunc = Namespace('Search Data',description='elasticsearch에 보내는 검색 API')
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

@SearchFunc.route('')
class Search(Resource) :
    @SearchFunc.doc(params={
        'term' :{'required':'true','type':'string',
                    'description':'검색 내용 쿼리 (ex.?term=프론트엔드'},
        'domain' : {'type':'string',
                    'description':'검색 도메인 쿼리 defaualt=all(전체검색)\n- all\n- skill_tag : 스택으로만 검색\n - company_name : 기업명으로만 검색\n(ex. ?term=자바&domain=skill_tag)'},
        'sort' :{'type':'string',
                    'description':'정렬 선택 default=최신순\n- 최신순\n- 정확도순\n- 추천순(개발중)'},
        'page' : {'type':'integer',
                    'description':'페이지 요청 (ex. ?page=3), default=1'},
        'per_page' : {'type':'integer',
                    'description':'데이터 표시개수 요청 (ex. ?per_page=40), default=20'}
        })
    def get(self) :
        '''검색창에서 보낼 쿼리'''
        return search_mgmt.get_search_result()
api.add_namespace(SearchFunc,'/search')

@DataFunc.route('/<selector>')
class GetData(Resource) :
    @DataFunc.doc(params={
        'selector': '가져올 데이터 영역 선택\n- 플랫폼이름 (ex. wanted,naver)\n- 회사 규모 (ex. smallcompany, bigcompany)',
        'page' : {'type':'integer',
                    'description':'페이지 요청 (ex. ?page=3), default=1'},
        'per_page' : {'type':'integer',
                    'description':'데이터 표시개수 요청 (ex. ?per_page=40), default=20'}
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
        active_data = request.get_json()
        active_data['user_id'] = current_user.id.hex

        if (active_data['activity'] in ['resume_sector','resume_skill']
                and 'resume_select' not in active_data) :
            app.logger.error(json.dumps(active_data))
            return 'Resume related data must have \"resume_select\" column', 400

        elif (active_data['activity'] == 'filtering'
                and 'filter_text' not in active_data) :
            app.logger.error(json.dumps(active_data))
            return 'Filtering data must have \"filter_text\" column', 400
        
        elif (active_data['activity'] in ['bookmark','click','recruit_apply']
                and 'recruit_id' not in active_data) :
            app.logger.error(json.dumps(active_data))
            return 'Recruit related data must have \"recruit_id\" column', 400

        else :
            app.logger.info(json.dumps(active_data))
            return 'Data transfer success',200
api.add_namespace(ActiveFunc,'/active_log')