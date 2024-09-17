print("")
print("start:  __init__.py")

from flask import Flask

app = Flask(__name__)

from Package import routes

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy       import Integer, ForeignKey, String, Column, func, and_
from sqlalchemy.orm   import DeclarativeBase
from sqlalchemy.orm   import relationship

# 20240822
from flask_wtf.csrf import CSRFProtect

app.app_context().push()

csrf = CSRFProtect(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///divescheduling.db'
app.config['SECRET_KEY'] = 'ec9bb7d32448dd860d3199a2'

#import os
#from dotenv import load_dotenv
#load_dotenv()

# 20240823
#from flask_mailman import Mail
#app.config['MAIL_SERVER'] = 'mail.nwilligen.nl'
#app.config['MAIL_PORT'] = '465'
#app.config['MAIL_USERNAME'] = 'pv'
#app.config['MAIL_PASSWORD'] = ''
#app.config['MAIL_USE_TLS'] = True
#app.config['MAIL_USE_SSL'] = True
#mail = Mail(app)

db = SQLAlchemy(app)

global loggedonuser

print("finish: __init__.py")
print ("")
print ("")

from Package.models import Products, Users, Appointments, Instructors

from Package import db

# source: https://flask-login.readthedocs.io/en/latest/
# 20240830
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Users, int(user_id))
