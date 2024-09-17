from flask import Flask, render_template, redirect, url_for, flash, request
from Package.models import Products, Users, Appointments
from Package import app, db
from Package.forms import AppointmentsEditForm, LoginForm, ProductsEditForm, ProductsUsersForm, UsersEditForm, UsersInfoForm, RegisterForm, RegisterForm2
from Package import bcrypt
from flask_login import login_user
import datetime
from sqlalchemy import func, and_

import datetime
from datetime import date, time
from datetime import datetime, timedelta

#------------------------------------------------------------------------------------------

@app.route('/')
@app.route('/home')
def homepage():

    nDateFrom  = datetime.today() - timedelta(days=8)
    nYearFrom  = nDateFrom.year
    nMonthFrom = nDateFrom.month
    nDayFrom   = nDateFrom.day

    nDateTo  = datetime.today() + timedelta(days=15)
    nYearTo  = nDateTo.year
    nMonthTo = nDateTo.month
    nDayTo   = nDateTo.day

    calendar = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date). \
                                order_by(Appointments.Date). \
                                where(and_(func.DATE(Appointments.Date) > datetime(nYearFrom,nMonthFrom,nDayFrom), func.DATE(Appointments.Date) <= datetime(nYearTo,nMonthTo,nDayTo))). \
                                select_from(Appointments). \
                                join(Users, Appointments.User == Users.Id). \
                                join(Products, Appointments.Product == Products.Id) )

    return render_template('home.html', calendar=calendar)

#------------------------------------------------------------------------------------------

@app.route('/appointments')
def appointments():
    #appointments = Appointments.query.order_by(Appointments.Date.desc()).all()
    #appointments = Appointments.query.order_by(Appointments.Date.asc()).all()

    #                                                   0             1                2                 3                 4                5                       5               7               
    appointments = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff). \
                                order_by(Appointments.Date). \
                                select_from(Appointments). \
                                join(Users, Appointments.User == Users.Id). \
                                join(Products, Appointments.Product == Products.Id) )

    return render_template('appointments.html', appointments = appointments)

#------------------------------------------------------------------------------------------

@app.route('/appointmentsdelete/<id>/')
def appointmentsdelete(id):

    appointment = db.session.execute(db.select(Appointments).filter_by(Id=id)).scalar_one()
    db.session.delete(appointment)
    db.session.commit()
    #                                                   0             1                2                 3                 4                5                       5               7               
    appointments = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff). \
                                order_by(Appointments.Date). \
                                select_from(Appointments). \
                                join(Users, Appointments.User == Users.Id). \
                                join(Products, Appointments.Product == Products.Id) )
    
    return render_template('appointments.html', appointments = appointments)

#------------------------------------------------------------------------------------------

@app.route('/appointmentsedit/<id>/', methods=['GET', 'POST'])
def appointmentsedit(id):

    form = AppointmentsEditForm(id)

    appointment = db.get_or_404(Appointments, id)

    if form.validate_on_submit():

        x = db.session.query(Products).get(id)
        x.Abbr        = request.form["abbr"]
        x.Parts       = request.form["parts"]
        x.Description = request.form["description"]
        db.session.commit()

        return redirect(url_for('appointments'))

    return render_template('appointmentsedit.html', form = form, appointment = appointment)

#------------------------------------------------------------------------------------------

@app.route('/support')
def support():
    return render_template('support.html')

#------------------------------------------------------------------------------------------

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = Users.query.filter_by(Username = form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            #login_user(attempted_user.Id)  # , remember=False
            loggedonuser = '[' + attempted_user.Username + form.username.data + ']'
            flash(f'logged in as: {attempted_user.Username} (ID:{attempted_user.Id})', category = 'success')
            return redirect(url_for('homepage'))
        else:
            loggedonuser = "n/a"
            flash(f'username ({attempted_user.Username}) or password ({form.password.data}) is incorrect', category = 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

#------------------------------------------------------------------------------------------

@app.route('/logout')
def logout():
    loggedonuser = ''
    flash('You have been logged out.', category = 'info')
    return redirect(url_for('homepage'))

#------------------------------------------------------------------------------------------

@app.route('/products')
def products():
#    items = [
#    {'id': 1, 'name': 'DiscoverScubaDiving', 'abbr': 'DSD', 'parts': 'DSD','price':  50},
#    {'id': 2, 'name': 'OpenWater'          , 'abbr': 'OW',  'parts': 'Intro|ZW1|ZW2|ZW3|Exam|BW1|BW2|BW3','price': 300},
#    {'id': 3, 'name': 'AdvancedOpenWater'  , 'abbr': 'AOW', 'parts': 'Intro|ZW1|ZW2|ZW3|ZW4|ZW5|Exam|BW1|BW2|BW3|BW4','price': 500},
#    ]
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

    appointments = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff). \
                                order_by(Appointments.User). \
                                where(Appointments.Product == id). \
                                select_from(Appointments). \
                                join(Users, Appointments.User == Users.Id). \
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
                elif isinstance(element, date):
                    cAppointments = cAppointments + element.strftime("%d-%m-%Y") + "; "
                elif isinstance(element, datetime):
                    cAppointments = cAppointments + element.strftime("%d-%m-%Y") + "; "
                else:
                    cAppointments = cAppointments + element + "; "
            cAppointments = cAppointments + '#BR#'

    return render_template('productsusers.html', appointments = appointments2, form = form, cAppointments = cAppointments)

#------------------------------------------------------------------------------------------

#CoPilot to the rescue! ;-)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    # results = Data.query.filter(Data.name.contains(query)).all()
    product = db.session.execute(db.select(Users).where(column(Users.Firstname).contains(query)))  # .all()
    return {'results': [data.name for data in results]}

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

    #                                                   0             1                2                 3                 4                5                       5               7               
    appointments = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff). \
                                order_by(Appointments.Date). \
                                where(Appointments.User == id). \
                                select_from(Appointments). \
                                join(Users, Appointments.User == Users.Id). \
                                join(Products, Appointments.Product == Products.Id) )
    user = db.session.execute(db.select(Users).filter_by(Id=id)).scalar_one()
    products = db.session.execute(db.select(Products)).scalars()

    if form.validate_on_submit():

        #t = datetime.datetime.now()
        #cTime = t.strftime("%d-%m-%Y %H:%M:%S")
        cDateToday = date.today()
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
                dt2 = datetime.strptime(cDateFrom, '%Y-%m-%d')
                for b in parts:
                    if b == "|":

                        nDateTo  = dt2 + timedelta(days=t)
                        nYearTo  = nDateTo.year  # nYearTo  = nDateTo.year
                        nMonthTo = nDateTo.month # nMonthTo = nDateTo.month
                        nDayTo   = nDateTo.day   # nDateTo.day + t

                        date0 = datetime.combine(date(nYearTo, nMonthTo, nDayTo), time(19,30))
                        A0 = Appointments(User = id, Product = p.Id, Part = part, Date = date0, Time = "19.30", Notes = "[" + cDate + ']', Staff = 2)
                        db.session.add(A0)
                        db.session.commit()
                        part = ""
                        t = t + 7
                    else:
                        part = part + b
                

        x.Info       = cInfo + cStatus
        db.session.commit()

        appointments = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff). \
                            order_by(Appointments.Date). \
                            where(Appointments.User == id). \
                            select_from(Appointments). \
                            join(Users, Appointments.User == Users.Id). \
                            join(Products, Appointments.Product == Products.Id) )
        products = db.session.execute(db.select(Products)).scalars()


        return render_template('usersinfo.html', form = form, user = user, appointments = appointments, products = products)
    
    cDateToday = date.today()

    return render_template('usersinfo.html', form = form, user = user, appointments = appointments, products = products, cDateToday = cDateToday)

#------------------------------------------------------------------------------------------

@app.route('/userdelete/<id>')
def userdelete(id):

    user = db.session.execute(db.select(Users).filter_by(Id=id)).scalar_one()
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('users'))

#------------------------------------------------------------------------------------------


