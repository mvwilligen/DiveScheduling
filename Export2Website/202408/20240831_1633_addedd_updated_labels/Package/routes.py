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

# added 20240831 1527   - issues with reinit_db.py
from Package import db
from Package import app
from Package.models import Appointments, Users, Instructors, Products

from flask import Flask, render_template, redirect, url_for, flash, request
from Package.forms import AppointmentsEditForm, LoginForm, ProductsEditForm, ProductsUsersForm, ProductsNewForm, UsersEditForm, UsersInfoForm, RegisterForm, RegisterForm2

#source: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import current_user, login_user, logout_user

import sqlalchemy as sa
from sqlalchemy import func, and_

import datetime
from datetime import timedelta

#------------------------------------------------------------------------------------------

@app.route('/')
@app.route('/home')
def homepage():

    nDateFrom  = datetime.date.today() - timedelta(days=8)
    nYearFrom  = nDateFrom.year
    nMonthFrom = nDateFrom.month
    nDayFrom   = nDateFrom.day

    nDateTo  = datetime.date.today() + timedelta(days=29)
    nYearTo  = nDateTo.year
    nMonthTo = nDateTo.month
    nDayTo   = nDateTo.day

    #                                        1                2                  3                4               5                     6                  7                  8 
    calendar = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Instructors.Name). \
                                order_by(Appointments.Date). \
                                where(and_(func.DATE(Appointments.Date) > datetime.datetime(nYearFrom,nMonthFrom,nDayFrom), func.DATE(Appointments.Date) <= datetime.datetime(nYearTo,nMonthTo,nDayTo))). \
                                select_from(Appointments). \
                                join(Users, Appointments.User == Users.Id). \
                                join(Instructors, Appointments.Staff == Instructors.Id). \
                                join(Products, Appointments.Product == Products.Id) )

    return render_template('home.html', calendar=calendar)

#------------------------------------------------------------------------------------------

@app.route('/appointments')
def appointments():
    #appointments = Appointments.query.order_by(Appointments.Date.desc()).all()
    #appointments = Appointments.query.order_by(Appointments.Date.asc()).all()

    #                                                   0             1                2                 3                 4                5                       5               7                 8
    appointments = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name). \
                                order_by(Appointments.Date). \
                                select_from(Appointments). \
                                join(Users,       Appointments.User    == Users.Id). \
                                join(Instructors, Appointments.Staff   == Instructors.Id). \
                                join(Products,    Appointments.Product == Products.Id) )

    return render_template('appointments.html', appointments = appointments)

#------------------------------------------------------------------------------------------

@app.route('/appointmentsdelete/<id>/')
def appointmentsdelete(id):

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
    
    return render_template('appointments.html', appointments = appointments)

#------------------------------------------------------------------------------------------

@app.route('/appointmentsedit/<id>/', methods=['GET', 'POST'])
def appointmentsedit(id):

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

    instructors = db.session.execute(db.select(Instructors.Id, Instructors.User, Instructors.Name))

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

        x.Date   = dDate
        x.Staff  = nStaff
        x.Notes = request.form["notes"] # cStaff + ' | ' + cDate + ' | ' + cTime + ' | ' + dDateText + ' | ' + dDate.strftime('%Y-%m-%d_%H.%M')
        # x.Notes  = cDebug

        db.session.commit()

        return redirect(url_for('appointments'))

    return render_template('appointmentsedit.html', form=form, appointment=appointment2, cDebug=cDebug, instructors=instructors)

#------------------------------------------------------------------------------------------

@app.route('/instructors')
def instructors():

    instructors = db.session.execute( db.select(Instructors.Id, Instructors.User, Instructors.Name). \
                                order_by(Instructors.Name). \
                                select_from(Instructors). \
                                join(Users,       Instructors.User    == Users.Id) )
    
    return render_template('instructors.html', instructors = instructors)

#------------------------------------------------------------------------------------------

@app.route('/instructorsinfo/<id>/')
def instructorsinfo(id):

    instructor = db.session.execute( db.select(Instructors.Id, Instructors.User, Instructors.Name). \
                                order_by(Instructors.Name). \
                                where(Instructors.User == id).\
                                select_from(Instructors). \
                                join(Users,       Instructors.User    == Users.Id) )

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
    
    return render_template('instructorsinfo.html', instructor = instructor2, appointments = appointments) # , cCSV = cCSV

#------------------------------------------------------------------------------------------

# source: https://flask-login.readthedocs.io/en/latest/
# 20240830
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        # User.query.get(1)
        # login_user(db.session.get(Users, 1))
        login_user(db.session.execute(db.select(Users).filter_by(Id=3)).scalar())

        flash('Logged in successfully.')

        next = request.args.get('home')
        # url_has_allowed_host_and_scheme should check if the url is safe
        # for redirects, meaning it matches the request host.
        # See Django's url_has_allowed_host_and_scheme for an example.
        #if not url_has_allowed_host_and_scheme(next, request.host):
        #    return flask.abort(400)

        return redirect(url_for('home'))
    
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

#------------------------------------------------------------------------------------------

@app.route('/products')
def products():
    products = Products.query.all()
    return render_template('products.html', products=products)

#------------------------------------------------------------------------------------------

@app.route('/productsedit/<id>/', methods=('GET', 'POST'))
def productsedit(id):
    form = ProductsEditForm(id)
    product = db.get_or_404(Products, id)

    if form.validate_on_submit():

        x = db.session.query(Products).get(id)
        x.Date        = request.form["abbr"]
        x.Parts       = request.form["parts"]
        x.Description = request.form["description"]
        db.session.commit()

        return redirect(url_for('products'))

    return render_template('productsedit.html', form=form, product=product)
#------------------------------------------------------------------------------------------

@app.route('/productsnew/', methods=('GET', 'POST'))
def productsnew(id):

    form = ProductsNewForm(id)

    product = db.get_or_404(Products, id)

    if form.validate_on_submit():

        x = db.session.query(Products).get(id)
        x.ProductName = request.form["abbr"]
        x.Abbr        = request.form["abbr"]
        x.Parts       = request.form["parts"]
        x.Description = request.form["description"]
        db.session.commit()

        return redirect(url_for('products'))

    return render_template('productsedit.html', form=form, product=product)

#------------------------------------------------------------------------------------------

@app.route('/productsdelete/<id>/')
def productsdelete(id):

    product = db.session.execute(db.select(Products).filter_by(Id=id)).scalar_one()
    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('products'))

#------------------------------------------------------------------------------------------

@app.route('/productsusers/<id>/')
def productsusers(id):

    form = ProductsUsersForm(id)

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
        if cUser != row [3] + row [4]:
            cUser = row [3] + row [4]

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

    return render_template('productsusers.html', appointments = appointments2, form = form, cAppointments = cAppointments)

#------------------------------------------------------------------------------------------

@app.route('/support')
def support():
    return render_template('support.html')

#------------------------------------------------------------------------------------------

@app.route('/users')
def users():
    users = Users.query.all()
    return render_template('users.html', users=users)

#------------------------------------------------------------------------------------------
# this is functional!

@app.route('/registerform2/<id>/', methods=['GET', 'POST'])
def registerform2(id):

    form = RegisterForm2(id)

    user = Users.query.filter_by(Id=int(id)).first()
    listStatus = ('new', 'student', 'staff', 'instructor', 'admin')

    if form.validate_on_submit():

        # pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # import datetime
        # from datetime import date
        # from datetime import datetime
        # t = datetime.datetime.now()
        # cTime = t.strftime("%d-%m-%Y %H:%M:%S")

        x = db.session.query(Users).get(id)
        #x.Firstname    = form.firstname.data
        #x.Firstname    = 'test ' + cTime
        x.Firstname    = request.form["firstname"]
        #x.Lastname     = form.lastname.data
        x.Lastname     = request.form["lastname"]
        #x.Phone        = form.phone.data
        x.Phone        = request.form["phone"]
        #x.Emailaddress = form.emailaddress.data
        x.Emailaddress = request.form["emailaddress"]
        # x.passwordhash = pw_hash
              
        cStatus = ''
        nC = 0
        for l in listStatus:
            value = request.form.get(eval('listStatus [nC]'))
            if value:
                cStatus = cStatus + listStatus [nC] + ' '
            nC = nC + 1

        x.Status       = cStatus
        db.session.commit()

        return redirect(url_for('users'))
    
    if form.errors != {}: # no errors?
        for err_msg in form.errors.values():
            flash(f'error: {err_msg}', category = 'danger')

    return render_template('registerform2.html', form=form, user=user, listStatus = listStatus)

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

    return render_template('register.html', form=form)

#------------------------------------------------------------------------------------------

@app.route('/usersinfo/<id>', methods = ['GET', 'POST'])
def usersinfo(id):
    form = UsersInfoForm(id)

    #                                            0                1                  2                3               4                     5                  5                  7                   8  
    appointments = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name). \
                                order_by(Appointments.Date). \
                                where(Appointments.User == id). \
                                select_from(Appointments). \
                                join(Users, Appointments.User == Users.Id). \
                                join(Instructors, Appointments.Staff == Instructors.Id). \
                                join(Products, Appointments.Product == Products.Id) )
    user = db.session.execute(db.select(Users).filter_by(Id=id)).scalar_one()
    products = db.session.execute(db.select(Products)).scalars()

    if form.validate_on_submit():

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
                        A0 = Appointments(User = id, Product = p.Id, Part = part, Date = date0, Time = "19.30", Notes = "[" + cDate + ']', Staff = 1)
                        db.session.add(A0)
                        db.session.commit()
                        part = ""
                        t = t + 7
                    else:
                        part = part + b
                

        x.Info       = cInfo + cStatus
        db.session.commit()

        #                                            0                1                  2                3               4                     5                  5                  7                   8  
        appointments = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name). \
                                order_by(Appointments.Date). \
                                where(Appointments.User == id). \
                                select_from(Appointments). \
                                join(Users, Appointments.User == Users.Id). \
                                join(Instructors, Appointments.Staff == Instructors.Id). \
                                join(Products, Appointments.Product == Products.Id) )
        products = db.session.execute(db.select(Products)).scalars()


        return render_template('usersinfo.html', form = form, user = user, appointments = appointments, products = products)
    
    cDateToday = datetime.datetime.today()

    return render_template('usersinfo.html', form = form, user = user, appointments = appointments, products = products, cDateToday = cDateToday)

#------------------------------------------------------------------------------------------

@app.route('/userdelete/<id>')
def userdelete(id):

    user = db.session.execute(db.select(Users).filter_by(Id=id)).scalar_one()
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('users'))

#------------------------------------------------------------------------------------------


