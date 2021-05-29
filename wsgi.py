from admin import app, db
from admin.control.user_mgmt import register_admin

db.create_all()
register_admin()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000',debug=True)
