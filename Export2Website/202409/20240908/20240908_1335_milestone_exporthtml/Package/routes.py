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

from Package import db
from Package import app
from Package.models import Appointments, Users, Instructors, Products

from flask import Flask, render_template, redirect, url_for, flash, request
from Package.forms import AppointmentsEditForm, LoginForm, ProductsEditForm, ProductsUsersForm, ProductsNewForm, UsersRegisterForm, UsersInfoForm, UsersEditForm2, UsersProductForm2, AppointmentsDateForm2

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

from Package.functions import get_rbac, no_access_text

import os

def test2(cText):
    print('')
    print('test: ', cText)
    print('')
    return()

def myquery(dbquery):

    result = []

    if len(dbquery) > 0:
        print('')
        print('#### datetime.datetime.now() - dbquery: ', dbquery)
        print('')
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

    #                                            0                1                  2                3               4                     5                  6                  7                 8                   9
    #appointments = db.session.execute(db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Instructors.Name, Appointments.Staff, Appointments.Product). \
    #                            order_by(Appointments.Date). \
    #                            where(and_(func.DATE(Appointments.Date) >= datetime.datetime(nYearFrom, nMonthFrom, nDayFrom), \
    #                                       func.DATE(Appointments.Date) <= datetime.datetime(nYearTo,   nMonthTo,   nDayTo))). \
    #                            select_from(Appointments). \
    #                            join(Users, Appointments.User        == Users.Id). \
    #                            join(Instructors, Appointments.Staff == Instructors.Id). \
    #                            join(Products, Appointments.Product  == Products.Id) )

    dbquery = 'db.session.execute(db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Instructors.Name, Appointments.Staff, Appointments.Product).'
    dbquery = dbquery + 'order_by(Appointments.Date).'
    dbquery = dbquery + 'where(and_(func.DATE(Appointments.Date) >= datetime.datetime('+ str(nYearFrom) + ', ' + str(nMonthFrom) + ', ' + str(nDayFrom) + '),'
    dbquery = dbquery + 'func.DATE(Appointments.Date) <= datetime.datetime(' + str(nYearTo) + ', ' + str(nMonthTo) + ',' + str(nDayTo) + '))).'
    dbquery = dbquery + 'select_from(Appointments).'
    dbquery = dbquery + 'join(Users, Appointments.User        == Users.Id).'
    dbquery = dbquery + 'join(Instructors, Appointments.Staff == Instructors.Id).'
    dbquery = dbquery + 'join(Products, Appointments.Product  == Products.Id) )'

    print('len(dbquery): ', len(dbquery))
    print('#### dbquery: ', dbquery)
   
    # appointments = eval(dbquery)
    appointments = myquery(dbquery)

    lRBAC = get_rbac(request.url_rule.endpoint)
 
    return render_template('home.html', appointments = appointments, lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

   ###    ########  ########   #######  #### ##    ## ######## ##     ## ######## ##    ## ########  ######  
  ## ##   ##     ## ##     ## ##     ##  ##  ###   ##    ##    ###   ### ##       ###   ##    ##    ##    ## 
 ##   ##  ##     ## ##     ## ##     ##  ##  ####  ##    ##    #### #### ##       ####  ##    ##    ##       
##     ## ########  ########  ##     ##  ##  ## ## ##    ##    ## ### ## ######   ## ## ##    ##     ######  
######### ##        ##        ##     ##  ##  ##  ####    ##    ##     ## ##       ##  ####    ##          ## 
##     ## ##        ##        ##     ##  ##  ##   ###    ##    ##     ## ##       ##   ###    ##    ##    ## 
##     ## ##        ##         #######  #### ##    ##    ##    ##     ## ######## ##    ##    ##     ######  


@app.route('/appointments')
def appointments():

    if current_user.is_anonymous:
        return (no_access_text())

    #appointments = Appointments.query.order_by(Appointments.Date.desc()).all()
    #appointments = Appointments.query.order_by(Appointments.Date.asc()).all()

    #                                            0                1                  2                3               4                     5                  6                  7                   8                 9
    appointments = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name, Instructors.Id). \
                                order_by(Appointments.Date). \
                                select_from(Appointments). \
                                join(Users,       Appointments.User    == Users.Id). \
                                join(Instructors, Appointments.Staff   == Instructors.Id). \
                                join(Products,    Appointments.Product == Products.Id) )

    lRBAC = get_rbac(request.url_rule.endpoint)


    return render_template('appointments.html', appointments = appointments, lRBAC = lRBAC)

#------------------------------------------------------------------------------------------


   ###    ########  ########          ########  ######## ##       ######## ######## ######## 
  ## ##   ##     ## ##     ##         ##     ## ##       ##       ##          ##    ##       
 ##   ##  ##     ## ##     ##         ##     ## ##       ##       ##          ##    ##       
##     ## ########  ########          ##     ## ######   ##       ######      ##    ######   
######### ##        ##                ##     ## ##       ##       ##          ##    ##       
##     ## ##        ##                ##     ## ##       ##       ##          ##    ##       
##     ## ##        ##        ####### ########  ######## ######## ########    ##    ######## 

@app.route('/appointmentsdelete/<int:id>/<string:cFrom>')
def appointmentsdelete(id, cFrom):

    if current_user.is_anonymous:
        return (no_access_text())

    appointment = db.session.execute(db.select(Appointments).filter_by(Id=id)).scalar_one()
    nPrevUser = appointment.User
    db.session.delete(appointment)
    db.session.commit()
    #                                                   0             1                2                 3                 4                5                       5               7                 8
    appointments = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name). \
                                order_by(Appointments.Date). \
                                select_from(Appointments). \
                                join(Users, Appointments.User == Users.Id). \
                                join(Instructors, Appointments.Staff == Instructors.Id). \
                                join(Products, Appointments.Product == Products.Id) )

    if cFrom == 'home':
        return redirect(url_for('homepage'))

    if cFrom == 'usersinfo':
        return redirect(url_for('usersinfo', id = nPrevUser))

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('appointments.html', appointments = appointments, lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

   ###    ########  ########             ###     ######   ######  ####  ######   ##    ## 
  ## ##   ##     ## ##     ##           ## ##   ##    ## ##    ##  ##  ##    ##  ###   ## 
 ##   ##  ##     ## ##     ##          ##   ##  ##       ##        ##  ##        ####  ## 
##     ## ########  ########          ##     ##  ######   ######   ##  ##   #### ## ## ## 
######### ##        ##                #########       ##       ##  ##  ##    ##  ##  #### 
##     ## ##        ##                ##     ## ##    ## ##    ##  ##  ##    ##  ##   ### 
##     ## ##        ##        ####### ##     ##  ######   ######  ####  ######   ##    ## 

@app.route('/appointmentsassign/<int:id>/<string:cFrom>')
def appointmentsassign(id, cFrom):

    if current_user.is_anonymous:
        return (no_access_text())

    #print('-------------------------------------------------------')

    #print(f'current_user.Username: { current_user.Username }')
    #print('current_user.Username: ' + current_user.Username )

    #if current_user.is_authenticated:
    #    print('current_user.is_authenticated')
    #    print(current_user.is_authenticated)

    user = db.session.execute(db.select(Users).filter_by(Username = current_user.Username)).scalar_one()
    instructor = db.session.execute(db.select(Instructors).filter_by(User = user.Id)).scalar_one()
    appointment = db.session.execute(db.select(Appointments).filter_by(Id=id)).scalar_one()

    appointment.Staff = instructor.Id
    db.session.commit()

    #                                                   0             1                2                 3                 4                5                       5               7                 8
    print ('appointment.Staff: ' + str(appointment.Staff))
    print('-------------------------------------------------------')

    appointments = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name). \
                                order_by(Appointments.Date). \
                                select_from(Appointments). \
                                join(Users, Appointments.User == Users.Id). \
                                join(Instructors, Appointments.Staff == Instructors.Id). \
                                join(Products, Appointments.Product == Products.Id) )
    
    if cFrom == 'home':
        return redirect(url_for('homepage'))

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('appointments.html', appointments = appointments, lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

   ###    ########  ########          ##     ## ##    ##    ###     ######   ######  ####  ######   ##    ## 
  ## ##   ##     ## ##     ##         ##     ## ###   ##   ## ##   ##    ## ##    ##  ##  ##    ##  ###   ## 
 ##   ##  ##     ## ##     ##         ##     ## ####  ##  ##   ##  ##       ##        ##  ##        ####  ## 
##     ## ########  ########          ##     ## ## ## ## ##     ##  ######   ######   ##  ##   #### ## ## ## 
######### ##        ##                ##     ## ##  #### #########       ##       ##  ##  ##    ##  ##  #### 
##     ## ##        ##                ##     ## ##   ### ##     ## ##    ## ##    ##  ##  ##    ##  ##   ### 
##     ## ##        ##        #######  #######  ##    ## ##     ##  ######   ######  ####  ######   ##    ## 

@app.route('/appointmentsunassign/<int:id>/<string:cFrom>')
def appointmentsunassign(id, cFrom):

    if current_user.is_anonymous:
        return (no_access_text())

    appointment = db.session.execute(db.select(Appointments).filter_by(Id=id)).scalar_one()

    appointment.Staff = 1
    db.session.commit()
    #                                                   0             1                2                 3                 4                5                       5               7                 8
    appointments = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name). \
                                order_by(Appointments.Date). \
                                select_from(Appointments). \
                                join(Users, Appointments.User == Users.Id). \
                                join(Instructors, Appointments.Staff == Instructors.Id). \
                                join(Products, Appointments.Product == Products.Id) )
    
    if cFrom == 'home':
        return redirect(url_for('homepage'))

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('appointments.html', appointments = appointments , lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

   ###    ########  ########          ######## ########  #### ######## 
  ## ##   ##     ## ##     ##         ##       ##     ##  ##     ##    
 ##   ##  ##     ## ##     ##         ##       ##     ##  ##     ##    
##     ## ########  ########          ######   ##     ##  ##     ##    
######### ##        ##                ##       ##     ##  ##     ##    
##     ## ##        ##                ##       ##     ##  ##     ##    
##     ## ##        ##        ####### ######## ########  ####    ##    

@app.route('/appointmentsedit/<int:id>/<string:cFrom>', methods=['GET', 'POST'])
def appointmentsedit(id, cFrom):

    if current_user.is_anonymous:
        return (no_access_text())

    form = AppointmentsEditForm()

    cDebug = ''
    #                                           0                1                  2                3               4                    5                   6                  7                   8                 9
    #appointment = db.session.execute(db.select(Appointments).filter_by(Id=id)).scalar_one()
    appointment = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name, Appointments.Notes). \
                                select_from(Appointments). \
                                filter_by(Id = id). \
                                join(Users, Appointments.User == Users.Id). \
                                join(Instructors, Appointments.Staff == Instructors.Id). \
                                join(Products, Appointments.Product == Products.Id) )

    instructors = db.session.execute(db.select(Instructors.Id, Instructors.User, Instructors.Name).where(Instructors.Active).order_by(Instructors.Name))

    appointment2 = []

    for row in appointment:
        for element in row:

            appointment2.append(element)

            if isinstance(element, int):
                cDebug = cDebug + str(element) + "; "
            elif isinstance(element, datetime.date):
                cDebug = cDebug + element.strftime("%d-%m-%Y") + "; "
            elif isinstance(element, datetime.datetime):
                cDebug = cDebug + element.strftime("%d-%m-%Y") + "; "
            else:
                cDebug = cDebug + element + "; "
        cDebug = cDebug + '#BR#'

    # appointment = db.get_or_404(Appointments, id)

    if form.validate_on_submit():

        x = db.session.query(Appointments).get(id)
        cStaff = request.form["instructor"]
        cDate  = request.form["date"]
        cTime  = request.form["time"]

        # cDebug = cStaff + ', ' + cDate + ', ' + cTime

        instructors = db.session.execute(db.select(Instructors.Id, Instructors.User, Instructors.Name))

        nStaff = 6
        for i in instructors:
            if i.Name == cStaff:
                nStaff = i.Id

        # cDebug = cDebug + ', ' + str(nStaff)

        dDateText = cDate[0:4] + '-' + cDate[5:7] + '-' + cDate[8:10] + ' | ' + cTime[0:2] + '.' + cTime[3:5]
        # dDate = date(int(cDate[0:4]), int(cDate[5:7]), int(cDate[8:10])) # , int(cTime[0:2]), int(cTime[3:5]))
        
        dDate = datetime.datetime(int(cDate[0:4]), int(cDate[5:7]), int(cDate[8:10]), int(cTime[0:2]), int(cTime[3:5]))

        x.Date  = dDate
        x.Staff = nStaff
        x.Notes = request.form["notes"] # cStaff + ' | ' + cDate + ' | ' + cTime + ' | ' + dDateText + ' | ' + dDate.strftime('%Y-%m-%d_%H.%M')
        # x.Notes  = cDebug

        db.session.commit()

        if cFrom == 'home':
            return redirect(url_for('homepage'))

        return redirect(url_for('appointments'))

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('appointmentsedit.html', form=form, appointment=appointment2, cDebug=cDebug, instructors=instructors, lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

   ###    ########  ########          ########     ###    ######## ######## 
  ## ##   ##     ## ##     ##         ##     ##   ## ##      ##    ##       
 ##   ##  ##     ## ##     ##         ##     ##  ##   ##     ##    ##       
##     ## ########  ########          ##     ## ##     ##    ##    ######   
######### ##        ##                ##     ## #########    ##    ##       
##     ## ##        ##                ##     ## ##     ##    ##    ##       
##     ## ##        ##        ####### ########  ##     ##    ##    ######## 

@app.route('/appointmentsdateform2/<string:text>/<string:cFrom>', methods=['GET', 'POST'])
def appointmentsdate2(text, cFrom):

    if current_user.is_anonymous:
        return (no_access_text())

    form = AppointmentsDateForm2(text)

    # appointment = db.session.execute(db.select(Appointments).filter_by(Id=id)).scalar_one()
    #
    #user    = appointment.User
    #product = appointment.Product

    # http://127.0.0.1:5000/appointmentsdateform2/02-09-2024/
    cDate = text [6:10] + '_' + text [3:5] + "_" + text [0:2]
    dDate = datetime.date(int(text [6:10]), int(text [3:5]), int(text [0:2]))

#    #                                           0                1                  2                3               4                     5                  6                  7                   8                 9               10
    appointments = db.session.execute(db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name, Instructors.Id, Appointments.Product). \
                                where(func.date(Appointments.Date) == dDate). \
                                order_by(Appointments.Product). \
                                join(Users,       Appointments.User    == Users.Id). \
                                join(Instructors, Appointments.Staff   == Instructors.Id). \
                                join(Products,    Appointments.Product == Products.Id) )

    instructors = db.session.execute(db.select(Instructors.Id, Instructors.User, Instructors.Name).where(Instructors.Active).order_by(Instructors.Name))

    filtered2 = [] # necessary because list could be for/endfor once.
    for i in instructors:
        filtered2.append(i)

    # filter on product.Id (solution for multiple filters not found)
    filtered = []
    for a in appointments:
        filtered.append(a)

    filtered.sort(key = lambda x: x[4]) # sort on productname

    if form.validate_on_submit():

        for a in filtered:
            cDate = chr(34) + 'date' + str(a [0]) + chr(34)
            cDateValue = request.form.get(eval(cDate))
            cTime = chr(34) + 'time' + str(a [0]) + chr(34)
            cTimeValue = request.form.get(eval(cTime))
            cInstructor = chr(34) + 'instructor' + str(a [0]) + chr(34)
            cInstructorValue = request.form.get(eval(cInstructor))

            nInstructor = 0
            for i in filtered2:
                if i.Name == cInstructorValue:
                    nInstructor = i.Id

            appointment = db.session.execute(db.select(Appointments).filter_by(Id=a [0])).scalar_one()
            dDate = datetime.datetime(int(cDateValue[0:4]), int(cDateValue[5:7]), int(cDateValue[8:10]), int(cTimeValue[0:2]), int(cTimeValue[3:5]))
            appointment.Date = dDate
            appointment.Staff = nInstructor
            db.session.commit()

        lRBAC = get_rbac(request.url_rule.endpoint)

        users = Users.query.all()

        if cFrom == 'home':
            return redirect(url_for('homepage'))           

        return render_template('users.html', users = users, lRBAC = lRBAC)

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('usersproductform.html', form=form, instructors = filtered2, appointments = filtered, lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

#### ##    ##  ######  ######## ########  ##     ##  ######  ########  #######  ########   ######  
 ##  ###   ## ##    ##    ##    ##     ## ##     ## ##    ##    ##    ##     ## ##     ## ##    ## 
 ##  ####  ## ##          ##    ##     ## ##     ## ##          ##    ##     ## ##     ## ##       
 ##  ## ## ##  ######     ##    ########  ##     ## ##          ##    ##     ## ########   ######  
 ##  ##  ####       ##    ##    ##   ##   ##     ## ##          ##    ##     ## ##   ##         ## 
 ##  ##   ### ##    ##    ##    ##    ##  ##     ## ##    ##    ##    ##     ## ##    ##  ##    ## 
#### ##    ##  ######     ##    ##     ##  #######   ######     ##     #######  ##     ##  ######  

@app.route('/instructors')
def instructors():

    if current_user.is_anonymous:
        return (no_access_text())

    instructors = db.session.execute( db.select(Instructors.Id, Instructors.User, Instructors.Name, Instructors.Active). \
                                order_by(Instructors.Name). \
                                select_from(Instructors). \
                                join(Users, Instructors.User == Users.Id) )
    
    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('instructors.html', instructors = instructors , lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

#### ##    ##  ######          #### ##    ## ########  #######  
 ##  ###   ## ##    ##          ##  ###   ## ##       ##     ## 
 ##  ####  ## ##                ##  ####  ## ##       ##     ## 
 ##  ## ## ##  ######           ##  ## ## ## ######   ##     ## 
 ##  ##  ####       ##          ##  ##  #### ##       ##     ## 
 ##  ##   ### ##    ##          ##  ##   ### ##       ##     ## 
#### ##    ##  ######  ####### #### ##    ## ##        #######  

@app.route('/instructorsinfo/<id>/')
def instructorsinfo(id):

    if current_user.is_anonymous:
        return (no_access_text())

    instructor = db.session.execute( db.select(Instructors.Id, Instructors.User, Instructors.Name). \
                                order_by(Instructors.Name). \
                                where(Instructors.User == id).\
                                select_from(Instructors). \
                                join(Users, Instructors.User    == Users.Id) )

    instructor2 = []

    # export data in csv-format
    cCSV = ""

    for row in instructor:

            instructor2.append(row)

            for element in row:
                if isinstance(element, int):
                    cCSV = cCSV + str(element) + "; "
                elif isinstance(element, datetime.date):
                    cCSV = cCSV + element.strftime("%d-%m-%Y") + "; "
                elif isinstance(element, datetime.datetime):
                    cCSV = cCSV + element.strftime("%d-%m-%Y") + "; "
                else:
                    cCSV = cCSV + element + "; "
            cCSV = cCSV + '#BR#'

    #                                            0                1                  2                3               4                    5                   6                  7                   8                 9
    appointments = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name, Appointments.Notes). \
                                order_by(Appointments.Date). \
                                select_from(Appointments). \
                                where(Appointments.Staff == int(cCSV [0:1])). \
                                join(Users,       Appointments.User == Users.Id). \
                                join(Instructors, Appointments.Staff == Instructors.Id). \
                                join(Products,    Appointments.Product == Products.Id) )

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('instructorsinfo.html', instructor = instructor2, appointments = appointments , lRBAC = lRBAC)

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

    form = LoginForm()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

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

                lRBAC = get_rbac(request.url_rule.endpoint)
                return render_template('login.html', form = form)

        # user = db.session.execute(db.select(Users).filter(func.lower(Users.Username) == func.lower(username))).one_or_none() # scalar_one() ## <class 'sqlalchemy.engine.row.Row'>
        # user = db.session.execute(db.select(Users).filter(func.lower(Users.Username) == func.lower(username))).scalar_one() ## <class 'Package.models.Users'>

        # user = Users.query.filter_by(Username = username).first()
        user = Users.query.filter(Users.Username.ilike(username)).first()
        print('type(user): ', type(user))

        if user is not None:

            print('-----------------------------------------')
            print('username:          ', username)
            print('password:          ', password)
            print(user)
            print('type:              ', type(user))
            print('user.Passwordhash: ', user.Passwordhash)
            print('-----------------------------------------')

            pwhash = user.Passwordhash
   
            if user and bcrypt.check_password_hash(pwhash, password):
                login_user(user)

                lRBAC = get_rbac(request.url_rule.endpoint)
                return redirect(url_for('homepage'))
        
    lRBAC = get_rbac(request.url_rule.endpoint)
    return render_template('login.html', form = form)

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

########  ########   #######  ########  ##     ##  ######  ########  ######  
##     ## ##     ## ##     ## ##     ## ##     ## ##    ##    ##    ##    ## 
##     ## ##     ## ##     ## ##     ## ##     ## ##          ##    ##       
########  ########  ##     ## ##     ## ##     ## ##          ##     ######  
##        ##   ##   ##     ## ##     ## ##     ## ##          ##          ## 
##        ##    ##  ##     ## ##     ## ##     ## ##    ##    ##    ##    ## 
##        ##     ##  #######  ########   #######   ######     ##     ######  

@app.route('/products')
def products():

    if current_user.is_anonymous:
        return (no_access_text())

    products = Products.query.all()

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('products.html', products=products , lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

########  ########   #######          ######## ########  #### ######## 
##     ## ##     ## ##     ##         ##       ##     ##  ##     ##    
##     ## ##     ## ##     ##         ##       ##     ##  ##     ##    
########  ########  ##     ##         ######   ##     ##  ##     ##    
##        ##   ##   ##     ##         ##       ##     ##  ##     ##    
##        ##    ##  ##     ##         ##       ##     ##  ##     ##    
##        ##     ##  #######  ####### ######## ########  ####    ##    

@app.route('/productsedit/<id>/', methods=('GET', 'POST'))
def productsedit(id):

    if current_user.is_anonymous:
        return (no_access_text())

    form = ProductsEditForm(id)
    product = db.get_or_404(Products, id)

    if form.validate_on_submit():

        x = db.session.query(Products).get(id)
        x.Date        = request.form["abbr"]
        x.Parts       = request.form["parts"]
        x.Description = request.form["description"]
        db.session.commit()

        return redirect(url_for('products'))

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('productsedit.html', form=form, product=product , lRBAC = lRBAC)
#------------------------------------------------------------------------------------------

########  ########   #######          ##    ## ######## ##      ## 
##     ## ##     ## ##     ##         ###   ## ##       ##  ##  ## 
##     ## ##     ## ##     ##         ####  ## ##       ##  ##  ## 
########  ########  ##     ##         ## ## ## ######   ##  ##  ## 
##        ##   ##   ##     ##         ##  #### ##       ##  ##  ## 
##        ##    ##  ##     ##         ##   ### ##       ##  ##  ## 
##        ##     ##  #######  ####### ##    ## ########  ###  ###  

@app.route('/productsnew/', methods=('GET', 'POST'))
def productsnew():

    if current_user.is_anonymous:
        return (no_access_text())

    form = ProductsNewForm()

    if form.validate_on_submit():

        newproductname = request.form["productname"].replace(' ', '_')

        product_to_create = Products(Productname = newproductname,
                                     Abbr        = request.form["abbr"],
                                     Parts       = request.form["parts"],
                                     Description = request.form["description"])
         
        db.session.add(product_to_create)
        db.session.commit()

        return redirect(url_for('products'))

    lRBAC = get_rbac(request.url_rule.endpoint) 

    return render_template('productsnew.html', form = form, lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

########  ########   #######          ########  ######## ##       ######## ######## ######## 
##     ## ##     ## ##     ##         ##     ## ##       ##       ##          ##    ##       
##     ## ##     ## ##     ##         ##     ## ##       ##       ##          ##    ##       
########  ########  ##     ##         ##     ## ######   ##       ######      ##    ######   
##        ##   ##   ##     ##         ##     ## ##       ##       ##          ##    ##       
##        ##    ##  ##     ##         ##     ## ##       ##       ##          ##    ##       
##        ##     ##  #######  ####### ########  ######## ######## ########    ##    ######## 

@app.route('/productsdelete/<id>/')
def productsdelete(id):

    if current_user.is_anonymous:
        return (no_access_text())

    product = db.session.execute(db.select(Products).filter_by(Id=id)).scalar_one()
    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('products'))

#------------------------------------------------------------------------------------------

########  ########   #######          ##     ##  ######  ######## ########   ######  
##     ## ##     ## ##     ##         ##     ## ##    ## ##       ##     ## ##    ## 
##     ## ##     ## ##     ##         ##     ## ##       ##       ##     ## ##       
########  ########  ##     ##         ##     ##  ######  ######   ########   ######  
##        ##   ##   ##     ##         ##     ##       ## ##       ##   ##         ## 
##        ##    ##  ##     ##         ##     ## ##    ## ##       ##    ##  ##    ## 
##        ##     ##  #######  #######  #######   ######  ######## ##     ##  ######  

@app.route('/productsusers/<id>/')
def productsusers(id):

    if current_user.is_anonymous:
        return (no_access_text())

    form = ProductsUsersForm(id)

    #                                            0                1                  2                3               4                     5
    appointments = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name). \
                                order_by(Appointments.User). \
                                where(Appointments.Product == id). \
                                select_from(Appointments). \
                                join(Users, Appointments.User == Users.Id). \
                                join(Instructors, Appointments.Staff == Instructors.Id). \
                                join(Products, Appointments.Product == Products.Id) )

    appointments2 = []

    # export data in csv-format
    cAppointments = ""
    cUser = ""
    for row in appointments:
        if cUser != row [2] + row [3]:
            cUser = row [2] + row [3]

            appointments2.append(row)

            for element in row:
                if isinstance(element, int):
                    cAppointments = cAppointments + str(element) + "; "
                elif isinstance(element, datetime.date):
                    cAppointments = cAppointments + element.strftime("%d-%m-%Y") + "; "
                elif isinstance(element, datetime.datetime):
                    cAppointments = cAppointments + element.strftime("%d-%m-%Y") + "; "
                else:
                    cAppointments = cAppointments + element + "; "
            cAppointments = cAppointments + '#BR#'

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('productsusers.html', appointments = appointments2, form = form, cAppointments = cAppointments , lRBAC = lRBAC)

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

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('support.html' , lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

##     ##  ######  ######## ########   ######  
##     ## ##    ## ##       ##     ## ##    ## 
##     ## ##       ##       ##     ## ##       
##     ##  ######  ######   ########   ######  
##     ##       ## ##       ##   ##         ## 
##     ## ##    ## ##       ##    ##  ##    ## 
 #######   ######  ######## ##     ##  ######  

@app.route('/users')
def users():

    if current_user.is_anonymous:
        return (no_access_text())

    users = Users.query.all()

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('users.html', users = users , lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

##     ##  ######  ######## ########   ######  ########  ########   #######  ########  ##     ##  ######  ######## 
##     ## ##    ## ##       ##     ## ##    ## ##     ## ##     ## ##     ## ##     ## ##     ## ##    ##    ##    
##     ## ##       ##       ##     ## ##       ##     ## ##     ## ##     ## ##     ## ##     ## ##          ##    
##     ##  ######  ######   ########   ######  ########  ########  ##     ## ##     ## ##     ## ##          ##    
##     ##       ## ##       ##   ##         ## ##        ##   ##   ##     ## ##     ## ##     ## ##          ##    
##     ## ##    ## ##       ##    ##  ##    ## ##        ##    ##  ##     ## ##     ## ##     ## ##    ##    ##    
 #######   ######  ######## ##     ##  ######  ##        ##     ##  #######  ########   #######   ######     ##    

@app.route('/usersproductform2/<id>/', methods=['GET', 'POST'])
def usersproduct2(id):

    if current_user.is_anonymous:
        return (no_access_text())

    form = UsersProductForm2(id)

    appointment = db.session.execute(db.select(Appointments).filter_by(Id=id)).scalar_one()

    user    = appointment.User
    product = appointment.Product

#    #                                           0                1                  2                3               4                     5                  6                  7                   8                 9               10
    appointments = db.session.execute(db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name, Instructors.Id, Appointments.Product). \
                                order_by(Appointments.Date). \
                                filter(Appointments.User == user). \
                                join(Users,       Appointments.User    == Users.Id). \
                                join(Instructors, Appointments.Staff   == Instructors.Id). \
                                join(Products,    Appointments.Product == Products.Id) )

    instructors = db.session.execute(db.select(Instructors.Id, Instructors.User, Instructors.Name).where(Instructors.Active).order_by(Instructors.Name))

    # pass the option list via a string... there is some room for improvement ;-)
    cInstructors = ""
    cOptions     = ""
    filtered2 = [] # necessary because list could be for/endfor once.
    for i in instructors:
        filtered2.append(i)
        cInstructors = cInstructors + "<option value='" + i.Name + "'>" + i.Name + "</option>"
        cOptions = cOptions + "<option value='" + i.Name + "'>" + i.Name + "</option>" + '|'

    # filter on product.Id (solution for multiple filters not found)
    filtered = []
    for a in appointments:
        if a [10] == product:
            filtered.append(a)

    if form.validate_on_submit():

        print ('=================================================================')
        
        for a in filtered:
            cDate = chr(34) + 'date' + str(a [0]) + chr(34)
            cDateValue = request.form.get(eval(cDate))
            cTime = chr(34) + 'time' + str(a [0]) + chr(34)
            cTimeValue = request.form.get(eval(cTime))
            print ('.')
            print ('#### cDate: ', cDate , cDateValue)
            print ('#### cTime: ', cTime , cTimeValue)
            cInstructor = chr(34) + 'instructor' + str(a [0]) + chr(34)
            cInstructorValue = request.form.get(eval(cInstructor))
            print ('#### cInstructor: ', cInstructor , cInstructorValue)
            print ('.')

            nInstructor = 0
            for i in filtered2:
                if i.Name == cInstructorValue:
                    nInstructor = i.Id

            print ('.')
            print ('#### nInstructor: ', nInstructor)
            print ('.')

            appointment = db.session.execute(db.select(Appointments).filter_by(Id=a [0])).scalar_one()
            dDate = datetime.datetime(int(cDateValue[0:4]), int(cDateValue[5:7]), int(cDateValue[8:10]), int(cTimeValue[0:2]), int(cTimeValue[3:5]))
            appointment.Date = dDate
            appointment.Staff = nInstructor
            db.session.commit()
        print ('=================================================================')

        lRBAC = get_rbac(request.url_rule.endpoint)

        users = Users.query.all()

        return render_template('users.html', users = users, lRBAC = lRBAC)

    instructors = db.session.execute(db.select(Instructors.Id, Instructors.User, Instructors.Name).where(Instructors.Active).order_by(Instructors.Name))

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('usersproductform.html', form=form, instructors=filtered2, appointments=filtered, lRBAC=lRBAC, cInstructors=cInstructors, cOptions=cOptions)

#------------------------------------------------------------------------------------------

##     ##  ######  ######## ########   ######  ######## ########  #### ######## 
##     ## ##    ## ##       ##     ## ##    ## ##       ##     ##  ##     ##    
##     ## ##       ##       ##     ## ##       ##       ##     ##  ##     ##    
##     ##  ######  ######   ########   ######  ######   ##     ##  ##     ##    
##     ##       ## ##       ##   ##         ## ##       ##     ##  ##     ##    
##     ## ##    ## ##       ##    ##  ##    ## ##       ##     ##  ##     ##    
 #######   ######  ######## ##     ##  ######  ######## ########  ####    ##    


@app.route('/userseditform2/<int:id>/<string:cFrom>', methods=['GET', 'POST'])
def usersedit2(id, cFrom):

    if current_user.is_anonymous:
        return (no_access_text())

    form = UsersEditForm2()

    user = Users.query.filter_by(Id = int(id)).first()

    listStatus = ['new', 'student', 'staff', 'instructor']

    lRBAC = get_rbac(request.url_rule.endpoint)
    if 'admin' in lRBAC [1]:
        listStatus.append('admin')

    lInstructorBefore = False
    cRolesBefore      = user.Status
    cStatusOld        = cRolesBefore

    if "instructor" in cRolesBefore:
        lInstructorBefore = True

    if form.validate_on_submit():

        newpassword = ""
        lRBAC = get_rbac(request.url_rule.endpoint)
        if "admin" in lRBAC [1]:
            newpassword = request.form["password"]

        pw_hash = ""
        if len(newpassword) > 0: 
          pw_hash = bcrypt.generate_password_hash(newpassword).decode('utf-8')

        x = db.session.query(Users).get(id)
        x.Firstname    = request.form["firstname"]
        x.Lastname     = request.form["lastname"]
        x.Phone        = request.form["phone"]
        x.Emailaddress = request.form["emailaddress"]
        if len(newpassword) > 0: 
            x.Passwordhash = pw_hash
              
        # process roles
        cUserStatus = ''
        nC = 0
        for l in listStatus:
            value = request.form.get(eval('listStatus [nC]'))
            if value:
                cUserStatus = cUserStatus + listStatus [nC] + ' '
            nC = nC + 1

        # x.Status       = cUserStatus
        db.session.commit()

        lInstructorAfter = False
        cRolesAfter = cUserStatus
        cStatusNew = cRolesAfter

        print('#### retrieving status')
        x = db.session.query(Users).get(x.Id)
        print('#### ', x.Username, ' ', x.Status)
        print('#### cUserStatus: ', cUserStatus)

        cTempStatus = cStatusOld

        if "instructor" in cRolesAfter:
            lInstructorAfter = True

            #x = db.session.query(Users).get(x.Id)
            #if not lInstructorAfter:
            #    cTempStatus = cUserStatus.replace('instructor ','')
            #print('#### cTempStatus: ', cTempStatus)
            #x.Status = cTempStatus
            #db.session.commit() 
        else:
            lInstructorAfter = False

            #x = db.session.query(Users).get(x.Id)
            #x.Status = cUserStatus
            #db.session.commit() 
            #print('#### saving status')
            #x = db.session.query(Users).get(x.Id)
            #print('#### ', x.Username, ' ', x.Status)
            #print('#### cUserStatus: ', cUserStatus)

        print("#### ---------------------------------------------------------------")
        print("#### before ", lInstructorBefore, ' ', cStatusOld)
        print("#### after  ", lInstructorAfter, ' ', cStatusNew)

        if lInstructorBefore and lInstructorAfter:
            x = db.session.query(Users).get(x.Id)
            x.Status = cStatusNew
            db.session.commit() 

        if lInstructorBefore and not lInstructorAfter:
            #print ('#### removing instructor from table instructors')

            print('------------------------------------------------------------------------------')
            print('')
            print('#### x.Id:                                   ', x.Id, ' (User.Id)')
            dbquery = 'db.session.execute(db.select(Instructors).filter_by(User = x.Id)).scalar_one_or_none()'
            print('#### ', datetime.datetime.today(), ' dbquery: ', dbquery)
            ## instructor = eval(dbquery)
            instructor = db.session.execute(db.select(Instructors.Id, Instructors.User, Instructors.Name).where(Instructors.User == x.Id)).all()
            nStaff = 0
            for i in instructor:
                print('#### instructor [0]', i [0])
                print('#### instructor [1]', i [1])
                print('#### instructor [2]', i [2])
                nStaffUser = i [0]
                nStaffId   = i [1]
                #print('#### instructor.Name', instructor.Name)
            print('#### nStaffUser: ', nStaffUser)
            print('#### nStaffId:   ', nStaffId)
            instructor2 = []
            for i in instructor:
                instructor2.append(i)
            for i in instructor2:
                print('#### instructor2 [0]', instructor2 [0])
                #print('#### instructor2.Name', instructor2.Name)
            print('#### type(instructor):   all   ', type(instructor))
            print('#### len(instructor):    al    ', len(instructor))
            print('#### type(instructor2):  all   ', type(instructor2))
            print('#### len(instructor2):   all   ', len(instructor2))
            print('')
            print('')

            # instructor = db.session.execute(db.select(Instructors.Id, Instructors.User, Instructors.Name).where(Instructors.User == x.Id)).all()

            print('nStaffId:   ', nStaffId)
            print('nStaffUser: ', nStaffUser)

            current_datetime = datetime.datetime.now()
            nYearFrom  = current_datetime.year
            nMonthFrom = current_datetime.month
            nDayFrom   = current_datetime.day

            dbquery = 'db.session.execute(db.select(Appointments.Id, Appointments.User, Appointments.Product, Appointments.Part, Appointments.Date, Appointments.Notes, Appointments.Staff).'
            dbquery = dbquery + 'where(and_(Appointments.Staff == nStaffUser),'
            dbquery = dbquery + '(Appointments.Date >= datetime.datetime(nYearFrom, nMonthFrom, nDayFrom) ))).all()'

            print('#### ', datetime.datetime.today(), ' dbquery: ', dbquery)

            appointments = eval(dbquery)

            # appointments = db.session.execute(db.select(Appointments.Id, Appointments.User, Appointments.Product, Appointments.Part, Appointments.Date, Appointments.Notes, Appointments.Staff).where(Appointments.Staff == nStaffId )).all()

            print('')
            print('#### type(appointments):', type(appointments))
            print('#### len(appointments): ', len(appointments))

            for a in appointments:
                print ('#### a: ', a[0], a[1], a[2], a[3],a[4],a[5])

            print('------------------------------------------------------------------------------')
            
            if appointments is None:
                print('#### Appointments is None.')

            nStaff = 0
            appointments2 = [] 
            for a in appointments:
                print('#### ', a [0], a [1], a[2], a[3], a[4], a[5], a[6])
                appointments2.append(a)

            if appointments2 is None:
                print('#### Appointments2 is None.')

            print('')
            print('------------------------------------------------------------------------------')
            print('')

            for a in appointments2:
                print('#### ', a [0], a [1], a[2], a[3], a[4], a[5], a[6])
                nStaff = a [6]

            print('#### nStaff:  ', nStaff)
            print('')
            print('------------------------------------------------------------------------------')
            print('')

            #if appointments is not None:
            if nStaff > 0:
                print('#### appointments found for instructor')
                lRBAC = get_rbac(request.url_rule.endpoint)        
                return redirect(url_for('instructorsinfo', id = nStaffId ))

            print ('#### saving new status')
            x = db.session.query(Users).get(x.Id)
            x.Status       = cUserStatus
            db.session.commit()
            x = db.session.query(Users).get(x.Id)
            print('#### ', x.Username, ' ', x.Status)

            print('')
            print('------------------------------------------------------------------------------')
            print('')
            dbquery = 'db.session.execute(db.select(Instructors).filter_by(User = x.Id)).scalar_one_or_none()'
            print('#### ', datetime.datetime.today(), ' dbquery: ', dbquery)
            instructor = eval(dbquery)

            print('')
            print('------------------------------------------------------------------------------')
            print('')
            #print ("#### instructor.Name: ", instructor.Name)
            #db.session.delete(instructor)
            instructor.Active = False
            db.session.commit()

        #lRBAC = get_rbac(request.url_rule.endpoint) 

        if not lInstructorBefore and lInstructorAfter:

            instructor = db.session.execute(db.select(Instructors).filter_by(User = x.Id)).scalar_one_or_none()

            print('####')
            print('#### type(instructor): ', type(instructor))

            if instructor is None:

                # adding new instructor

                print ('#### adding instructor to table instructors')

                instructor_to_create = Instructors(User   = x.Id,
                                                   Name   = x.Firstname + " " + x.Lastname, 
                                                   Active = True)
                db.session.add(instructor_to_create)
                db.session.commit()

            else:

                # re-instating instructor status

                print ('#### altering instructor in table instructors')
                print ("#### instructor.Name: ", instructor.Name)
                # db.session.delete(instructor)
                instructor.Active = True
                db.session.commit()

            print ('#### saving new status')
            x = db.session.query(Users).get(x.Id)
            x.Status       = cUserStatus
            db.session.commit()
            x = db.session.query(Users).get(x.Id)
            print('#### ', x.Username, ' ', x.Status)

        print('####')

        print("#### ---------------------------------------------------------------")

        if cFrom == 'instructors':
            return redirect(url_for('instructors'))

        return redirect(url_for('users'))
    
    if form.errors != {}: # no errors?
        for err_msg in form.errors.values():
            flash(f'error: {err_msg}', category = 'danger')

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('userseditform2.html', form = form, user = user, listStatus = listStatus , lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

##     ##  ######  ######## ########   ######  ########  ########  ######   ####  ######  ######## ######## ########  
##     ## ##    ## ##       ##     ## ##    ## ##     ## ##       ##    ##   ##  ##    ##    ##    ##       ##     ## 
##     ## ##       ##       ##     ## ##       ##     ## ##       ##         ##  ##          ##    ##       ##     ## 
##     ##  ######  ######   ########   ######  ########  ######   ##   ####  ##   ######     ##    ######   ########  
##     ##       ## ##       ##   ##         ## ##   ##   ##       ##    ##   ##        ##    ##    ##       ##   ##   
##     ## ##    ## ##       ##    ##  ##    ## ##    ##  ##       ##    ##   ##  ##    ##    ##    ##       ##    ##  
 #######   ######  ######## ##     ##  ######  ##     ## ########  ######   ####  ######     ##    ######## ##     ## 

@app.route('/usersregisterform', methods=['GET' ,'POST'])
def usersregister():

    form = UsersRegisterForm()

    if form.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(form.password1.data).decode('utf-8')

        user_to_create = Users(Username     = form.username.data,
                               Firstname    = form.firstname.data,
                               Lastname     = form.lastname.data,
                               Phone        = form.phone.data,
                               Emailaddress = form.emailaddress.data,
                               Passwordhash = pw_hash,
                               Status       = "new")
        
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('users'))
   
    if form.errors != {}: # no errors?
        for err_msg in form.errors.values():
            flash(f'error: {err_msg}', category = 'danger')

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('usersregisterform.html', form=form , lRBAC = lRBAC)

# ---------------------------------------------------------------------------------------


##     ##  ######  ######## ########   ######  #### ##    ## ########  #######  
##     ## ##    ## ##       ##     ## ##    ##  ##  ###   ## ##       ##     ## 
##     ## ##       ##       ##     ## ##        ##  ####  ## ##       ##     ## 
##     ##  ######  ######   ########   ######   ##  ## ## ## ######   ##     ## 
##     ##       ## ##       ##   ##         ##  ##  ##  #### ##       ##     ## 
##     ## ##    ## ##       ##    ##  ##    ##  ##  ##   ### ##       ##     ## 
 #######   ######  ######## ##     ##  ######  #### ##    ## ##        #######  


@app.route('/usersinfo/<id>', methods = ['GET', 'POST'])
def usersinfo(id):

    if current_user.is_anonymous:
        return (no_access_text())

    form = UsersInfoForm(id)

    #                                            0                1                  2                3               4                     5                  5                  7                   8  
    appointments = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name). \
                                order_by(Appointments.Date). \
                                where(Appointments.User == id). \
                                select_from(Appointments). \
                                join(Users, Appointments.User == Users.Id). \
                                join(Instructors, Appointments.Staff == Instructors.Id). \
                                join(Products, Appointments.Product == Products.Id) )
    user         = db.session.execute(db.select(Users).filter_by(Id=id)).scalar_one()
    products     = db.session.execute(db.select(Products)).scalars()

    if form.validate_on_submit():

        print ("----------------------------------------------------------------")
        #t = datetime.datetime.now()
        #cTime = t.strftime("%d-%m-%Y %H:%M:%S")
        cDateToday = datetime.datetime.today()
        cDate = cDateToday.strftime("%d-%b-%Y")

        x = db.session.query(Users).get(id)
        if x.Info:
            cInfo = x.Info
        else:
            cInfo = ""

        cStatus = ''
        for p in products:
            value = request.form.get(eval('p.Productname'))
            if value:
                cStatus = cStatus + cDate + ' ' + p.Productname + '|'
                        
                parts = p.Parts

                #20240829 - MvW - adding '\' if necessary...
                if not parts[len(parts)-1] == '|':
                    parts = parts + '|'

                part = ""
                t = 0
                cDateFrom = request.form.get('datefrom')
                dt2 = datetime.datetime.strptime(cDateFrom, '%Y-%m-%d')
                for b in parts:
                    if b == "|":

                        nDateTo  = dt2 + timedelta(days=t)
                        nYearTo  = nDateTo.year  # nYearTo  = nDateTo.year
                        nMonthTo = nDateTo.month # nMonthTo = nDateTo.month
                        nDayTo   = nDateTo.day   # nDateTo.day + t

                        date0 = datetime.datetime.combine(datetime.date(nYearTo, nMonthTo, nDayTo), datetime.time(20,00))
                        A0 = Appointments(User = id, Product = p.Id, Part = part, Date = date0, Notes = "[" + cDate + ']', Staff = 1)
                        db.session.add(A0)
                        db.session.commit()
                        part = ""
                        t = t + 7
                    else:
                        part = part + b

        x.Info       = cInfo + cStatus
        db.session.commit()
        print ("----------------------------------------------------------------")

        #                                            0                1                  2                3               4                     5                  5                  7                   8  
        appointments = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name). \
                                order_by(Appointments.Date). \
                                where(Appointments.User == id). \
                                select_from(Appointments). \
                                join(Users, Appointments.User == Users.Id). \
                                join(Instructors, Appointments.Staff == Instructors.Id). \
                                join(Products, Appointments.Product == Products.Id) )
        products = db.session.execute(db.select(Products)).scalars()


        lRBAC = get_rbac(request.url_rule.endpoint) 

        return render_template('usersinfo.html', form = form, user = user, appointments = appointments, products = products, lRBAC = lRBAC)
    
    cDateToday = datetime.datetime.today()

    lRBAC = get_rbac(request.url_rule.endpoint) 

    return render_template('usersinfo.html', form = form, user = user, appointments = appointments, products = products, cDateToday = cDateToday, lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

##     ##  ######  ######## ########  ########  ######## ##       ######## ######## ######## 
##     ## ##    ## ##       ##     ## ##     ## ##       ##       ##          ##    ##       
##     ## ##       ##       ##     ## ##     ## ##       ##       ##          ##    ##       
##     ##  ######  ######   ########  ##     ## ######   ##       ######      ##    ######   
##     ##       ## ##       ##   ##   ##     ## ##       ##       ##          ##    ##       
##     ## ##    ## ##       ##    ##  ##     ## ##       ##       ##          ##    ##       
 #######   ######  ######## ##     ## ########  ######## ######## ########    ##    ######## 

@app.route('/userdelete/<id>')
def userdelete(id):

    if current_user.is_anonymous:
        return (no_access_text())

    user = db.session.execute(db.select(Users).filter_by(Id=id)).scalar_one()
    cUsername = user.Username
    db.session.delete(user)
    db.session.commit()

    print('#### cUsername:             ', cUsername)
    print('#### current_user.Username: ', current_user.Username)

    if cUsername == current_user.Username:
        return (url_for('logout'))

    lRBAC = get_rbac(request.url_rule.endpoint) 

    return render_template(url_for('users'), lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

# HTML ########  ##    ##  #######    ######   #######   ##########
       ##        ##    ##  ##    ##  ##    ##  ##    ##      ##
       ##         ##  ##   ##    ##  ##    ##  ##    ##      ##
       ######      ####    #######   ##    ##  #######       ##
       ##         ##  ##   ##        ##    ##  ##  ##        ##
       ##        ##    ##  ##        ##    ##  ##   ##       ##
       ########  ##    ##  ##         ######   ##    ##      ##

@app.route('/htmlexport/')
def htmlexport():

    from calendar import monthrange

    cWhiteSpace = "&nbsp;&nbsp;&nbsp;"

    nStartTime = datetime.datetime.today()

    if not os.path.exists('Exports'):
        os.makedirs('Exports') 

    cDateToday = datetime.datetime.today()
    cDate2     = cDateToday.strftime("%d-%b-%Y")
    cDate4     = cDateToday.strftime("%Y%m%d")
    cDate5     = cDateToday.strftime("%d-%m-%Y")
    cTime      = cDateToday.strftime("%H%M")
    cTime2     = cDateToday.strftime("%H:%M")

    dDateFrom  = datetime.date.today() - timedelta(days=14)
    dDateTo    = datetime.date.today() + timedelta(92)
    dDateTo    = datetime.date.today() + timedelta(int(4 * 30.5))

    nYearFrom  = dDateFrom.year
    nMonthFrom = dDateFrom.month  
    nYearTo    = dDateTo.year
    nMonthTo   = dDateTo.month

    print('nYearFrom:  ', nYearFrom)
    print('nMonthFrom: ', nMonthFrom)
    print('nYearTo:    ', nYearTo)
    print('nMonthTo:   ', nMonthTo)
    
    if nMonthTo < nMonthFrom:
        nMonthTo = nMonthTo + 12

    cFolderNameHtml = '../divescheduling_' + cDate4 + '_' + cTime + '/'
    cFolderNameOS   = 'c:/data/python/divescheduling/Exports/divescheduling_' + cDate4 + '_' + cTime + '/'

    if not os.path.exists(cFolderNameOS):
        os.makedirs(cFolderNameOS) 

    print("--[exporthtml]--------------------------------------------------------------------")

    lMonthNames = ['','January','February','March','April','May','June','July','August','September','October','November','December']
    lDayNames   = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    cStyle = '<style>'
    cStyle = cStyle + 'td { text-align:left; vertical-align:top; padding-left:5px;padding-right:5px;padding-bottom:5px;padding-top:5px;'
    cStyle = cStyle + 'font-family:verdana; }'
    cStyle = cStyle + 'table { border-collapse: collapse; }'
    cStyle = cStyle + 'a, p, h3 {font-family:verdana;}'
    cStyle = cStyle + 'table, th, td { border: 1px solid};'
    cStyle = cStyle + '</style>'
    cStyle = cStyle + ''

    cHtmlCal = '<html>' + cStyle + '<body>[cInstructorsMenu]<br>'

    aInstructor = []
    aHtmlFiles  = []
    nInstructor = 0

    # start instructorsmenu with link to calendar
    cInstructorsMenu = "<a href=" + cFolderNameHtml + "calendar_" + cDate4 + "_" + cTime + ".html>Calendar</a>"

    # 'prefill' for week height
    cWeekLines = "<br><br><br><br><br><br>"

    nYear = nYearFrom

    # repair an unknown issue with same years in range
    nAddYear = 0
    if nYearFrom == nYearTo:
        nAddYear = 1

    aStudentHtml = []
    cStudentMenu = ''
    nStudent     = 0

    for nYears in range(nYearFrom, nYearTo + nAddYear):

        print('processing year: ', nYear)

        for nMonths in range(nMonthFrom, nMonthTo):

            print('nMonths: ', nMonths)

            if nMonths > 12:
                nMonth = nMonths - 12
                nYear = nYearFrom + 1
            else:
                nMonth = nMonths

            if True:
                print('processing month: ', nMonth)

                cHtmlCal = cHtmlCal + "<table><tr><td colspan=8 style='text-align: center;'><h3>" + lMonthNames [nMonth] + "</h3></td></tr>"
                cHtmlCal = cHtmlCal + '<tr><td><b>week' + cWhiteSpace + '</b></td>'

                # table header with daynames
                for n in lDayNames:
                    cHtmlCal = cHtmlCal + '<td><b>' + n + cWhiteSpace + '</b></td>'

                cHtmlCal = cHtmlCal + '</tr>'

                lResult = monthrange(nYear, nMonth)

                nFirstDay = lResult [0]
                nLastDay  = lResult [1]

                # weeknumber
                nDay = 1
                cWeekNumber = datetime.date(int(nYear), int(nMonth), int(nDay)).strftime('%V')
                cWeekNumber = str(int(cWeekNumber) - 1)
                cHtmlCal = cHtmlCal + '<tr><td>' + str(cWeekNumber) + cWeekLines + '</td>'

                cWhiteSpace2 = cWhiteSpace + cWhiteSpace + cWhiteSpace + cWhiteSpace + cWhiteSpace + cWhiteSpace + cWhiteSpace + cWhiteSpace + cWhiteSpace + cWhiteSpace

                # add before cells to table
                for nDay in range(nFirstDay):
                    cHtmlCal = cHtmlCal + '<td>' + cWhiteSpace2 + '</td>'

                for nDays in range(nLastDay):
                    cHtmlDat = ''

                    # correct 0-based range
                    nDay = nDays + 1

                    #print('processing: ', nYear, nMonth, nDay)

                    cProducts = ''
                    nDayOfWeek = (nDay + nFirstDay - 1) % 7
                    cDate = str(nYear) + '-' + str(nMonth).rjust(2,'0') + '-' + str(nDay + 1).rjust(2, '0')
                    cHtmlCal = cHtmlCal + '<td>' + str(nDay) + '<br>'
                    
                    dDate = datetime.date(nYear, nMonth, nDay)
                    #                                           0                1                  2                3               4                     5                  6                  7                   8                 9               10
                    appointments = db.session.execute(db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name, Instructors.Id, Appointments.Product). \
                                   where(func.date(Appointments.Date) == dDate). \
                                   order_by(Appointments.Product). \
                                   join(Users,       Appointments.User    == Users.Id). \
                                   join(Instructors, Appointments.Staff   == Instructors.Id). \
                                   join(Products,    Appointments.Product == Products.Id) )

                    cOldProduct = ''

                    cHtmlIns = ''

                    cDate3 = str(nYear) + str(nMonth).rjust(2,'0') + str(nDay + 1).rjust(2, '0')

                    cEmptyTR = ''

                    cAddHtmlHeader = "<tr><td><b>date</b></td><td><b>product</b></td><td><b>part</b></td><td><b>student</b></td><td><b>instructor</b></td></tr>"

                    for a in appointments:
 
                        # date html
                        cHtmlDat = cHtmlDat + '<tr><td>dat-' + a [6].strftime('%H.%M') + cWhiteSpace  + '</td><td>' + a [4] + cWhiteSpace + '</td><td>' + a [5] + cWhiteSpace + '</td><td>'  + a [2] + ' ' + a [3] + cWhiteSpace + '</td><td>' + a [8] + cWhiteSpace + '</td>' + chr(13) + chr(10)

                        #---------------------------------------
                        # process student info

                        nFound = 0
                        nCounter = 0
                        for i in aStudentHtml:
                            if i [1] == a [1]:
                                nFound = nCounter
                            nCounter = nCounter + 1

                        # html student
                        cAddHtmlLine = "<tr><td>stu-" + a [6].strftime("%d-%m-%Y %H:%M") + cWhiteSpace + "</td><td>" + a [4] + cWhiteSpace + "</td><td>" + a [5] + cWhiteSpace + "</td><td>" + a [2] + " " + a [3] + cWhiteSpace + "</td><td>" + a [8] + cWhiteSpace + "</td></tr>"

                        if nFound == 0:
 
                            nStudent = nStudent + 1
                            aStudentHtml.append([nStudent, a [1], a [2] + ' ' + a [3], cAddHtmlHeader + cAddHtmlLine])

                            cStudentName = a [2] + " " + a [3]
                            if not cStudentName in cStudentMenu:
                                cStudentMenu = cStudentMenu + ";<a href=" + cFolderNameHtml + "calendar_st_" + cStudentName.replace(' ', '_') + ".html>" + cStudentName + "</a>"

                        else:
 
                            aStudentHtml [nFound][3] = aStudentHtml [nFound][3] + cAddHtmlLine

                        #---------------------------------------
                        # process instructor info
                        nFound = 0
                        nCounter = 0
                        for i in aInstructor:
                            if i [1] == a [9]:
                                nFound = nCounter
                            nCounter = nCounter + 1

                        # html instructor
                        cAddHtmlIns = "<tr><td>ins-" + a [6].strftime("%d-%m-%Y %H:%M") + cWhiteSpace + "</td><td>" + a [4] + cWhiteSpace + "</td><td>" + a [5] + cWhiteSpace + "</td><td>" + a [2] + " " + a [3] + cWhiteSpace + "</td><td>" + a [8] + cWhiteSpace + "</td></tr>"

                        if nFound == 0:
 
                            nInstructor = nInstructor + 1
                            # print('instructor ' + a [8] + ' not found')

                            aInstructor.append([nInstructor, a [9], a [8], cAddHtmlHeader + cAddHtmlIns])

                            if not a [8] in cInstructorsMenu:
                                cInstructorsMenu = cInstructorsMenu + ";<a href=" + cFolderNameHtml + "calendar_in_" + a [8].replace(' ', '_') + ".html>" + a [8] + "</a>"

                            cEmptyTR = cEmptyTR + '|'+ str(a[9]) + '|'

                        else:
 
                            print('instructor ', a [8],' found: ', nFound)
                            # print('before: ', aInstructor [nFound][2], aInstructor [nFound][3])
                            aInstructor [nFound][3] = aInstructor [nFound][3] + cAddHtmlIns
                            # print('after:  ', aInstructor [nFound][2], aInstructor [nFound][3])

                            cEmptyTR = cEmptyTR + '|'+ str(a[9]) + '|'
                        
                        #---------------------------------------

                        if not a [4] in cProducts:
                            cHtmlCal = cHtmlCal + '<a href=' + cFolderNameHtml + 'calendar_da_' + cDate3 + '.html>' + a [4] + '</a><br>'
                            cProducts = cProducts + a [4] + '|'
                        
                    #### for a in appointments:

                    # add empty row in instructor table
                    for i in aInstructor:
                        if '|' + str(i [1]) + '|' in cEmptyTR: 
                            i [3] = i [3] + "<tr><td colspan = 4>&nbsp;</td></tr>"
                    
                    # to force a default cell width
                    cHtmlCal = cHtmlCal + cWhiteSpace2

                    # end of week
                    if nDayOfWeek == 6:
                        cWhiteSpace2 = ''
                        cHtmlCal = cHtmlCal + '</tr>'
                        if nDay != nLastDay:
                            # weeknumber
                            print('#### ', nYear, nMonth, nDay)
                            cHtmlCal = cHtmlCal + '<tr><td>' + str(datetime.date(int(nYear), int(nMonth), int(nDay)).strftime('%V')) + cWeekLines + '</td>'

                    if len(cHtmlDat) > 0:
                        # date html
                        cHtmlDat2 = '<html>' + cStyle + '<body>[cInstructorsMenu]<br><br><table>'

                        cWeekdayName = lDayNames[datetime.date(nYear, nMonth, nDay).weekday()]

                        cHtmlDat2 = cHtmlDat2 + "<tr><td colspan=5 style='text-align: center;'><h3>" + str(nDay) + " " + lMonthNames[nMonth] + " " + str(nYear) + " - " + cWeekdayName + "<h3></td></tr>"
                        cHtmlDat2 = cHtmlDat2 + '<tr><td><b>time</b><td><b>product</b><td><b>part</b><td><b>student</b><td><b>instructor</b></td><tr>'
                        cHtmlDat2 = cHtmlDat2 + cHtmlDat
                        cHtmlDat2 = cHtmlDat2 + '</table>'

                        cFileName = cFolderNameOS + '/calendar_da_' + cDate3 + '.html'

                        aHtmlFiles.append([cFileName, cHtmlDat2])
                
                #### for nDay in range(nLastDay):

                # after cells
                nCounter = 1    
                for nDay in range(nDayOfWeek + 1, 7):
                    #print('----'.ljust(17), end='')
                    cHtmlCal = cHtmlCal + '<td></td>'
                    nCounter = nCounter + 1

                cHtmlCal = cHtmlCal + '</tr></table><br><br>'

        #### for nMonth in range(12):

    #### for nYear in range(nYearFrom, nYearTo):

    #------------------------------------------------------------------------------
    # split students to list
    newList = list(cStudentMenu.split(";"))

    # sort list
    sortedList = sorted(newList)

    print('')
 
    cNewStudentMenu = ''
 
    for n in sortedList:
        print ('n: ', n)
        cNewStudentMenu = cNewStudentMenu + ' - ' + n

    cStudentMenu = cNewStudentMenu + '<br>'

    #------------------------------------------------------------------------------
    # split instructors to list
    newList = list(cInstructorsMenu.split(";"))

    # sort list
    sortedList = sorted(newList)
 
    cNewInstructorsMenu = ''
 
    for n in sortedList:
        print ('n: ', n)
        cNewInstructorsMenu = cNewInstructorsMenu + ' - ' + n

    #------------------------------------------------------------------------------

    cInstructorsMenu = cNewInstructorsMenu + '<br>'

    for i in aStudentHtml:

        # replace spaces in instructorname with underscores for filename
        cInsName = i [2].replace(' ', '_')

        cFileName = cFolderNameOS + '/calendar_st_' + cInsName + '.html'
        cHtmlIns = '<html>' + cStyle + "<body>[cInstructorsMenu]<br><br><table><tr><td colspan=5 style='text-align: center;'><h3>" + i [2] + "</h3></td></tr>" + i [3] + "</table>"
        aHtmlFiles.append([cFileName, cHtmlIns])

    for i in aInstructor:

        # replace spaces in instructorname with underscores for filename
        cInsName = i [2].replace(' ', '_')

        cFileName = cFolderNameOS + '/calendar_in_' + cInsName + '.html'
        cHtmlIns = '<html>' + cStyle + "<body>[cInstructorsMenu]<br><br><table><tr><td colspan=5 style='text-align: center;'><h3>" + i [2] + "</h3></td></tr>" + i [3] + "</table>"
        aHtmlFiles.append([cFileName, cHtmlIns])

    # add Calendar html to html list
    cFileName = cFolderNameOS + '/calendar_' + cDate4 + '_' + cTime + '.html'
    aHtmlFiles.append([cFileName, cHtmlCal])

    cHtmlCalendar = cHtmlCal

    # create html files
    for h in aHtmlFiles:

        # replace tag with links to instructor html files
        cHtml = h [1].replace('[cInstructorsMenu]', cInstructorsMenu + '<br>' + cStudentMenu + '<br>') 

        # remove last empty table row
        cHtml = cHtml.replace('</tr><tr><td colspan = 4>&nbsp;</td></tr></table>', '</tr></table>') 

        # add footer
        cHtml = cHtml + "<br><br><p style='font-size: 12px;'>powered by divescheduling. created:" + cDate5 + " " + cTime2 + "</p></body></html>"

        f = open(h [0], 'w')
        f.write(cHtml)
        f.close()

    nFinishTime = datetime.datetime.today()

    print()
    print('export start: ', nStartTime, ' export finish: ', nFinishTime)

    lRBAC = get_rbac(request.url_rule.endpoint) 

    return render_template('test.html', lRBAC = lRBAC, cHtml = cHtmlCalendar)
