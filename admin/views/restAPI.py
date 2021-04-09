from admin import app
from flask import send_from_directory,render_template
from flask import request, redirect, url_for, session
from admin.control import user_mgmt,data_mgmt
from flask_login import logout_user,current_user

@app.route('/',methods=["GET","POST"])
def index() :
    if request.method == "GET" :
        if not current_user.is_authenticated :
            return redirect(url_for('login'))
        else :
            if current_user.is_admin :
                return redirect('/admin')
            else :
                return send_from_directory('build','index.html')

@app.route('/register',methods=["GET","POST"])
def register() :
    if request.method == "GET" :
        return render_template('register.html')
    elif request.method == "POST" :
        user_mgmt.registerUser()
        return redirect(url_for('login'))

@app.route('/checkemail', methods=["POST"])
def check() :
    return user_mgmt.checkemail()

@app.route('/login',methods=["GET","POST"])
def login() :
    if request.method == "GET" :
        if not current_user.is_authenticated :
            return render_template('login.html')
        else :
            return redirect(url_for('index'))

@app.route('/checkloginpassword', methods=["POST"])
def checkUserpassword():
    return user_mgmt.checkloginpassword()

#The admin logout
@app.route('/logout', methods=["GET"])  # URL for logout
def logout():  # logout function
    logout_user()  # remove user session
    return redirect(url_for("login"))  # redirect to home page with message

#Forgot Password
@app.route('/forgot-password', methods=["GET"])
def forgotpassword():
    return render_template('forgot-password.html')

@app.route('/getresume',methods=["GET"])
def get_resume():
    if current_user.is_active :
        user_id = current_user.get_id().hex
        return data_mgmt.get_resume(user_id)
    else :
        return '',404

@app.route('/getdata/<selector>',methods=["GET","POST"])
def getData(selector):
    if request.method == "GET" :
        return data_mgmt.get_data(selector)

@app.route('/getcompany/<company_name>',methods=["GET","POST"])
def getCompanyData(company_name) :
    if request.method == "GET" :
        return data_mgmt.get_company_data(company_name)

@app.route('/getsector',methods=["GET","POST"])
def getDataSector():
    if request.method == "GET" :
        return data_mgmt.get_sector()

# @app.route('/getdata/skills',methods=["GET","POST"])
# def getDataBigSkills():
#     if request.method == "GET" :
#         return data_mgmt.get_data_big_company()
#404 Page
