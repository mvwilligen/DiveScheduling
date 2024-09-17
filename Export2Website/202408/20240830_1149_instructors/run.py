from Package import app
from Package import db

print('run.py\app: ' + app)
print('run.py\db:  ' + db)

global loggedonuser
loggedonuser = "none"

if __name__ == '__main__':
    app.run(debug=True)
