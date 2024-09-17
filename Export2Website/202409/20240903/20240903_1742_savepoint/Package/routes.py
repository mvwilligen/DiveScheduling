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
from Package.forms import AppointmentsEditForm, LoginForm, ProductsEditForm, ProductsUsersForm, ProductsNewForm, UsersEditForm, UsersInfoForm, RegisterForm, RegisterForm2, UsersProductForm2, AppointmentsDateForm2

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash


from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.init_app(app)  
@login_manager.user_loader
def load_user(user_id):
  return Users.query.get(user_id)

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

import sqlalchemy as sa
from sqlalchemy import func, and_

import datetime
from datetime import timedelta

from Package.functions import get_rbac, string2safe, no_access_text

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

    nDateTo  = datetime.date.today() + timedelta(days=29)
    nYearTo  = nDateTo.year
    nMonthTo = nDateTo.month
    nDayTo   = nDateTo.day

    #                                            0                1                  2                3               4                     5                  6                  7                 8 
    appointments = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Instructors.Name, Appointments.Staff). \
                                order_by(Appointments.Date). \
                                where(and_(func.DATE(Appointments.Date) >= datetime.datetime(nYearFrom, nMonthFrom, nDayFrom), \
                                           func.DATE(Appointments.Date) <= datetime.datetime(nYearTo,   nMonthTo,   nDayTo))). \
                                select_from(Appointments). \
                                join(Users, Appointments.User        == Users.Id). \
                                join(Instructors, Appointments.Staff == Instructors.Id). \
                                join(Products, Appointments.Product  == Products.Id) )

    lRBAC = get_rbac()

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

    lRBAC = get_rbac()

    return render_template('appointments.html', appointments = appointments, lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

@app.route('/appointmentsdelete/<id>/')
def appointmentsdelete(id):

    if current_user.is_anonymous:
        return (no_access_text())

    appointment = db.session.execute(db.select(Appointments).filter_by(Id=id)).scalar_one()
    db.session.delete(appointment)
    db.session.commit()
    #                                                   0             1                2                 3                 4                5                       5               7                 8
    appointments = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name). \
                                order_by(Appointments.Date). \
                                select_from(Appointments). \
                                join(Users, Appointments.User == Users.Id). \
                                join(Instructors, Appointments.Staff == Instructors.Id). \
                                join(Products, Appointments.Product == Products.Id) )
    
    lRBAC = get_rbac()

    return render_template('appointments.html', appointments = appointments, lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

@app.route('/appointmentsassign/<id>/')
def appointmentsassign(id):

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
    
    lRBAC = get_rbac()

    return render_template('appointments.html', appointments = appointments, lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

@app.route('/appointmentsunassign/<id>/')
def appointmentsunassign(id):

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
    
    lRBAC = get_rbac()

    return render_template('appointments.html', appointments = appointments , lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

@app.route('/appointmentsedit/<id>/', methods=['GET', 'POST'])
def appointmentsedit(id):

    if current_user.is_anonymous:
        return (no_access_text())

    form = AppointmentsEditForm(id)

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

        return redirect(url_for('appointments'))

    lRBAC = get_rbac()

    return render_template('appointmentsedit.html', form=form, appointment=appointment2, cDebug=cDebug, instructors=instructors, lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

@app.route('/appointmentsdateform2/<text>/', methods=['GET', 'POST'])
def appointmentsdate2(text):

    if current_user.is_anonymous:
        return (no_access_text())

    form = AppointmentsDateForm2(text)

    # appointment = db.session.execute(db.select(Appointments).filter_by(Id=id)).scalar_one()
    #
    #user    = appointment.User
    #product = appointment.Product

    # http://127.0.0.1:5000/appointmentsdateform2/02-09-2024/
    cDate = text [6:10] + '_' + text [3:4] + "_" + text [0:1]
    print ('#### -----------------------------------------------------------------------')
    print ('#### text: ', text)
    print ('#### cDate: ', cDate)
    dDate = datetime.date(int(text [6:10]), int(text [3:5]), int(text [0:2]))
    print ('#### dDate: ', dDate)
    print ('#### -----------------------------------------------------------------------')

#    #                                           0                1                  2                3               4                     5                  6                  7                   8                 9               10
    appointments = db.session.execute(db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name, Instructors.Id, Appointments.Product). \
                                order_by(Appointments.Date). \
                                filter(Appointments.Date == dDate). \
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
        print()
        print ('=================================================================')

        lRBAC = get_rbac()

        users = Users.query.all()

        return render_template('users.html', users = users, lRBAC = lRBAC)

    instructors = db.session.execute(db.select(Instructors.Id, Instructors.User, Instructors.Name).where(Instructors.Active).order_by(Instructors.Name))

    lRBAC = get_rbac()

    return render_template('usersproductform.html', form=form, instructors=filtered2, appointments=filtered, lRBAC=lRBAC, cInstructors=cInstructors, cOptions=cOptions)

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
                                join(Users,       Instructors.User    == Users.Id) )
    
    lRBAC = get_rbac()

    return render_template('instructors.html', instructors = instructors , lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

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

    lRBAC = get_rbac()

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

                return redirect(url_for('appointments'))
        
    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    lRBAC = []
    return redirect(url_for('appointments'))

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

    lRBAC = get_rbac()

    return render_template('products.html', products=products , lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

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

    lRBAC = get_rbac()

    return render_template('productsedit.html', form=form, product=product , lRBAC = lRBAC)
#------------------------------------------------------------------------------------------

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

    lRBAC = get_rbac() 

    return render_template('productsnew.html', form = form, lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

@app.route('/productsdelete/<id>/')
def productsdelete(id):

    if current_user.is_anonymous:
        return (no_access_text())

    product = db.session.execute(db.select(Products).filter_by(Id=id)).scalar_one()
    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('products'))

#------------------------------------------------------------------------------------------

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

    lRBAC = get_rbac()

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

    lRBAC = get_rbac()

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

    lRBAC = get_rbac()

    return render_template('users.html', users = users , lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

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
        print()
        print ('=================================================================')

        lRBAC = get_rbac()

        users = Users.query.all()

        return render_template('users.html', users = users, lRBAC = lRBAC)

    instructors = db.session.execute(db.select(Instructors.Id, Instructors.User, Instructors.Name).where(Instructors.Active).order_by(Instructors.Name))

    lRBAC = get_rbac()

    return render_template('usersproductform.html', form=form, instructors=filtered2, appointments=filtered, lRBAC=lRBAC, cInstructors=cInstructors, cOptions=cOptions)

#------------------------------------------------------------------------------------------
# this is functional!

@app.route('/registerform2/<id>/', methods=['GET', 'POST'])
def registerform2(id):

    if current_user.is_anonymous:
        return (no_access_text())

    form = RegisterForm2(id)

    user = Users.query.filter_by(Id = int(id)).first()

    listStatus = ('new', 'student', 'staff', 'instructor', 'admin')

    lInstructorBefore = False
    cRolesBefore = user.Status
    if "instructor" in cRolesBefore:
        lInstructorBefore = True

    if form.validate_on_submit():

        newpassword = ""
        lRBAC = get_rbac()
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
        cStatus = ''
        nC = 0
        for l in listStatus:
            value = request.form.get(eval('listStatus [nC]'))
            if value:
                cStatus = cStatus + listStatus [nC] + ' '
            nC = nC + 1

        x.Status       = cStatus
        db.session.commit()

        lInstructorAfter = False
        cRolesAfter = cStatus
        if "instructor" in cRolesAfter:
            lInstructorAfter = True

        print("#### ---------------------------------------------------------------")
        print("#### before ", lInstructorBefore)
        print("#### after  ", lInstructorAfter)

        if lInstructorBefore and not lInstructorAfter:

            print ('#### removing instructor from table instructors')

            instructor = db.session.execute(db.select(Instructors).filter_by(User = x.Id)).scalar_one_or_none()
            print ("#### instructor.Name: ", instructor.Name)
            #db.session.delete(instructor)
            instructor.Active = False
            db.session.commit()

        #lRBAC = get_rbac() 

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
                #db.session.delete(instructor)
                instructor.Active = True
                db.session.commit()

        print('####')

        print("#### ---------------------------------------------------------------")

        return redirect(url_for('users'))
    
    if form.errors != {}: # no errors?
        for err_msg in form.errors.values():
            flash(f'error: {err_msg}', category = 'danger')

    lRBAC = get_rbac()

    return render_template('registerform2.html', form = form, user = user, listStatus = listStatus , lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

@app.route('/register', methods=['GET' ,'POST'])
def register():

    form = RegisterForm()

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

    lRBAC = get_rbac()

    return render_template('register.html', form=form , lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

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


        lRBAC = get_rbac() 

        return render_template('usersinfo.html', form = form, user = user, appointments = appointments, products = products, lRBAC = lRBAC)
    
    cDateToday = datetime.datetime.today()

    lRBAC = get_rbac() 

    return render_template('usersinfo.html', form = form, user = user, appointments = appointments, products = products, cDateToday = cDateToday, lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

@app.route('/userdelete/<id>')
def userdelete(id):

    if current_user.is_anonymous:
        return (no_access_text())

    user = db.session.execute(db.select(Users).filter_by(Id=id)).scalar_one()
    db.session.delete(user)
    db.session.commit()

    lRBAC = get_rbac() 

    return redirect(url_for('users'), lRBAC = lRBAC)

#------------------------------------------------------------------------------------------
