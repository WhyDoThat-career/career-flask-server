from admin import app, db
from admin.control.user_mgmt import registerAdmin

db.create_all()
registerAdmin()
print('jenkins test5')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888',debug=True)
