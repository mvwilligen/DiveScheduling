# ###########################################################################################
# ##                                                                                       ##
# ##                 #### ##    ## #### ########                     ########  ##    ##    ##
# ##                  ##  ###   ##  ##     ##                        ##     ##  ##  ##     ##
# ##                  ##  ####  ##  ##     ##                        ##     ##   ####      ##
# ##                  ##  ## ## ##  ##     ##                        ########     ##       ##
# ##                  ##  ##  ####  ##     ##                        ##           ##       ##
# ##                  ##  ##   ###  ##     ##                    ### ##           ##       ##
# ## ####### ####### #### ##    ## ####    ##    ####### ####### ### ##           ##       ##
# ##                                                                                       ##
# ###########################################################################################

# from Package.functions import logtext

print('')
print("start:  __init__.py")

import datetime
import platform
import sys
import os
import socket

from dotenv import dotenv_values
secrets = dotenv_values(".env")

from flask import Flask

app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy       import Integer, ForeignKey, String, Column, func, and_
from sqlalchemy.orm   import DeclarativeBase
from sqlalchemy.orm   import relationship

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///divescheduling.db'

cDateToday = datetime.datetime.today()
cDate      = cDateToday.strftime("%d-%m-%Y")
cTime      = cDateToday.strftime("%H:%M:%S")
cDate2     = cDateToday.strftime("%Y%m%d")
cTime2     = cDateToday.strftime("%H%M%S")
cYYYYMMDD  = cDateToday.strftime("%Y%m%d")


# added MVW - 20241114
if '_s226_' in socket.gethostname():
    app.config["APPLICATION_ROOT"] = "/ds"
    app.config["SESSION_COOKIE_PATH"] = "/ds"
    print("APPLICATION_ROOT: /ds")

    # added 20241119
    app.config['REMEMBER_COOKIE_PATH'] = '/ds'
else:
    app.config["APPLICATION_ROOT"] = "/"
    app.config["SESSION_COOKIE_PATH"] = "/"
    print(cDate2 + ";" + cTime2 + ";__init__.py;" + "APPLICATION_ROOT: /")

    # added 20241119
    app.config['REMEMBER_COOKIE_PATH'] = '/'

if socket.gethostname() == "_MWI20_":
    pass
    # app.config['SECRET_KEY'] = secrets["SECRETKEY"]
else:
    # SECRET_KEY = os.urandom(32)

    SECRET_KEY = os.environ.get('_SECRETKEY_').replace(chr(34), '')
    app.config['SECRET_KEY'] = SECRET_KEY

# 20241114 added by MvW
app.config['SECRET_KEY'] = "nn4NTEI0OjHjTfJN0hiXMGvkx05yPIFqjnvtY7dUvgzgQMT"

# added for issues with html-calendar
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

# app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_ECHO"] = False

db = SQLAlchemy(app)

from Package import routes
from Package import routes_test
from Package import routes_appointments
from Package import routes_users
from Package import routes_products
from Package import routes_instructors
from Package import routes_html

from flask_wtf.csrf import CSRFProtect

app.app_context().push()

csrf = CSRFProtect(app)

from Package.models import Products, Users, Appointments, Instructors

import socket

# # 20241115
# # source: https://flask-session.readthedocs.io/en/latest/usage.html
# from flask import session
# from flask_session import Session
# SESSION_TYPE = 'sqlalchemy'

# logtext("start:  __init__.py", "i")
print(cDate2 + ";" + cTime2 + ";" + "__init__.py;socket.gethostename():" + socket.gethostname())

cOutfile = '_logfile/logfile_' + socket.gethostname() + '_' + cYYYYMMDD + '.txt'

if socket.gethostname() == "MWI20":
    cOutfile = "_logfile\\logfile_" + socket.gethostname() + "_" + cYYYYMMDD + ".txt"

print(cDate2 + ";" + cTime2 + ";" + "__init__.py;cOutfile:" + cOutfile)

with open(cOutfile, 'a') as the_file:
    the_file.write(cDate + ";" + cTime + ";i;;;;\n")
    the_file.write(cDate + ";" + cTime + ";i;;;;__init__.py\n")

# print('')
# print("===========================================================================================================")
# print('date and time:       ', datetime.datetime.today())
# print('')
# print('OS version:          ', os.name)
# print('sys.platform:        ', sys.platform)
# print('platform.system():   ', platform.system())
# print('platform.release():  ', platform.release())
# print('platform.version():  ', platform.version())
# print('platform.platform(): ', platform.platform())
# print('')
# print('Python version:      ', sys.version)
# print('')
# print('Hostname             ', socket.gethostname())
# print('')
# print('app:                 ', app)
# print('-----------------------------------------------------------------------------------------------------------')
# print('')
print("finish: __init__.py")
print ("")

