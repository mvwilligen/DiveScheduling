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

print('')
print("start:  __init__.py")

import datetime
import platform
import sys
import os

from dotenv import dotenv_values
secrets = dotenv_values(".env")

from flask import Flask

app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy       import Integer, ForeignKey, String, Column, func, and_
from sqlalchemy.orm   import DeclarativeBase
from sqlalchemy.orm   import relationship

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///divescheduling.db'

import socket
if socket.gethostname() == "_MWI20_":
    pass
    # app.config['SECRET_KEY'] = secrets["SECRETKEY"]
else:
    # SECRET_KEY = os.urandom(32)

    SECRET_KEY = os.environ.get('_SECRETKEY_').replace(chr(34), '')
    app.config['SECRET_KEY'] = SECRET_KEY

app.config['SEND_FILE_MAX_AGE_DEFAULT']=0

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

print('')
print("===========================================================================================================")
print('date and time:       ', datetime.datetime.today())
print('')
print('OS version:          ', os.name)
print('sys.platform:        ', sys.platform)
print('platform.system():   ', platform.system())
print('platform.release():  ', platform.release())
print('platform.version():  ', platform.version())
print('platform.platform(): ', platform.platform())
print('')
print('Python version:      ', sys.version)
print('')
print('Hostname             ', socket.gethostname())
print('')
print('app:                 ', app)
print('-----------------------------------------------------------------------------------------------------------')
print('')
print("finish: __init__.py")
print ("")

