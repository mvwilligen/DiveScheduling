
from Package import db
from Package import app
from Package.models import Appointments, Users, Instructors, Products
from flask import Flask, render_template, redirect, url_for, flash, request

from flask_login import current_user

from Package.functions import get_rbac, no_access_text

from Package.forms import AppointmentsEditForm, LoginForm, ProductsEditForm, ProductsUsersForm, ProductsNewForm, UsersRegisterForm, UsersInfoForm, UsersEditForm2, UsersProductForm2, AppointmentsDateForm2, AppointmentsEventForm

import datetime
from datetime import timedelta

from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy import func, and_


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

    #                                            0                1                  2                3               4                     5                  6                  7                   8                 9               10
    appointments = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name, Instructors.Id, Appointments.Assistants). \
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

    # appointments = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name). \
    #                             order_by(Appointments.Date). \
    #                             select_from(Appointments). \
    #                             join(Users, Appointments.User == Users.Id). \
    #                             join(Instructors, Appointments.Staff == Instructors.Id). \
    #                             join(Products, Appointments.Product == Products.Id) )

    #                                            0                1                  2                3               4                     5                  6                  7                   8                 9               10
    appointments = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name, Instructors.Id, Appointments.Assistants). \
                                order_by(Appointments.Date). \
                                select_from(Appointments). \
                                join(Users,       Appointments.User    == Users.Id). \
                                join(Instructors, Appointments.Staff   == Instructors.Id). \
                                join(Products,    Appointments.Product == Products.Id) )

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
    #                                           0                1                  2                3               4                    5                   6                  7                   8                 9                  10
    #appointment = db.session.execute(db.select(Appointments).filter_by(Id=id)).scalar_one()
    appointment = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name, Appointments.Notes, Appointments.Assistants). \
                                select_from(Appointments). \
                                filter_by(Id = id). \
                                join(Users, Appointments.User == Users.Id). \
                                join(Instructors, Appointments.Staff == Instructors.Id). \
                                join(Products, Appointments.Product == Products.Id) )

    instructors = db.session.execute(db.select(Instructors.Id, Instructors.User, Instructors.Name).where(Instructors.Active).order_by(Instructors.Name))

    # user = Users.query.filter(and_((Users.Firstname == cFirstname), (Users.Lastname == cLastname)))
    assistants = Users.query.filter(Users.Status.contains('assistant'))

    instructors2 = []
    for row in instructors:
        instructors2.append(row)

    appointment2 = []

    for row in appointment:
        for element in row:
            appointment2.append(element)
    #         if isinstance(element, int):
    #             cDebug = cDebug + str(element) + "; "
    #         elif isinstance(element, datetime.date):
    #             cDebug = cDebug + element.strftime("%d-%m-%Y") + "; "
    #         elif isinstance(element, datetime.datetime):
    #             cDebug = cDebug + element.strftime("%d-%m-%Y") + "; "
    #         else:
    #             cDebug = cDebug + element + "; "
    #     cDebug = cDebug + '#BR#'

    appointment = db.get_or_404(Appointments, id)

    if form.validate_on_submit():

        x = db.session.query(Appointments).get(id)
        cStaff      = request.form["instructor"]
        cAssistants = request.form["assistants1"]
        cDate       = request.form["date"]
        cTime       = request.form["time"]

        if cAssistants == 'no ne':
            cAssistants = ''

        # cDebug = cStaff + ', ' + cDate + ', ' + cTime

        instructors = db.session.execute(db.select(Instructors.Id, Instructors.User, Instructors.Name))

        nStaff = 6
        for i in instructors:
            if i.Name == cStaff:
                nStaff = i.Id

        dDateText = cDate[0:4] + '-' + cDate[5:7] + '-' + cDate[8:10] + ' | ' + cTime[0:2] + '.' + cTime[3:5]
        # dDate = date(int(cDate[0:4]), int(cDate[5:7]), int(cDate[8:10])) # , int(cTime[0:2]), int(cTime[3:5]))
        
        dDate = datetime.datetime(int(cDate[0:4]), int(cDate[5:7]), int(cDate[8:10]), int(cTime[0:2]), int(cTime[3:5]))

        x.Date       = dDate
        x.Staff      = nStaff
        x.Assistants = cAssistants
        print ('cAssistant: ', cAssistants)
        x.Notes      = request.form["notes"] # cStaff + ' | ' + cDate + ' | ' + cTime + ' | ' + dDateText + ' | ' + dDate.strftime('%Y-%m-%d_%H.%M')
        # x.Notes    = cDebug
        db.session.commit()

        if cFrom == 'home':
            return redirect(url_for('homepage'))

        return redirect(url_for('appointments'))

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('appointmentsedit.html', form=form, appointment=appointment2, cDebug=cDebug, instructors=instructors2, instructors2=instructors2, lRBAC = lRBAC, assistants = assistants)

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

    #                                           0                1                  2                3               4                     5                  6                  7                   8                 9               10
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

   ###    ########  ########          ######## ##     ## ######## ##    ## ########  ######  
  ## ##   ##     ## ##     ##         ##       ##     ## ##       ###   ##    ##    ##    ## 
 ##   ##  ##     ## ##     ##         ##       ##     ## ##       ####  ##    ##    ##       
##     ## ########  ########          ######   ##     ## ######   ## ## ##    ##     ######  
######### ##        ##                ##        ##   ##  ##       ##  ####    ##          ## 
##     ## ##        ##                ##         ## ##   ##       ##   ###    ##    ##    ## 
##     ## ##        ##        ####### ########    ###    ######## ##    ##    ##     ######  

@app.route('/appointmentsevent/<string:cName>/<string:cDate>/<string:cFrom>', methods=['GET', 'POST'])

def appointmentsevent(cName, cDate, cFrom):

    if current_user.is_anonymous:
        return (no_access_text())

    form = AppointmentsEventForm()

    print()
    print('---------------------------------------------------------------------')
    print('cName: ', cName)
    print('cFrom: ', cFrom)
    print('cDate: ', cDate)
    # print(cDate[6:10])
    # print(cDate[3:5])
    # print(cDate[0:2])
    dDate = datetime.date(int(cDate[6:10]), int(cDate[3:5]), int(cDate[0:2]))
    print('dDate: ', dDate)
    print()

    #                                           0                1                  2                                3                     4                  5                  6                   7                 8               9
    appointments = db.session.execute(db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name, Instructors.Id, Appointments.Product). \
                                where(and_(  func.date(Appointments.Date) == dDate , (Appointments.Product == 1)       )). \
                                join(Users,       Appointments.User    == Users.Id). \
                                join(Instructors, Appointments.Staff   == Instructors.Id). \
                                join(Products,    Appointments.Product == Products.Id) )

    appointments2 = []
    for a in appointments:
        appointments2.append(a)

        #print(a.Date, a.Firstname, a.Lastname, a.Productname)

    print('---------------------------------------------------------------------')
    print()

    lRBAC = get_rbac(request.url_rule.endpoint)

    if form.validate_on_submit():

        return redirect(url_for('homepage'))

    if cFrom == 'home':
        return redirect(url_for('appointmentsevent', appointments = appointments2, lRBAC = lRBAC))
    
    return redirect(url_for('homepage'))

