###########################################################################################
##                                                                                       ##
##                 #### ##    ## #### ########                     ########  ##    ##    ##
##                  ##  ###   ##  ##     ##                        ##     ##  ##  ##     ##
##                  ##  ####  ##  ##     ##                        ##     ##   ####      ##
##                  ##  ## ## ##  ##     ##                        ########     ##       ##
##                  ##  ##  ####  ##     ##                        ##           ##       ##
##                  ##  ##   ###  ##     ##                    ### ##           ##       ##
## ####### ####### #### ##    ## ####    ##    ####### ####### ### ##           ##       ##
##                                                                                       ##
###########################################################################################
                                                               

# added 20240831 1509   - issues with reinit_db.py
# removed 20240831 .... - issues with reinit_db.py
# added 20240831 1515   - issues with reinit_db.py
# removed 20240831 1526 - issues with reinit_db.py
# from Package import db

import datetime
import platform
import sys
import os

print('')
print("start:  __init__.py")
print('')
print("===========================================================================================================")
print('date and time:       ', datetime.datetime.today())
print('OS version:          ', os.name)
print('sys.platform:        ', sys.platform)
print('platform.system():   ', platform.system())
print('platform.release():  ', platform.release())
print('platform.version():  ', platform.version())
print('platform.platform(): ', platform.platform())
print('Python version:      ', sys.version)
print('-----------------------------------------------------------------------------------------------------------')
print('')

from dotenv import dotenv_values

# config = dotenv_values(".env")
# print('config: ', config )
# 
# u = config['SMTP_USER']
# 
# print(config['SMTP_USER'])

secrets = dotenv_values(".env")

# s = secrets["SECRETKEY"]
# print('s: ', s)
# f = secrets["FTP_USER"]
# print('f: ', f)
# print('secrets["FTP_USER"]: ', secrets["FTP_USER"])
# s = secrets["SMTP_USER"]
# print('s: ', s)
# print('secrets["SMTP_USER"]: ', secrets["SMTP_USER"])
# print()
# print('secrets: ', secrets)
# print()
# print(secrets["SMTP_USER"])
# print("SMTP_USER: ", secrets["SMTP_USER"])
# print("FTP_USER:  ", secrets["FTP_USER"])
# print()

from flask import Flask

app = Flask(__name__)
print(app)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy       import Integer, ForeignKey, String, Column, func, and_
from sqlalchemy.orm   import DeclarativeBase
from sqlalchemy.orm   import relationship

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///divescheduling.db'
app.config['SECRET_KEY'] = secrets["SECRETKEY"]

# app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_ECHO"] = False

# moved up - 20240831 1529 - issues with reinit_db.py
db = SQLAlchemy(app)

# moved down - 20240831 1530 - issues with reinit.py
from Package import routes

# 20240822
from flask_wtf.csrf import CSRFProtect

app.app_context().push()

csrf = CSRFProtect(app)

print("finish: __init__.py")
print ("")
print ("")

from Package.models import Products, Users, Appointments, Instructors

# removed 20240831 1514 - issues with reinit_db.py
# from Package import db
