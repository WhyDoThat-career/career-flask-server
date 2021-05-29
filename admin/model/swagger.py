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
    - recruit_apply : 유저가 공고에서 지원하기 버튼을 눌러 확인한 경우
    - resume_sector : 유저가 개인 이력서에서 직군을 선택한 경우
    - resume_skill : 유저가 개인 이력서에서 기술스택을 선택한 경우
    '''),
    'recruit_id':fields.Integer(required=False,description='공고 ID, 공고 관련 행동일 경우만 전송'),
    'filter_text' : fields.String(required=False,description='검색 또는 필터링 내용, 검색또는 필터링 행동일 경우만 전송'),
    'resume_select':fields.String(required=False,description='직군 또는 스택이름,이력서 관련 행동일 경우만 전송')
})

resume_career_model = api.model('career_model',{
            'company' : fields.String(required=False,description='회사명'),
            'term' : fields.String(required=False,description='기간')
        })
resume_project_model = api.model('project_model',{
            'title' : fields.String(required=False,description='프로젝트명'),
            'term' : fields.String(required=False,description='기간'),
            'role' : fields.String(required=False,description='참여 역할'),
            'belong' : fields.String(required=False,description='개인 or 회사명 표기')
        })
resume_education_model = api.model('education_model',{
            'title' : fields.String(required=False,description='교육명'),
            'term' : fields.String(required=False,description='기간'),
            'academy' : fields.String(required=False,description='교육기관명')
        })
resume_foreign_model = api.model('foreign_model',{
            'contents' : fields.String(required=False,description='어학 취득 내용'),
        })
resume_award_model = api.model('award_model',{
            'title' : fields.String(required=False,description='수상명'),
            'term' : fields.String(required=False,description='수상 날짜'),
            'academy' : fields.String(required=False,description='기관명')
        })

resume_article_model = api.model('article_model',{
            'title' : fields.String(required=False,description='출판/논문/특허 이름'),
            'address' : fields.String(required=False,description='게시된 자료 웹 주소'),
        })

resume_model = api.model('resume_model',{
        'title': fields.String(required=False,description='이력서 제목'),
        'email' : fields.String(required=False,description='이메일'),
        'phone' : fields.String(required=False,description='휴대폰 번호'),
        'github' : fields.String(required=False,description='Gihub 프로필 링크'),
        'personal_page' : fields.String(required=False,description='개인 블로그 및 웹사이트'),
        'introduce' : fields.String(required=False,description='간단한 소개 (40자 이내)'),
        'sector' : fields.String(required=False,description='지원하는 기술 직군'),
        'skill_stack': fields.List(fields.String,description='기술 스택 리스트'),
        'devops' : fields.List(fields.String,description='사용가능한 DevOps 리스트'),
        'career' : fields.List(fields.Nested(resume_career_model),required=False,description='경력'),
        'project' : fields.List(fields.Nested(resume_project_model),required=False,description='프로젝트'),
        'education' : fields.List(fields.Nested(resume_education_model),required=False,description='교육'),
        'last_education' : fields.String(required=False,description='최종학력'),
        'military' : fields.String(required=False,description='군필,미필,면제 선택'),
        'foreign' : fields.List(fields.Nested(resume_foreign_model),required=False,description='외국어'),
        'award' : fields.List(fields.Nested(resume_award_model),required=False,description='수상 경력'),
        'article' : fields.List(fields.Nested(resume_article_model),required=False,description='출판/논문/특허')
        })

resume_update_model = api.model('resume_update',{
    'id' : fields.Integer(required=True,description='이력서의 아이디 값(mongo_key가 아닌 id 필드)'),
    'main_flag' : fields.Boolean(required=False,description='대표 이력서 설정'),
    'resume' : fields.Nested(resume_model,required=True,description='수정된 이력서 정보가 들어갈 필드')
})

resume_delete_model = api.model('resume_delete',{
    'id' : fields.Integer(required=True,description='이력서의 아이디 값(mongo_key가 아닌 id 필드)')
})