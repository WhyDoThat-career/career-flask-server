from admin import db
import uuid
from sqlalchemy_utils import EmailType, UUIDType, URLType, IPAddressType

USER_AUTH = [
    (u'admin', u'Admin'),
    (u'reqular', u'Regular'),
]

class Resume(db.Model) :
    id     = db.Column(db.Integer, primary_key=True)
    main_flag = db.Column(db.Boolean, nullable=False)
    mongo_key = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey('user.id'))

    @property
    def get_data(self):
        dictionary = self.__dict__
        try :
            del dictionary['_sa_instance_state']
            dictionary['user_id'] = self.user_id.hex
        except :
            pass
        return dictionary

class Social(db.Model) :
    id = db.Column(db.String(128), primary_key=True)
    name = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.String(32), db.ForeignKey('user.id'))

class User(db.Model) :
    id          = db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    password    = db.Column(db.String(128))
    auth           = db.Column(db.String(100))
    email          = db.Column(EmailType, unique=True, nullable=False)
    nickname       = db.Column(db.String(100), nullable=False)
    thumbnail      = db.Column(URLType, default = '/static/img/wdticon.png')
    resume    = db.relationship('Resume')

    @property
    def is_authenticated(self):
        return True
    @property
    def is_admin(self) :
        if self.auth == u'admin' :
            return True
        else :
            return False
    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username

class JobDetail(db.Model) :
    id     = db.Column(db.Integer, primary_key=True)
    title     = db.Column(db.String(500))
    href      = db.Column(URLType)
    main_text = db.Column(db.Text)
    salary    = db.Column(db.String(50))
    skill_tag = db.Column(db.String(500))
    sector    = db.Column(db.String(200))
    newbie    = db.Column(db.Boolean)
    career    = db.Column(db.String(50))
    deadline  = db.Column(db.Date)
    company_name    = db.Column(db.String(100))
    company_address = db.Column(db.String(500))
    logo_image      = db.Column(db.String(500))
    big_company    = db.Column(db.Boolean)
    platform        = db.Column(db.String(100))
    crawl_date      = db.Column(db.DateTime)
    
    @property
    def get_data(self):
        dictionary = self.__dict__
        try :
            del dictionary['_sa_instance_state']
            if dictionary['deadline'] != None :
                dictionary['deadline'] = str(dictionary['deadline'])
            dictionary['crawl_date'] = str(dictionary['crawl_date'])
            dictionary['skill_tag'] = dictionary['skill_tag'].split(',')
        except :
            pass
        return dictionary

skills_sector_table = db.Table('skill_sector',db.Model.metadata,
                            db.Column('job_skill_id', db.Integer, db.ForeignKey('jobskill.id')),
                            db.Column('job_sector_id', db.Integer, db.ForeignKey('jobsector.id'))
                        )

class JobSkill(db.Model) :
    __tablename__ = "jobskill"
    id  = db.Column(db.Integer, primary_key=True)
    name   = db.Column(db.String(200))
    sector = db.relationship('JobSector',secondary=skills_sector_table)

    def __str__(self):
        return "{}".format(self.name)
    @property
    def get_data(self):
        dictionary = self.__dict__
        try :
            del dictionary['_sa_instance_state']
        except :
            pass
        return dictionary

class JobSector(db.Model) :
    __tablename__ = "jobsector"
    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(200))
    skills = db.relationship('JobSkill',secondary=skills_sector_table)

    def __str__(self):
        return "{}".format(self.name)
    @property
    def get_data(self):
        dictionary = self.__dict__
        try :
            del dictionary['_sa_instance_state']
        except :
            pass
        return dictionary

class CompanyInfo(db.Model) :
    __tablename__ = "company_info"
    id = db.Column(db.Integer, primary_key=True)
    crawl_date  = db.Column(db.DateTime)
    name        = db.Column(db.String(200))
    sector      = db.Column(db.String(200))
    scale       = db.Column(db.String(200))
    employees   = db.Column(db.String(100))
    establishment_date = db.Column(db.Date)
    review_count = db.Column(db.Integer)
    star_point  = db.Column(db.Float)
    salary_count = db.Column(db.Integer)
    salary_average = db.Column(db.Integer)
    interview_count = db.Column(db.Integer)
    interview_level = db.Column(db.String(100))
    interview_feel = db.Column(db.String(100))

    def __str__(self):
        return "{}".format(self.name)
    @property
    def get_data(self):
        dictionary = self.__dict__
        try :
            del dictionary['_sa_instance_state']
            dictionary['crawl_date'] = str(dictionary['crawl_date'])
            dictionary['establishment_date'] = str(dictionary['establishment_date'])
        except :
            pass
        return dictionary