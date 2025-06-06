
from Package import db
from Package import app
from Package.models import Appointments, Users, Instructors, Products, Notes
from flask import Flask, render_template, redirect, url_for, flash, request

from flask_login import current_user

from Package.functions import get_rbac, no_access_text, GetNote, SaveNote, string2safe

from Package.forms import AppointmentsEditForm, LoginForm, ProductsEditForm, ProductsUsersForm, ProductsNewForm, UsersRegisterForm, UsersInfoForm, \
                          UsersEditForm2, UsersProductForm2, AppointmentsDateForm2, AppointmentsEventsForm

import datetime
from datetime import timedelta

from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy import func, and_
from Package.functions import logtext
from Package.functions import myquery


##########################################################################################################################

   ###    ########  ########   #######  #### ##    ## ######## ##     ## ######## ##    ## ########  ######  
  ## ##   ##     ## ##     ## ##     ##  ##  ###   ##    ##    ###   ### ##       ###   ##    ##    ##    ## 
 ##   ##  ##     ## ##     ## ##     ##  ##  ####  ##    ##    #### #### ##       ####  ##    ##    ##       
##     ## ########  ########  ##     ##  ##  ## ## ##    ##    ## ### ## ######   ## ## ##    ##     ######  
######### ##        ##        ##     ##  ##  ##  ####    ##    ##     ## ##       ##  ####    ##          ## 
##     ## ##        ##        ##     ##  ##  ##   ###    ##    ##     ## ##       ##   ###    ##    ##    ## 
##     ## ##        ##         #######  #### ##    ##    ##    ##     ## ######## ##    ##    ##     ######  

##########################################################################################################################

@app.route('/appointments')
def appointments():

    logtext('/appointments','i')

    if current_user.is_anonymous:
        logtext('anonymous','w')
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

##########################################################################################################################

   ###    ########  ########           ######     ###    ##       ######## ##    ## ########     ###    ########  
  ## ##   ##     ## ##     ##         ##    ##   ## ##   ##       ##       ###   ## ##     ##   ## ##   ##     ## 
 ##   ##  ##     ## ##     ##         ##        ##   ##  ##       ##       ####  ## ##     ##  ##   ##  ##     ## 
##     ## ########  ########          ##       ##     ## ##       ######   ## ## ## ##     ## ##     ## ########  
######### ##        ##                ##       ######### ##       ##       ##  #### ##     ## ######### ##   ##   
##     ## ##        ##                ##    ## ##     ## ##       ##       ##   ### ##     ## ##     ## ##    ##  
##     ## ##        ##        #######  ######  ##     ## ######## ######## ##    ## ########  ##     ## ##     ## 

##########################################################################################################################

@app.route('/appointmentscalendar')
def appointmentscalendar():

    logtext('/appointmentscalendar','i')

    cHtml = ""



    return (cHtml)

##########################################################################################################################

   ###    ########  ########          ########  ######## ##       ######## ######## ######## 
  ## ##   ##     ## ##     ##         ##     ## ##       ##       ##          ##    ##       
 ##   ##  ##     ## ##     ##         ##     ## ##       ##       ##          ##    ##       
##     ## ########  ########          ##     ## ######   ##       ######      ##    ######   
######### ##        ##                ##     ## ##       ##       ##          ##    ##       
##     ## ##        ##                ##     ## ##       ##       ##          ##    ##       
##     ## ##        ##        ####### ########  ######## ######## ########    ##    ######## 

##########################################################################################################################

@app.route('/appointmentsdelete/<int:id>/<string:cFrom>')
def appointmentsdelete(id, cFrom):

    logtext('/appointmentsdelete id:' + str(id) + ' from:' + cFrom,'i')


    if current_user.is_anonymous:
        logtext('anonymous','w')
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


##########################################################################################################################

   ###    ########  ########             ###     ######   ######  ####  ######   ##    ## 
  ## ##   ##     ## ##     ##           ## ##   ##    ## ##    ##  ##  ##    ##  ###   ## 
 ##   ##  ##     ## ##     ##          ##   ##  ##       ##        ##  ##        ####  ## 
##     ## ########  ########          ##     ##  ######   ######   ##  ##   #### ## ## ## 
######### ##        ##                #########       ##       ##  ##  ##    ##  ##  #### 
##     ## ##        ##                ##     ## ##    ## ##    ##  ##  ##    ##  ##   ### 
##     ## ##        ##        ####### ##     ##  ######   ######  ####  ######   ##    ## 

##########################################################################################################################

@app.route('/appointmentsassign/<int:id>/<string:cFrom>')
def appointmentsassign(id, cFrom):

    logtext('/appointmentsassign id' + str(id) + ' from:' + cFrom,'i')

    if current_user.is_anonymous:
        logtext('anonymous','w')
        return (no_access_text())

    #print('-------------------------------------------------------')

    #print(f'current_user.Username: { current_user.Username }')
    #print('current_user.Username: ' + current_user.Username )

    #if current_user.is_authenticated:
    #    print('current_user.is_authenticated')
    #    print(current_user.is_authenticated)

    user        = db.session.execute(db.select(Users).filter_by(Username = current_user.Username)).scalar_one()
    instructor  = db.session.execute(db.select(Instructors).filter_by(User = user.Id)).scalar_one()
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


##########################################################################################################################

   ###    ########  ########          ##     ## ##    ##    ###     ######   ######  ####  ######   ##    ## 
  ## ##   ##     ## ##     ##         ##     ## ###   ##   ## ##   ##    ## ##    ##  ##  ##    ##  ###   ## 
 ##   ##  ##     ## ##     ##         ##     ## ####  ##  ##   ##  ##       ##        ##  ##        ####  ## 
##     ## ########  ########          ##     ## ## ## ## ##     ##  ######   ######   ##  ##   #### ## ## ## 
######### ##        ##                ##     ## ##  #### #########       ##       ##  ##  ##    ##  ##  #### 
##     ## ##        ##                ##     ## ##   ### ##     ## ##    ## ##    ##  ##  ##    ##  ##   ### 
##     ## ##        ##        #######  #######  ##    ## ##     ##  ######   ######  ####  ######   ##    ## 

##########################################################################################################################

@app.route('/appointmentsunassign/<int:id>/<string:cFrom>')
def appointmentsunassign(id, cFrom):

    logtext('/appointmentsunassign id:' + str(id) + ' from:' + cFrom,'i')


    if current_user.is_anonymous:
        logtext('anonymous','w')
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


##########################################################################################################################

   ###    ########  ########          ######## ########  #### ######## 
  ## ##   ##     ## ##     ##         ##       ##     ##  ##     ##    
 ##   ##  ##     ## ##     ##         ##       ##     ##  ##     ##    
##     ## ########  ########          ######   ##     ##  ##     ##    
######### ##        ##                ##       ##     ##  ##     ##    
##     ## ##        ##                ##       ##     ##  ##     ##    
##     ## ##        ##        ####### ######## ########  ####    ##    

##########################################################################################################################

@app.route('/appointmentsedit/<int:id>/<string:cFrom>', methods=['GET', 'POST'])
def appointmentsedit(id, cFrom):

    logtext('/appointmentsedit idi' + str(id) + ' from:' + cFrom,'i')

    if current_user.is_anonymous:
        logtext('anonymous','w')
        return (no_access_text())

    form = AppointmentsEditForm()

    cDebug = ''
    #                                           0                1                  2                3               4                    5                   6                  7                   8                 9 (temp)             10
    #appointment = db.session.execute(db.select(Appointments).filter_by(Id=id)).scalar_one()
    appointment = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name, Instructors.Active , Appointments.Assistants). \
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

    nPrevUser = appointment.User
    nPrevInstructor = appointment.Staff

    cNote = GetNote(appointment.Id, 'ap')
    form.note.data = cNote

    if form.validate_on_submit():
        logtext('validate_on_submit ' + str(id), 'i')

        if request.form.get('cancel') == 'cancel':
            logtext('cancelled ' + str(id), 'i')

            if cFrom == 'usersinfo':
                return redirect(url_for('usersinfo', id = nPrevUser))
            
            if cFrom == 'instructorsinfo':
                return redirect(url_for('instructorsinfo', id = nPrevInstructor))
            
            if cFrom == "appointments":
                return redirect(url_for('appointments'))           

            # print('cancel')
            return redirect(url_for('homepage'))           

        cNote          = string2safe(request.form["note"])
        SaveNote(appointment.Id, 'ap', cNote, 'replace')

        x = db.session.query(Appointments).get(id)
        cStaff      = request.form["instructor"]    # list
        cAssistants = request.form["assistants1"]   # list
        cDate       = request.form["date"]          # formatted input
        cTime       = request.form["time"]          # formatted input

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
        # print ('cAssistant: ', cAssistants)
        # x.Notes      = request.form["notes"] # cStaff + ' | ' + cDate + ' | ' + cTime + ' | ' + dDateText + ' | ' + dDate.strftime('%Y-%m-%d_%H.%M')
        # x.Notes    = cDebug
        db.session.commit()

        if cFrom == 'home':
            return redirect(url_for('homepage'))

        if cFrom == 'usersinfo':
            return redirect(url_for('usersinfo', id = nPrevUser))
        
        if cFrom == 'instructorsinfo':
            return redirect(url_for('instructorsinfo', id = nPrevInstructor))
            
        return redirect(url_for('appointments'))

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('appointmentsedit.html', form = form, appointment = appointment2, cDebug = cDebug, instructors = instructors2, \
                           instructors2 = instructors2, lRBAC = lRBAC, assistants = assistants)


##########################################################################################################################

   ###    ########  ########          ########     ###    ######## ######## 
  ## ##   ##     ## ##     ##         ##     ##   ## ##      ##    ##       
 ##   ##  ##     ## ##     ##         ##     ##  ##   ##     ##    ##       
##     ## ########  ########          ##     ## ##     ##    ##    ######   
######### ##        ##                ##     ## #########    ##    ##       
##     ## ##        ##                ##     ## ##     ##    ##    ##       
##     ## ##        ##        ####### ########  ##     ##    ##    ######## 

##########################################################################################################################

@app.route('/appointmentsdateform2/<string:text>/<string:cFrom>', methods=['GET', 'POST'])
def appointmentsdate2(text, cFrom):

    logtext('/appointmentsdateform2 date:' + text + ' from:' + cFrom, 'i')

    if current_user.is_anonymous:
        logtext('anonymous','w')
        return (no_access_text())

    form = AppointmentsDateForm2(text)

    # appointment = db.session.execute(db.select(Appointments).filter_by(Id=id)).scalar_one()
    #
    #user    = appointment.User
    #product = appointment.Product

    # http://127.0.0.1:5000/appointmentsdateform2/02-09-2024/
    cDate = text [6:10] + '_' + text [3:5] + "_" + text [0:2]
    dDate = datetime.date(int(text [6:10]), int(text [3:5]), int(text [0:2]))

    #                                           0                1                  2                3               4                     5                  6                  7                   8                 9               10                    11
    appointments = db.session.execute(db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name, Instructors.Id, Appointments.Product, Appointments.Assistants). \
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

    assistants = Users.query.filter(Users.Status.contains('assistant'))

    if form.validate_on_submit():
        logtext('validate_on_submit ' + cDate, 'i')

        # print("validate_on_submit")
        # print("form.cancel.data: ", form.cancel.data)
        # print("form.save.data: ", form.save.data)
        # print(request.form.get('save'))
        # print(request.form.get('cancel'))
        
        if request.form.get('cancel') == 'cancel':
            logtext('cancelled ' + cDate, 'i')
            return redirect(url_for('homepage'))           

        for a in filtered:
            # print('--- begin ---')
            cDate = chr(34) + 'date' + str(a [0]) + chr(34)
            # print('cDate: ', cDate)
            cDateValue = request.form.get(eval(cDate))                 # formatted input
            cTime = chr(34) + 'time' + str(a [0]) + chr(34)
            cTimeValue = request.form.get(eval(cTime))                 # formatted input
            cInstructor = chr(34) + 'instructor' + str(a [0]) + chr(34)
            cInstructorValue = request.form.get(eval(cInstructor))     # provided list
            # print('cInstructorValue: ', cInstructor, cInstructorValue)
            cAssistantField = chr(34) + 'assistant' + str(a [0]) + chr(34)
            cAssistantValue = request.form.get(eval(cAssistantField))  # provided list
            # print('cAssistantValue:  ', cAssistantField, cAssistantValue)

            nInstructor = 0
            for i in filtered2:
                if i.Name == cInstructorValue:
                    nInstructor = i.Id

            appointment = db.session.execute(db.select(Appointments).filter_by(Id=a [0])).scalar_one()
            dDate = datetime.datetime(int(cDateValue[0:4]), int(cDateValue[5:7]), int(cDateValue[8:10]), int(cTimeValue[0:2]), int(cTimeValue[3:5]))
            appointment.Date = dDate
            appointment.Staff = nInstructor
            appointment.Assistants = cAssistantValue
            db.session.commit()
            # print('---- end ---')

        lRBAC = get_rbac(request.url_rule.endpoint)

        users = Users.query.all()

        if cFrom == 'home':
            return redirect(url_for('homepage'))           

        return render_template('users.html', users = users, lRBAC = lRBAC)

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('usersproductform.html', form=form, instructors = filtered2, appointments = filtered, lRBAC = lRBAC, assistants = assistants)


##########################################################################################################################

   ###    ########  ########          ######## ##     ## ######## ##    ## ########  ######  
  ## ##   ##     ## ##     ##         ##       ##     ## ##       ###   ##    ##    ##    ## 
 ##   ##  ##     ## ##     ##         ##       ##     ## ##       ####  ##    ##    ##       
##     ## ########  ########          ######   ##     ## ######   ## ## ##    ##     ######  
######### ##        ##                ##        ##   ##  ##       ##  ####    ##          ## 
##     ## ##        ##                ##         ## ##   ##       ##   ###    ##    ##    ## 
##     ## ##        ##        ####### ########    ###    ######## ##    ##    ##     ######  

##########################################################################################################################

@app.route('/appointmentsevents/<string:cName>/<string:cDate>/<string:cFrom>', methods=['GET', 'POST'])
def appointmentsevents(cName, cDate, cFrom):

    logtext('open name:' + cName + ' date:' + cDate + ' from:' + cFrom,'i')

    if current_user.is_anonymous:
        logtext('anonymous','w')
        return (no_access_text())

    form = AppointmentsEventsForm(cName)

    # print()
    #print('---------------------------------------------------------------------')
    #print('cName: ', cName)
    #print('cFrom: ', cFrom)
    #print('cDate: ', cDate)
    # print(cDate[6:10])
    # print(cDate[3:5])
    # print(cDate[0:2])
    dDate = datetime.date(int(cDate[6:10]), int(cDate[3:5]), int(cDate[0:2]))
    #print('dDate: ', dDate)
    #print()

    #                                           0                1                  2                3               4                     5                  6                  7                   8                 9               10                    11                       12
    appointments = db.session.execute(db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name, Instructors.Id, Appointments.Product, Appointments.Assistants, Users.Active). \
                                where(and_(func.date(Appointments.Date) == dDate , (Appointments.Product == 1))). \
                                join(Users,       Appointments.User    == Users.Id). \
                                join(Instructors, Appointments.Staff   == Instructors.Id). \
                                join(Products,    Appointments.Product == Products.Id) )

    appointments2 = []
    for a in appointments:
        appointments2.append(a)

        #print(a.Date, a.Firstname, a.Lastname, a.Productname)

    instructors = db.session.execute(db.select(Instructors.Id, Instructors.User, Instructors.Name).where(Instructors.Active).order_by(Instructors.Name))

    # print('first pass')
    # for i in instructors:
    #     print('i: ', i[0],i[1],i[2])
    # print()
    # print('second pass')
    # for i in instructors:
    #     print('i: ', i[0],i[1],i[2])

    instructors2 = []
    for row in instructors:
        instructors2.append(row)
    
    # print('first pass')
    # for i in instructors2:
    #     print('i: ', i[0],i[1],i[2])
    # print()
    # print('second pass')
    # for i in instructors2:
    #     print('i: ', i[0],i[1],i[2])

    # user = Users.query.filter(and_((Users.Firstname == cFirstname), (Users.Lastname == cLastname)))
    assistants = Users.query.filter(Users.Status.contains('assistant'))

    # print()
    # print('first pass')
    # for a in assistants:
    #     print('a: ', a.Id,a.Firstname,a.Lastname,a.Status)
    # print('second pass')
    # print()
    # for a in assistants:
    #     print('a: ', a.Id,a.Firstname,a.Lastname,a.Status)

    #print('---------------------------------------------------------------------')
    #print()

    lRBAC = get_rbac(request.url_rule.endpoint)

    if form.validate_on_submit():
        logtext('validate_on_submit ' + cDate,'i')

        if request.form.get('cancel') == 'cancel':
            logtext('cancel ' + cDate,'i')
            return redirect(url_for('homepage'))           

        cAutofillin = request.form.get("autofillin") # checkbox
        print('cAutofillin: ', cAutofillin)
        # logtext('appointmentsevents:form.validate_on_submit:autofillin=' + cAutofillin,'i')

        cNewstudent = string2safe(request.form.get("newstudent"))
        #print('cNewstudent: ', cNewstudent)

        cPrevinstructor = ''
        cPrevassistant  = ''

        for a in appointments2:
            cInstructor = chr(34) + "instructor" + str(a.Id) + chr(34)
            cInstructorValue = request.form.get(eval(cInstructor))       # provided list
            cAssistant = chr(34) + "assistant"+str(a.Id) + chr(34)
            cAssistantValue = request.form.get(eval(cAssistant))         # provided list

            if cAutofillin == 'checked':
                if len(cInstructorValue) > 0:
                    if cInstructorValue == '[none]':
                        cInstructorValue = cPrevinstructor
                if len(cPrevassistant) > 0:
                    if cAssistantValue == 'none':
                        cAssistantValue = cPrevassistant

            cPrevinstructor = cInstructorValue
            cPrevassistant  = cAssistantValue

            nFound = 0
            for i in instructors2:
                if cInstructorValue == i[2]:
                    nFound = i[0]
            
            #print('nFound: ', nFound)

            appointment = db.session.execute(db.select(Appointments).filter_by(Id = a.Id)).scalar_one()
            appointment.Staff      = nFound
            appointment.Assistants = cAssistantValue
            db.session.commit()

        if len(cNewstudent) > 0:
            cDateToday = datetime.datetime.today()
            cNewusername = cNewstudent.replace(' ', '_') + '_' + cName + '_' + cDateToday.strftime("%Y%m%d%H%M")

            user_to_create = Users(Username  = cNewusername,
                                Firstname    = cNewstudent,
                                Lastname     = '',
                                Phone        = '',
                                Emailaddress = '',
                                Passwordhash = '-',
                                Active       = False,
                                Status       = "new")
            
            db.session.add(user_to_create)
            db.session.commit()

            # assistants = Users.query.filter(Users.Status.contains('assistant'))
            # user         = Users.query.filter(Users.Username.contains('a'))
            user = db.session.execute(db.select(Users).filter_by(Username = cNewusername)).scalar_one()

            #print('user.Id: ', user.Id)
            #print('user.Username: ', user.Username)

            cFormTime = request.form.get('time00')              # formatted input
            cFormDate = request.form.get('date00')              # formatted input
            cAssistantForm = request.form.get('assistant00')    # provided list

            # 20240916?
            # cInstructor = chr(34) + "instructor" + str(a.Id) + chr(34)
            # print(cInstructor)
            cInstructorValue = request.form.get('instructor00') # provided list
            nFound = 0
            for i in instructors2:
                #print('-- i:',i[0], i[1], i[2])
                if cInstructorValue == i[2]:
                    nFound = i[0]
                    #print('-- found')

            # print('cInstructorValue: ', cInstructorValue)

            # print('nFound: ', nFound)
            # print('cFormDate: ', cFormDate)
            # print('cFormTime: ', cFormTime)

            # print((cFormDate[0:4]))  # year
            # print((cFormDate[5:7]))  # month
            # print((cFormDate[8:10])) # dat
            # print((cFormTime[0:2]))  # hour
            # print((cFormTime[3:5]))  # min

            # print('date: ', int(cFormDate[0:4]), int(cFormDate[5:7]), int(cFormDate[8:10]), int(cFormTime[0:2]), int(cFormTime[3:5]))

            dDate = datetime.datetime(int(cFormDate[0:4]), int(cFormDate[5:7]), int(cFormDate[8:10]), int(cFormTime[0:2]), int(cFormTime[3:5]))

            # find dsd in products
            dbquery = 'db.session.execute(db.select(Products).filter_by(Productname = "Discover_Scuba_Diving")).scalars()' # scalar_one_or_none()
            nDSD = eval(dbquery)
            print('#1 nDSD: ', nDSD)
            logtext('#1 DSD: ' + str(nDSD), 'i')

            dbquery = 'db.session.execute(db.select(Products).filter_by(Productname = "Discover_Scuba_Diving")).scalar_one()' # scalar_one_or_none() # Abbr = "DSD"
            nDSD = eval(dbquery)
            print('#2 nDSD: ', nDSD)
            logtext('#2 DSD: ' + str(nDSD), 'i')

            appointment_to_create = Appointments(User      = user.Id,
                                                Date       = dDate,
                                                Product    = 1,
                                                Part       = 'zw',
                                                Staff      = nFound,
                                                Assistants = cAssistantForm )
            
            db.session.add(appointment_to_create)
            logtext('add appointment', 'i')
            db.session.commit()

            # http://127.0.0.1:5000/appointmentsevents/dsd/13-09-2024/home
        return redirect(url_for('appointmentsevents', cName = 'dsd', cDate = cDate, cFrom = 'home' ))
    
    return render_template('appointmentsevents.html', form=form, appointments=appointments2, assistants=assistants, instructors=instructors2, lRBAC=lRBAC)


##########################################################################################################################

   ###    ########  ########          ##    ##  #######  ######## ########  ######  
  ## ##   ##     ## ##     ##         ###   ## ##     ##    ##    ##       ##    ## 
 ##   ##  ##     ## ##     ##         ####  ## ##     ##    ##    ##       ##       
##     ## ########  ########          ## ## ## ##     ##    ##    ######    ######  
######### ##        ##                ##  #### ##     ##    ##    ##             ## 
##     ## ##        ##                ##   ### ##     ##    ##    ##       ##    ## 
##     ## ##        ##        ####### ##    ##  #######     ##    ########  ######  

##########################################################################################################################

@app.route('/appointmentsnotes/<string:text>/<string:cFrom>', methods=['GET', 'POST'])
def appointmentsnotes(text, cFrom):

    logtext('/appointmentsnotes ' + text + ' from:' + cFrom,'i')

    if current_user.is_anonymous:
        logtext('anonymous','w')
        return (no_access_text())
    
    print('cDate: ', text)
    dDate = datetime.date(int(text[6:10]), int(text[3:5]), int(text[0:2]))
    print('dDate: ', dDate)

    print('--- appointmentsnotes:' + str(text) + '-----------------------------------------------')
    #                                            0                1                  2                3               4                     5                  6                  7                   8                 9
    appointments = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name, Appointments.Assistants). \
                                order_by(Appointments.Date). \
                                where(func.date(Appointments.Date) == dDate). \
                                select_from(Appointments). \
                                join(Users, Appointments.User == Users.Id). \
                                join(Instructors, Appointments.Staff == Instructors.Id). \
                                join(Products, Appointments.Product == Products.Id) )

    cText = "<h3>Notes " + text + "</h3><br><br>"
    cCRLF = chr(13) + chr(10)

    #cText = cText + "<table style='border-top: 1pt solid white; border-bottom: 1pt solid white;'>" + cCRLF
    cText = cText + "<table>" + cCRLF

    for a in appointments:
        # print(a [6].strftime("%d-%m-%Y %H:%M") )

        cText = cText + "<tr style='border-top: 1pt solid white;'><td style='width:200px'>date</td><td style='width:400px'>" + a [6].strftime("%d-%m-%Y %H:%M") + "</td></tr>" + cCRLF
        cText = cText + "<tr><td>product</td><td>" + a[4] + " - " + a[5] + "</td></tr>" + cCRLF
        cText = cText + "<tr><td>instructor</td><td>" + a[8] + "</td></tr>" + cCRLF
        cText = cText + "<tr><td>Assistant</td><td>" + a[9] + "</td></tr>" + cCRLF
        cText = cText + "<tr><td>&nbsp;</td><td></td></tr>" + cCRLF
        cText = cText + "<tr><td>student</td><td>" + a[2] + " " + a[3] + "</td></tr>" + cCRLF
        cText = cText + "<tr style='border-top: 1pt solid white;'><td>&nbsp;</td><td></td></tr>" + cCRLF

        cNotes = GetNote(a[0], 'ap')   
        cNotes = cNotes.replace(chr(13) + chr(10), '<br>')

        cText = cText + "<tr><td colspan=2>" + cNotes + "</td></tr>" + cCRLF
        cText = cText + "<tr><td>&nbsp;</td><td></td></tr>" + cCRLF

    cText = cText + "<tr style='border-top: 1pt solid white;'><td>&nbsp;</td><td></td></tr>" + cCRLF
    cText = cText + "</table>"

    lRBAC = get_rbac(request.url_rule.endpoint) 

    return render_template('usersnotes.html', cText = cText , lRBAC = lRBAC)


##########################################################################################################################


   ###    ########  ########           ######  ##       ########    ###    ##    ## ##     ## ########  
  ## ##   ##     ## ##     ##         ##    ## ##       ##         ## ##   ###   ## ##     ## ##     ## 
 ##   ##  ##     ## ##     ##         ##       ##       ##        ##   ##  ####  ## ##     ## ##     ## 
##     ## ########  ########          ##       ##       ######   ##     ## ## ## ## ##     ## ########  
######### ##        ##                ##       ##       ##       ######### ##  #### ##     ## ##        
##     ## ##        ##                ##    ## ##       ##       ##     ## ##   ### ##     ## ##        
##     ## ##        ##        #######  ######  ######## ######## ##     ## ##    ##  #######  ##        


##########################################################################################################################


@app.route('/cleanupallappointments/')
def cleanupallappointments():

    logtext('/cleanupallappointments','i')


    lRBAC = get_rbac('')
    if 'Admin' in lRBAC[0]:

        Appointments.query.delete()
        db.session.commit()

        db.session.query(Notes).filter(Notes.Type=='ap').delete()
        db.session.commit()

    lRBAC = get_rbac('')

    return render_template('home.html', lRBAC = lRBAC)




##########################################################################################################################


########  ########   #######  ########           ######  ##       ########    ###    ##    ## ##     ## ########  
##     ## ##     ## ##     ## ##     ##         ##    ## ##       ##         ## ##   ###   ## ##     ## ##     ## 
##     ## ##     ## ##     ## ##     ##         ##       ##       ##        ##   ##  ####  ## ##     ## ##     ## 
########  ########  ##     ## ##     ##         ##       ##       ######   ##     ## ## ## ## ##     ## ########  
##        ##   ##   ##     ## ##     ##         ##       ##       ##       ######### ##  #### ##     ## ##        
##        ##    ##  ##     ## ##     ##         ##    ## ##       ##       ##     ## ##   ### ##     ## ##        
##        ##     ##  #######  ########  #######  ######  ######## ######## ##     ## ##    ##  #######  ##        


##########################################################################################################################


@app.route('/cleanupallproducts/')
def cleanupallproducts():

    logtext('/cleanupallproducts','i')

    lRBAC = get_rbac('')
    if 'Admin' in lRBAC[0]:

        Products.query.delete()
        db.session.commit()

        db.session.query(Notes).filter(Notes.Type=='ap').delete()
        db.session.commit()

    lRBAC = get_rbac('')

    return render_template('home.html', lRBAC = lRBAC)
 