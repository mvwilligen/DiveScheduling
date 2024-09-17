from Package import app
# from Package import db

global loggedonuser
loggedonuser = "none"

if __name__ == '__main__':
    app.run(debug=True)
