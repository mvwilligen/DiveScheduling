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

print("")
print("start:  __init__.py")

from flask import Flask

app = Flask(__name__)
print(app)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy       import Integer, ForeignKey, String, Column, func, and_
from sqlalchemy.orm   import DeclarativeBase
from sqlalchemy.orm   import relationship

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///divescheduling.db'
app.config['SECRET_KEY'] = 'ec9bb7d32448dd860d3199a2'
app.config["SQLALCHEMY_ECHO"] = True

# moved up - 20240831 1529 - issues with reinit_db.py
db = SQLAlchemy(app)

# moved down - 20240831 1530 - issues with reinit.py
from Package import routes

# 20240822
from flask_wtf.csrf import CSRFProtect

app.app_context().push()

csrf = CSRFProtect(app)

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

print("finish: __init__.py")
print ("")
print ("")

from Package.models import Products, Users, Appointments, Instructors

# removed 20240831 1514 - issues with reinit_db.py
# from Package import db
