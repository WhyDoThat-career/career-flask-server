from admin import db
import uuid
from sqlalchemy_utils import EmailType, UUIDType, URLType, IPAddressType

USER_AUTH = [
    (u'admin', u'Admin'),
    (u'reqular', u'Regular'),
]

class Resume(db.Model) :
    id     = db.Column(db.Integer, primary_key=True)
    mongo_key = db.Column(db.String(100), nullable=False)

class User(db.Model) :
    id          = db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    password    = db.Column(db.String(128))
    auth           = db.Column(db.String(100))
    email          = db.Column(EmailType, unique=True, nullable=False)
    nickname       = db.Column(db.String(100), nullable=False)
    main_resume_id = db.Column(db.Integer, db.ForeignKey(Resume.id),nullable=True)
    main_resume    = db.relationship('Resume',foreign_keys=[main_resume_id])

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
            dictionary['deadline'] = str(dictionary['deadline'])
            dictionary['crawl_date'] = str(dictionary['crawl_date'])
        except :
            pass
        return dictionary

skills_sector_table = db.Table('skills_sector',db.Model.metadata,
                            db.Column('job_skill_id', db.Integer, db.ForeignKey('jobsector.id')),
                            db.Column('job_sector_id', db.Integer, db.ForeignKey('jobskill.id'))
                        )

class JobSkill(db.Model) :
    __tablename__ = "jobskill"
    id  = db.Column(db.Integer, primary_key=True)
    name   = db.Column(db.String(200))
    sector = db.relationship('JobSector',secondary=skills_sector_table)

    def __str__(self):
        return "{}".format(self.name)

class JobSector(db.Model) :
    __tablename__ = "jobsector"
    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(200))

    def __str__(self):
        return "{}".format(self.name)
