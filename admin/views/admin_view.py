from admin import app, db
from admin.model.mysql import USER_AUTH,User,JobDetail,JobSector,JobSkill,Resume,CompanyInfo

import flask_admin as admin
from flask_admin import expose
from flask_admin.base import MenuLink
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from flask_admin.contrib.sqla.filters import FilterEqual
from flask_admin.form.rules import HTML,Markup
from flask_login import logout_user,current_user
from flask import send_from_directory,request, redirect,render_template,url_for,abort


class UserAdmin(sqla.ModelView):
    can_view_details = True
    create_modal = True
    edit_modal = True
    column_auto_select_related = True
    column_default_sort = [('nickname', False)]  # sort on multiple columns
    action_disallowed_list = ['delete', ]

    form_choices = {
        'auth': USER_AUTH,
    }

    form_widget_args = {
        'id': {
            'readonly': True
        }
    }
    column_list = [
        'auth',
        'nickname',
        'email',
        'thumbnail'
    ]
    column_searchable_list = [
        'nickname',
        'email',
        'auth',
    ]
    column_editable_list = ['auth','thumbnail']
    column_details_list = [
        'id',
        'password',
    ] + column_list
    form_columns = [
        'id',
        'auth',
        'nickname',
        'email',
        'thumbnail'
    ]
    form_create_rules = [
        'nickname',
        'auth',
        'email',
    ]
    column_filters = [
        'nickname',
        FilterEqual(column=User.nickname, name='Nick Name'),
        'auth',
        'email',
    ]
    def edit_form(self, obj):
        return self._filtered_posts(
            super(UserAdmin, self).edit_form(obj)
        )
    def is_accessible(self):
        try :
            return current_user.is_admin
        except :
            False

def _set_image_tag(view,text,model,name) :
    return Markup(f'<img src={model.logo_image}>')
def _set_hyper_link(view,text,model,name) :
    return Markup(f'<a href={model.href}>{model.href}</a>')
def _set_html(view,text,model,name) :
    return Markup(f'{model.main_text}')

class JobDetailAdmin(sqla.ModelView) :
    detail_template = 'admin/views/templates/detail.html'
    can_view_details = True
    column_display_pk = True
    create_modal = True
    edit_modal = True
    can_export = True
    export_types = ['csv', 'xls']
    column_list = ['title','company_name', 'sector','skill_tag', 'salary','platform','crawl_date' ]
    column_editable_list = ['sector', ]
    column_default_sort = ('crawl_date', True)
    column_sortable_list = [
        'salary',
        'crawl_date',
        'platform'
    ]
    column_searchable_list = [
        'title',
        'company_name', 
        'sector',
        'skill_tag', 
        'platform',
        'href'
    ]
    column_labels = {
        'title':'Title',
        'company_name':'Company', 
        'sector':'Sector',
        'skill_tag':'Skills', 
        'platform':'Platform',
    }
    column_filters = [
        'title',
        'company_name', 
        'sector',
        'skill_tag', 
        'big_company',
        'platform',
    ]
    column_details_list = [
        'crawl_date',
        'id',     
        'title',     
        'href',       
        'salary',
        'skill_tag',
        'sector',  
        'newbie',
        'career',
        'deadline',
        'company_name',
        'company_address', 
        'logo_image',
        'platform',
        'big_company',
        'main_text',
    ]
    column_formatters = {
        'logo_image' : _set_image_tag,
        'main_text' : _set_html,
        'href' : _set_hyper_link
    }
    def is_accessible(self):
        try :
            return current_user.is_admin
        except :
            False

class CompanyInfoAdmin(sqla.ModelView) :
    detail_template = 'admin/views/templates/detail.html'
    can_view_details = True
    column_display_pk = True
    create_modal = True
    edit_modal = True
    can_export = True
    export_types = ['csv', 'xls']
    column_list = ['name','sector', 'scale','employees', 'star_point','salary_average','interview_level' ]
    column_editable_list = ['sector', ]
    column_default_sort = ('star_point', True)
    column_sortable_list = [
        'salary_average',
        'crawl_date',
        'scale',
        'interview_level',
        'employees'
    ]
    column_searchable_list = [
        'name',
        'sector', 
        'scale',
    ]
    column_labels = {
        'name':'Name',
        'company_name':'Company', 
        'scale':'Scale',
        'employees':'Employees', 
        'star_point':'Star_point',
        'salary_average' : 'Salary_average',
        'interview_level':'interview_level',
    }
    column_filters = [
        'name',
        'salary_average',
        'crawl_date',
        'scale',
        'interview_level',
        'employees'
    ]
    column_details_list = [
        "crawl_date",
        "id",     
        "name",
        "sector",
        "scale",
        "employees",
        "establishment_date",
        "review_count",
        "star_point",
        "salary_count",
        "salary_average",
        "interview_count",
        "interview_level",
        "interview_feel"
    ]
    def is_accessible(self):
        try :
            return current_user.is_admin
        except :
            False
    
class IndexAdmin(admin.AdminIndexView) :
    @expose('/')
    def index(self):
        if request.method == "GET" :
            if not current_user.is_authenticated :
                return redirect(url_for('index'))
            elif current_user.is_anonymous :
                return redirect(url_for('index'))
            elif current_user.is_admin :
                return self.render('index.html')
            else :
                return redirect(url_for('index'))

admin = admin.Admin(app,index_view=IndexAdmin(), name ='WhyDoThat Admin page', template_mode='bootstrap4')

admin.add_view(UserAdmin(User,db.session))
admin.add_view(JobDetailAdmin(JobDetail,db.session))
admin.add_view(CompanyInfoAdmin(CompanyInfo,db.session))
admin.add_view(sqla.ModelView(JobSector,db.session))
admin.add_view(sqla.ModelView(JobSkill,db.session))
admin.add_view(sqla.ModelView(Resume,db.session,category='Other'))
admin.add_sub_category(name="Links", parent_name="Other")
admin.add_link(MenuLink(name='Back Home', url='/', category='Links'))
admin.add_link(MenuLink(name='Logout', url='/api/logout', category='Links'))