from Package import db
from Package import app
from Package.models import Appointments, Users, Instructors, Products, Notes, Status
from flask import Flask, render_template, redirect, url_for, flash, request

from flask_login import current_user

from Package.functions import get_rbac, no_access_text, GetNote, SaveNote, string2safe

from Package.forms import AppointmentsEditForm, LoginForm, ProductsEditForm, ProductsUsersForm, ProductsNewForm, UsersRegisterForm, UsersInfoForm, UsersEditForm2, UsersProductForm2, AppointmentsDateForm2, UsersProductNext

import datetime
from datetime import timedelta

from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy import func, and_

from dotenv import dotenv_values

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os
import os.path

from flask import request   


from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash

cCRLF = chr(13) + chr(10)

from Package.functions import logtext
from Package.functions import myquery

# import email_validator
from email_validator import validate_email, EmailNotValidError

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

    logtext('users', 'i')

    if current_user.is_anonymous:
        logtext('anonymous','w')
        return (no_access_text())

    # users = Users.query.all()
    users = db.session.execute(db.select(Users).filter_by(Active = True)).scalars()

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('users.html', users = users , lRBAC = lRBAC)

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

    logtext('usersdelete ' + id, 'i')

    if current_user.is_anonymous:
        logtext('anonymous','w')
        return (no_access_text())

    user = db.session.execute(db.select(Users).filter_by(Id=id)).scalar_one()
    cUsername = user.Username
    db.session.delete(user)
    db.session.commit()

    logtext('usersdelete ' + cUsername, 'i')

    print('#### cUsername:             ', cUsername)
    print('#### current_user.Username: ', current_user.Username)

    if cUsername == current_user.Username:
        return (url_for('logout'))

    lRBAC = get_rbac(request.url_rule.endpoint) 

    return redirect(url_for('users'))

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

    logtext('open ' + str(id) + ' from:' + cFrom, 'i')

    if current_user.is_anonymous:
        logtext('anonymous','w')
        return (no_access_text())

    form = UsersEditForm2()

    user = Users.query.filter_by(Id = int(id)).first()

    # listStatus = ['new', 'student', 'staff', 'assistant', 'instructor'] # , 'admin'
    listStatus = Status.query.all()

    lInstructorBefore = False
    cRolesBefore      = user.Status
    cStatusOld        = cRolesBefore

    if "instructor" in cRolesBefore:
        lInstructorBefore = True

    # note = Notes.query.filter(and_((Notes.User == user.Id), (Notes.Type == 'st')))

    # print('user.Id:   ', user.Id)
    # print('type(note: ', type(note))
    # print('note:      ', note)
    # print('Notes.Id:  ', Notes.Id)

    # if note:
    #     print('note is True')
    #     for n in note:
    #         print('n: ', n)
    #         cNote = n.Note
    #         print('cNote: ', cNote)
    # else:
    #     print('note is False')

    cNote = GetNote(user.Id, 'st')

    form.note.data = cNote

    if form.validate_on_submit():

        logtext('validate on submit ' + str(id), 'i')

        if request.form.get('cancel') == 'cancel':
            logtext('cancel  ' + str(id), 'i')

            if cFrom == 'instructors':

                return redirect(url_for('instructors'))

            return redirect(url_for('users'))

        newpassword = ""
        lRBAC = get_rbac(request.url_rule.endpoint)
        if "admin" in lRBAC [1]:
            newpassword = request.form["password"]     # will be processed and stored as a hash

        pw_hash = ""
        if len(newpassword) > 0: 
          pw_hash = bcrypt.generate_password_hash(newpassword).decode('utf-8')

        x = db.session.query(Users).get(id)
        x.Firstname    = string2safe(request.form["firstname"])
        x.Lastname     = string2safe(request.form["lastname"])
        x.Phone        = string2safe(request.form["phone"])
        x.Emailaddress = string2safe(request.form["emailaddress"])
        cNote          = string2safe(request.form["note"])
        if len(newpassword) > 0: 
            x.Passwordhash = pw_hash

        # -----------------------------------------------------------------------------      
        # process notes

        # if len(cNote) > 0:

        #     # class Notes(db.Model):
        #     #     __tablename__   = 'Notes'
        #     #  0   Id              = db.Column(db.Integer(),                primary_key=True)
        #     #  1   Author          = db.Column(db.Integer(),                nullable=True, unique=False)
        #     #  2   Date            = db.Column(db.DateTime(timezone=True))
        #     #  3   Description     = db.Column(db.String(60),               nullable=True, unique=False)
        #     #  4   Note            = db.Column(db.Text,                     nullable=True, unique=False)
        #     #  5   Datelastwritten = db.Column(db.DateTime(timezone=True))
        #     #  6   User            = db.Column(db.Integer(),                nullable=True, unique=False)
        #     #  7   Type            = db.Column(db.String(2) ,               nullable=True, unique=False) # st, re, ap, in, pr
        #     #     Product         = db.Column(db.Integer(),                nullable=True, unique=False)
        #     #     Appointment     = db.Column(db.Integer(),                nullable=True, unique=False)
        #     #     Instructor      = db.Column(db.Integer(),                nullable=True, unique=False)
        #     #     Studentrecord   = db.Column(db.Integer(),                nullable=True, unique=False)
        #     #     Text            = db.Column(db.Text(),                   nullable=True, unique=False)

        #     print('form.cNote: ', cNote)
        #     note = Notes.query.where(and_((Notes.User == user.Id),(Notes.Type == 'st'))).first()

        #     if not note:
        #         print('adding new note')
        #         note_to_create = Notes(Author          = lRBAC[2],  
        #                                Date            = datetime.datetime.now(),
        #                                Description     = "student notes",
        #                                Datelastwritten = datetime.datetime.now(),
        #                                User            = user.Id,
        #                                Type            = 'st',
        #                                Note            = cNote)
        
        #         db.session.add(note_to_create)
        #         db.session.commit()      
        #     else:
        #         print('updating note')
        #         print('user.Id: ', user.Id)
        #         print('cNote: ', cNote)

        #         note = Notes.query.where(and_((Notes.User == user.Id),(Notes.Type == 'st'))).first()
        #         x = db.session.query(Notes).get(note.Id)
        #         x.Note = cNote
        #         db.session.commit()      

        SaveNote(user.Id, 'st', cNote, 'replace')

        # -----------------------------------------------------------------------------      
        # process roles
        cUserStatus = ''
        nC = 0
        nR = 0
        for l in listStatus:
            value = request.form.get(eval('l.Name'))   # provided as checkboxes
            if value:
                cUserStatus = cUserStatus + l.Name + ' '
                nR = nR + 1
            nC = nC + 1

        if nR > 1:
            if 'new ' in cUserStatus:
                cUserStatus = cUserStatus.replace('new ', '')
                logtext('removed status new', 'i')

        # x.Status       = cUserStatus
        db.session.commit()

        lInstructorAfter = False
        cRolesAfter = cUserStatus
        cStatusNew = cRolesAfter

        #print('#### retrieving status')
        x = db.session.query(Users).get(x.Id)
        #print('#### ', x.Username, ' ', x.Status)
        #print('#### cUserStatus: ', cUserStatus)

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

        # print("#### ---------------------------------------------------------------")
        # print("#### before ", lInstructorBefore, ' ', cStatusOld)
        # print("#### after  ", lInstructorAfter,  ' ', cStatusNew)

        if not lInstructorBefore and not lInstructorAfter:
            x = db.session.query(Users).get(x.Id)
            x.Status = cStatusNew
            db.session.commit() 
            #print("#### changed status from " + chr(34) + cStatusOld + chr(34) + " to " + chr(34) + cStatusNew + chr(34))

        if lInstructorBefore and lInstructorAfter:
            x = db.session.query(Users).get(x.Id)
            x.Status = cStatusNew
            db.session.commit() 

        if lInstructorBefore and not lInstructorAfter:
            #print ('#### removing instructor from table instructors')

            #print('------------------------------------------------------------------------------')
            #print('')
            #print('#### x.Id:                                   ', x.Id, ' (User.Id)')
            dbquery = 'db.session.execute(db.select(Instructors).filter_by(User = x.Id)).scalar_one_or_none()'
            #print('#### ', datetime.datetime.today(), ' dbquery: ', dbquery)
            ## instructor = eval(dbquery)
            instructor = db.session.execute(db.select(Instructors.Id, Instructors.User, Instructors.Name).where(Instructors.User == x.Id)).all()
            nStaff = 0
            for i in instructor:
                #print('#### instructor [0]', i [0])
                #print('#### instructor [1]', i [1])
                #print('#### instructor [2]', i [2])
                nStaffUser = i [0]
                nStaffId   = i [1]
                #print('#### instructor.Name', instructor.Name)
            #print('#### nStaffUser: ', nStaffUser)
            #print('#### nStaffId:   ', nStaffId)
            instructor2 = []
            for i in instructor:
                instructor2.append(i)
            #for i in instructor2:
                #print('#### instructor2 [0]', instructor2 [0])
                #print('#### instructor2.Name', instructor2.Name)
            #print('#### type(instructor):   all   ', type(instructor))
            #print('#### len(instructor):    al    ', len(instructor))
            #print('#### type(instructor2):  all   ', type(instructor2))
            #print('#### len(instructor2):   all   ', len(instructor2))
            #print('')
            #print('')

            # instructor = db.session.execute(db.select(Instructors.Id, Instructors.User, Instructors.Name).where(Instructors.User == x.Id)).all()

            #print('nStaffId:   ', nStaffId)
            #print('nStaffUser: ', nStaffUser)

            current_datetime = datetime.datetime.now()
            nYearFrom  = current_datetime.year
            nMonthFrom = current_datetime.month
            nDayFrom   = current_datetime.day

            dbquery = 'db.session.execute(db.select(Appointments.Id, Appointments.User, Appointments.Product, Appointments.Part, Appointments.Date, Appointments.Assistants, Appointments.Staff).'
            dbquery = dbquery + 'where(and_(Appointments.Staff == nStaffUser),'
            dbquery = dbquery + '(Appointments.Date >= datetime.datetime(nYearFrom, nMonthFrom, nDayFrom) ))).all()'

            #print('#### ', datetime.datetime.today(), ' dbquery: ', dbquery)

            appointments = eval(dbquery)

            # appointments = db.session.execute(db.select(Appointments.Id, Appointments.User, Appointments.Product, Appointments.Part, Appointments.Date, Appointments.Notes, Appointments.Staff).where(Appointments.Staff == nStaffId )).all()

            #print('')
            #print('#### type(appointments):', type(appointments))
            #print('#### len(appointments): ', len(appointments))

            #for a in appointments:
                #print ('#### a: ', a[0], a[1], a[2], a[3],a[4],a[5])

            #print('------------------------------------------------------------------------------')
            
            #if appointments is None:
                #print('#### Appointments is None.')

            nStaff = 0
            appointments2 = [] 
            for a in appointments:
                #print('#### ', a [0], a [1], a[2], a[3], a[4], a[5], a[6])
                appointments2.append(a)

            #if appointments2 is None:
                #print('#### Appointments2 is None.')

            #print('')
            #print('------------------------------------------------------------------------------')
            #print('')

            for a in appointments2:
                print('#### ', a [0], a [1], a[2], a[3], a[4], a[5], a[6])
                nStaff = a [6]

            #print('#### nStaff:  ', nStaff)
            #print('')
            #print('------------------------------------------------------------------------------')
            #print('')

            #if appointments is not None:
            if nStaff > 0:
                print('#### appointments found for instructor')
                lRBAC = get_rbac(request.url_rule.endpoint)        
                return redirect(url_for('instructorsinfo', id = nStaffId ))

            #print ('#### saving new status')
            x = db.session.query(Users).get(x.Id)
            x.Status       = cUserStatus
            db.session.commit()
            x = db.session.query(Users).get(x.Id)
            #print('#### ', x.Username, ' ', x.Status)

            #print('')
            #print('------------------------------------------------------------------------------')
            #print('')
            dbquery = 'db.session.execute(db.select(Instructors).filter_by(User = x.Id)).scalar_one_or_none()'
            #print('#### ', datetime.datetime.today(), ' dbquery: ', dbquery)
            instructor = eval(dbquery)

            #print('')
            #print('------------------------------------------------------------------------------')
            #print('')
            #print ("#### instructor.Name: ", instructor.Name)
            #db.session.delete(instructor)
            instructor.Active = False
            db.session.commit()

        #lRBAC = get_rbac(request.url_rule.endpoint) 

        if not lInstructorBefore and lInstructorAfter:

            instructor = db.session.execute(db.select(Instructors).filter_by(User = x.Id)).scalar_one_or_none()

            #print('####')
            #print('#### type(instructor): ', type(instructor))

            if instructor is None:

                # adding new instructor

                #print ('#### adding instructor to table instructors')

                instructor_to_create = Instructors(User   = x.Id,
                                                   Name   = x.Firstname + " " + x.Lastname, 
                                                   Active = True)
                db.session.add(instructor_to_create)
                db.session.commit()

            else:

                # re-instating instructor status

                #print ('#### altering instructor in table instructors')
                #print ("#### instructor.Name: ", instructor.Name)
                # db.session.delete(instructor)
                instructor.Active = True
                db.session.commit()

            #print ('#### saving new status')
            x = db.session.query(Users).get(x.Id)
            x.Status       = cUserStatus
            db.session.commit()
            x = db.session.query(Users).get(x.Id)
            #print('#### ', x.Username, ' ', x.Status)

        #print('####')

        #print("#### ---------------------------------------------------------------")

        if cFrom == 'instructors':
            return redirect(url_for('instructors'))

        return redirect(url_for('users'))
    
    if form.errors != {}: # no errors?
        for err_msg in form.errors.values():
            flash(f'error: {err_msg}', category = 'danger')

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('userseditform2.html', form = form, user = user, listStatus = listStatus , lRBAC = lRBAC, cNote = cNote)

#------------------------------------------------------------------------------------------

##     ##  ######  ######## ########   ######  #### ##    ## ########  #######  
##     ## ##    ## ##       ##     ## ##    ##  ##  ###   ## ##       ##     ## 
##     ## ##       ##       ##     ## ##        ##  ####  ## ##       ##     ## 
##     ##  ######  ######   ########   ######   ##  ## ## ## ######   ##     ## 
##     ##       ## ##       ##   ##         ##  ##  ##  #### ##       ##     ## 
##     ## ##    ## ##       ##    ##  ##    ##  ##  ##   ### ##       ##     ## 
 #######   ######  ######## ##     ##  ######  #### ##    ## ##        #######  


@app.route('/usersinfo/<id>', methods = ['GET', 'POST'])
def usersinfo(id):

    logtext('usersinfo ' + str(id), 'i')

    if current_user.is_anonymous:
        logtext('anonymous','w')
        return (no_access_text())

    form = UsersInfoForm(id)

    #                                            0                1                  2                3               4                     5                  5                  7                   8                 9
    appointments = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name, Appointments.Assistants). \
                                order_by(Appointments.Date). \
                                where(Appointments.User == id). \
                                select_from(Appointments). \
                                join(Users, Appointments.User == Users.Id). \
                                join(Instructors, Appointments.Staff == Instructors.Id). \
                                join(Products, Appointments.Product == Products.Id) )
    user         = db.session.execute(db.select(Users).filter_by(Id=id)).scalar_one()
    #products    = db.session.execute(db.select(Products)).scalars()
    products     = Products.query.order_by(func.lower(Products.Productname)).where(Products.Active)
    assistants   = Users.query.filter(Users.Status.contains('assistant'))

    if form.validate_on_submit():
        logtext('validate_on_submit ' + str(id), 'i')

        if request.form.get('cancel') == 'cancel':
            # print('cancel')
            logtext('cancelled ' + str(id), 'i')

            return redirect(url_for('users'))           

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

        cDateFrom = request.form.get('datefrom')      # formatted input
        dt2 = datetime.datetime.strptime(cDateFrom, '%Y-%m-%d')
        nDateTo  = dt2 - timedelta(days = 7)

        cStatus = ''
        for p in products:

            value = request.form.get(eval('p.Productname'))    # from checkboxes

            if value:
                cStatus = cStatus + cDate + ' ' + p.Productname + '|'
                        
                parts = p.Parts

                #20240829 - MvW - adding '\' if necessary...
                if not parts[len(parts)-1] == ':':
                    parts = parts + ':|'

                part = ""
                t = 0

                # 20241108 - disabled adding all lessons
                # for b in parts:
                #     if b == ":":

                #         nDateTo  = nDateTo + timedelta(days = 7)
                #         nYearTo  = nDateTo.year  # nYearTo  = nDateTo.year
                #         nMonthTo = nDateTo.month # nMonthTo = nDateTo.month
                #         nDayTo   = nDateTo.day   # nDateTo.day + t

                #         date0 = datetime.datetime.combine(datetime.date(nYearTo, nMonthTo, nDayTo), datetime.time(20,00))
                #         A0 = Appointments(User = id, Product = p.Id, Part = part, Date = date0, Staff = 1, Assistants = '')
                #         db.session.add(A0)
                #         db.session.commit()
                #         part = ""
                #         t = t + 7
                #     else:
                #         part = part + b

                nDateTo  = nDateTo + timedelta(days = 7)
                nYearTo  = nDateTo.year  # nYearTo  = nDateTo.year
                nMonthTo = nDateTo.month # nMonthTo = nDateTo.month
                nDayTo   = nDateTo.day   # nDateTo.day + t

                parts = p.Parts
                nDivider = parts.find(":")
                if nDivider > 0:
                    part = parts[0:nDivider]
                else:
                    part = parts

                date0 = datetime.datetime.combine(datetime.date(nYearTo, nMonthTo, nDayTo), datetime.time(20,00))
                A0 = Appointments(User = id, Product = p.Id, Part = part, Date = date0, Staff = 1, Assistants = '')
                db.session.add(A0)
                db.session.commit()

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
        
        # products = db.session.execute(db.select(Products)).scalars()
        products     = Products.query.order_by(func.lower(Products.Productname)).where(Products.Active)

        lRBAC = get_rbac(request.url_rule.endpoint) 

        return render_template('usersinfo.html', form = form, user = user, appointments = appointments, products = products, lRBAC = lRBAC)
    
    cDateToday = datetime.datetime.today()

    lRBAC = get_rbac(request.url_rule.endpoint) 

    return render_template('usersinfo.html', form = form, user = user, appointments = appointments, products = products, cDateToday = cDateToday, lRBAC = lRBAC, assistants = assistants)

#------------------------------------------------------------------------------------------

##     ##  ######  ######## ########   ######  ##     ##    ###    #### ##       
##     ## ##    ## ##       ##     ## ##    ## ###   ###   ## ##    ##  ##       
##     ## ##       ##       ##     ## ##       #### ####  ##   ##   ##  ##       
##     ##  ######  ######   ########   ######  ## ### ## ##     ##  ##  ##       
##     ##       ## ##       ##   ##         ## ##     ## #########  ##  ##       
##     ## ##    ## ##       ##    ##  ##    ## ##     ## ##     ##  ##  ##       
 #######   ######  ######## ##     ##  ######  ##     ## ##     ## #### ######## 

@app.route('/usersmail/<id>')
def usersmail(id):

    logtext('usersmail', 'i')

    secrets = dotenv_values(".env")
    cMessage = ""

    if current_user.is_anonymous:
        logtext('anonymous','w')
        return (no_access_text())

    lRBAC = get_rbac(request.url_rule.endpoint) 

    if 'admin' in lRBAC[1]:

        user               = db.session.execute(db.select(Users).filter_by(Id=id)).scalar_one()
        cFullname          = user.Firstname + ' ' + user.Lastname
        cEmailaddress      = user.Emailaddress
        cFullname2         = cFullname.replace(' ', '_')

        # sender_email      = secrets['SMTP_USER']
        # password          = secrets['SMTP_PASSWORD']

        sender_email       = os.environ.get('_SMTP_USER_').replace(chr(34), '')
        password           = os.environ.get('_SMTP_PASSWORD_').replace(chr(34), '')
        # print('E-Mail: ', sender_email, password)
        cc_email           = "mvwilligen@gmail.com"
        bcc_email          = "mvwilligen@hotmail.com"
        receiver_email     = cEmailaddress

        cMessage = cMessage + "sender_email: " + sender_email + cCRLF
        cMessage = cMessage + "receiver_email: " + receiver_email + cCRLF
        cMessage = cMessage + "" + cCRLF

        message            = MIMEMultipart("alternative")
        message["Subject"] = "Appointments for " + cFullname
        message["From"]    = sender_email
        message["To"]      = receiver_email
        message["CC"]      = "cc@mwihosting.nl"
        message["BCC"]     = "mvwilligen@gmail.com"
        message["Subject"] = "Appointments for " + cFullname

        cMessageText = ""
        cMessageHtml = ""
        cMailbodyIn  = ""
        cMailbodySt  = ""

        cFilenameSt = "./Package/static/Internal/calendar_st_" + cFullname2 + ".html"
        cMessage = cMessage + "cFilenameSt: " + cFilenameSt + cCRLF
        if os.path.isfile(cFilenameSt):
            f = open(cFilenameSt, "r")
            cMessageHtmlSt = f.read()
            f.close()
            cMailbodySt = "student:" + cMessageHtmlSt        
            cFirstPart  = cMailbodySt[0:cMailbodySt.find('<!--BeginCut -->')]
            cLastPart   = cMailbodySt[cMailbodySt.find('<!--EndCut -->')+14:]
            cMailbodySt = cFirstPart + cLastPart
            cFirstPart  = cMailbodySt[0:cMailbodySt.find('<style>')]
            cLastPart   = cMailbodySt[cMailbodySt.find('</style>')+8:]
            cMailbodySt = cFirstPart + cLastPart
        else:
            print("file " + cFilenameSt + " not found.")

        cFilenameIn = "./Package/static/Internal/calendar_in_" + cFullname2 + ".html"
        cMessage = cMessage + "cFilenameIn: " + cFilenameIn + cCRLF
        if os.path.isfile(cFilenameIn):
            f = open(cFilenameIn, "r")
            cMessageHtmlIn = f.read()
            f.close()
            cMailbodyIn = "staff:" + cMessageHtmlIn
            cFirstPart  = cMailbodyIn[0:cMailbodyIn.find('<!--BeginCut -->')]
            cLastPart   = cMailbodyIn[cMailbodyIn.find('<!--EndCut -->')+14:]
            cMailbodyIn = cFirstPart + cLastPart
            cFirstPart  = cMailbodyIn[0:cMailbodyIn.find('<style>')]
            cLastPart   = cMailbodyIn[cMailbodyIn.find('</style>')+8:]
            cMailbodyIn = cFirstPart + cLastPart
        else:
            print("file " + cFilenameIn + " not found.")

        cMailbody = cMailbodyIn + "<br><br>" + cCRLF + cCRLF + cMailbodySt

        cMessage = cMessage + "len(cMailbody): " + str(len(cMailbody)) + cCRLF
        cMessage = cMessage + "" + cCRLF

        # print('cMailFilename: ', cMailFilename)

        # f = open(cMailFilename, "r")
        # cMessageHtml = f.read()
        # f.close()

        #print('')
        #print('before: ', len(cMailbody))
        # remove all from '<style>' until '</style>'


        # cFirstPart   = cMailbody[0:cMailbody.find('<style>')]
        # cLastPart    = cMailbody[cMailbody.find('</style>')+8:]

        # cMailbody = cFirstPart + cLastPart

        #print('after removing style part: ', len(cMailbody))
        # remove all from '<!--BeginCut -->' until '<!--EndCut -->'


        # cFirstPart = cMailbody[0:cMailbody.find('<!--BeginCut -->')]
        # cLastPart  = cMailbody[cMailbody.find('<!--EndCut -->')+14:]

        # cMailbody  = cFirstPart + cLastPart

        #print('after removing studentsmenu and instructorsmenu: ', len(cMailbody))

        cMessageText = cMailbody.replace('</td><td>','; ')
        cMessageText = strip_tags(cMessageText)   # .replace('student', 'staff'

        #print('after strip_tags: ', len(cMessageText))
        #print(cMessageText)
        #print('')

        #print('cMailbody:    ', cMailbody)
        #print('cMessageText: ', cMessageText)

        if len(cMailbody) > 0:

            #print('start sending mail')
            # Turn these into plain/html MIMEText objects
            part1 = MIMEText(cMessageText, "plain")
            part2 = MIMEText(cMailbody, "html")

            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            message.attach(part1)
            message.attach(part2)

            # Create secure connection with server and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("mail.mwihosting.nl", 465, context=context) as server:   #587
                server.login(sender_email, password)
                cResult = server.sendmail(sender_email, receiver_email, message.as_string())
                cMessage = cMessage + "cResult: " + str(cResult) + cCRLF
            #print('finished sending mail')

        #### if len(cMailfile) > 0:

    print(cMessage)

    lRBAC = get_rbac(request.url_rule.endpoint) 

    # return render_template(url_for('users'), lRBAC = lRBAC)
    return redirect(url_for('users'))

#------------------------------------------------------------------------------------------


##     ##  ######  ######## ########   ######  ##    ##  #######  ######## ########  ######  
##     ## ##    ## ##       ##     ## ##    ## ###   ## ##     ##    ##    ##       ##    ## 
##     ## ##       ##       ##     ## ##       ####  ## ##     ##    ##    ##       ##       
##     ##  ######  ######   ########   ######  ## ## ## ##     ##    ##    ######    ######  
##     ##       ## ##       ##   ##         ## ##  #### ##     ##    ##    ##             ## 
##     ## ##    ## ##       ##    ##  ##    ## ##   ### ##     ##    ##    ##       ##    ## 
 #######   ######  ######## ##     ##  ######  ##    ##  #######     ##    ########  ######  


@app.route('/usersnotes/<id>')
def usersnotes(id):

    logtext('usersnotes ' + str(id), 'i')

    print('--- usersnotes:' + str(id) + '-----------------------------------------------')
    #                                            0                1                  2                3               4                     5                  6                  7                   8                 9
    appointments = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name, Appointments.Assistants). \
                                order_by(Appointments.Date). \
                                where(Appointments.User == id). \
                                select_from(Appointments). \
                                join(Users, Appointments.User == Users.Id). \
                                join(Instructors, Appointments.Staff == Instructors.Id). \
                                join(Products, Appointments.Product == Products.Id) )

    user               = db.session.execute(db.select(Users).filter_by(Id=id)).scalar_one()
    cFullname          = user.Firstname + ' ' + user.Lastname
    logtext('usersinfo ' + cFullname, 'i')

    cText = "<h3>Notes " + cFullname + "</h3><br><br>"
    cCRLF = chr(13) + chr(10)

    #cText = cText + "<table style='border-top: 1pt solid white; border-bottom: 1pt solid white;'>" + cCRLF
    cText = cText + "<table>" + cCRLF

    for a in appointments:
        # print(a [6].strftime("&d-%m-%Y %H:%M"))

        cText = cText + "<tr style='border-top: 1pt solid white;'><td style='width:200px'>date</td><td style='width:400px'>" + a [6].strftime("%d-%m-%Y %H:%M") + "</td></tr>" + cCRLF
        cText = cText + "<tr><td>product</td><td>" + a[4] + " - " + a[5] + "</td></tr>" + cCRLF
        cText = cText + "<tr><td>instructor</td><td>" + a[8] + "</td></tr>" + cCRLF
        cText = cText + "<tr><td>Assistant</td><td>" + a[9] + "</td></tr>" + cCRLF
        # cText = cText + "<tr><td>&nbsp;</td><td></td></tr>" + cCRLF
        # cText = cText + "<tr><td>student</td><td>" + a[2] + " " + a[3] + "</td></tr>" + cCRLF
        cText = cText + "<tr style='border-top: 1pt solid white;'><td>&nbsp;</td><td></td></tr>" + cCRLF

        cNotes = GetNote(a[0], 'ap')   
        cNotes = cNotes.replace(chr(13) + chr(10), '<br>')

        cText = cText + "<tr><td colspan=2>" + cNotes + "</td></tr>" + cCRLF
        cText = cText + "<tr><td>&nbsp;</td><td></td></tr>" + cCRLF

    cText = cText + "<tr style='border-top: 1pt solid white;'><td>&nbsp;</td><td></td></tr>" + cCRLF
    cText = cText + "</table>"

    # cText = cFullname + '<br><br>'

    # for a in appointments:
    #     print(a [6].strftime("&d-%m-%Y %H:%M"))

    #     cText = cText + "----------------------------------------------------------------------------------------------------------------------<br>" + cCRLF
    #     cText = cText + "date: " + a [6].strftime("%d-%m-%Y %H:%M") + "<br>" + cCRLF
    #     cText = cText + "product: " + a[4] + " - " + a[5] + "<br>" + cCRLF
    #     cText = cText + "instructor: " + a[8] + "<br>" + cCRLF
    #     cText = cText + "----------------------------------------------------------------------------------------------------------------------<br>" + cCRLF

    #     cNotes = GetNote(a[0], 'ap')   

    #     cNotes = cNotes.replace(chr(13) + chr(10), '<br>')

    #     cText = cText + "<br>" + cNotes + "<br>" + "<br>"

    # cText = cText + "----------------------------------------------------------------------------------------------------------------------<br>" + cCRLF
    lRBAC = get_rbac(request.url_rule.endpoint) 

    return render_template('usersnotes.html', cText = cText , lRBAC = lRBAC)


##     ##  ######  ######## ########   ######  ########  ########   #######  ########  ##     ##  ######  ######## 
##     ## ##    ## ##       ##     ## ##    ## ##     ## ##     ## ##     ## ##     ## ##     ## ##    ##    ##    
##     ## ##       ##       ##     ## ##       ##     ## ##     ## ##     ## ##     ## ##     ## ##          ##    
##     ##  ######  ######   ########   ######  ########  ########  ##     ## ##     ## ##     ## ##          ##    
##     ##       ## ##       ##   ##         ## ##        ##   ##   ##     ## ##     ## ##     ## ##          ##    
##     ## ##    ## ##       ##    ##  ##    ## ##        ##    ##  ##     ## ##     ## ##     ## ##    ##    ##    
 #######   ######  ######## ##     ##  ######  ##        ##     ##  #######  ########   #######   ######     ##    

@app.route('/usersproductform2/<id>/<cFrom>/', methods=['GET', 'POST'])
def usersproduct2(id, cFrom):

    logtext('usersproduct2 ' + str(id) + 'from:' + cFrom, 'i')

    if current_user.is_anonymous:
        logtext('anonymous','w')
        return (no_access_text())

    form = UsersProductForm2(id)

    appointment = db.session.execute(db.select(Appointments).filter_by(Id=id)).scalar_one()

    user    = appointment.User
    product = appointment.Product

    nPrevUser = user

    #                                           0                1                  2                3               4                     5                  6                  7                   8                 9               10                    11
    appointments = db.session.execute(db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name, Instructors.Id, Appointments.Product, Appointments.Assistants). \
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

    assistants = Users.query.filter(Users.Status.contains('assistant'))

    if form.validate_on_submit():
        logtext('validate_on_submit ' + str(id), 'i')
        print('validate on submit')

        if request.form.get('cancel') == 'cancel':
            logtext('cancelled ' + str(id), 'i')
            print('cancelled')

            if cFrom == 'usersinfo':
                return redirect(url_for('usersinfo', id = nPrevUser))

            return redirect(url_for('users'))

        # print ('=================================================================')
        
        for a in filtered:
            cDate = chr(34) + 'date' + str(a [0]) + chr(34)
            cDateValue = request.form.get(eval(cDate))         # formatted input
            cTime = chr(34) + 'time' + str(a [0]) + chr(34)
            cTimeValue = request.form.get(eval(cTime))         # formatted input
            # print ('.')
            # print ('#### cDate: ', cDate , cDateValue)
            # print ('#### cTime: ', cTime , cTimeValue)
            cInstructor = chr(34) + 'instructor' + str(a [0]) + chr(34)
            cInstructorValue = request.form.get(eval(cInstructor))        # provided list
            cAssistant = chr(34) + 'assistant' + str(a [0]) + chr(34)
            cAssistantValue = request.form.get(eval(cAssistant))        # provided list
            # print ('#### cInstructor: ', cInstructor , cInstructorValue)
            # print ('.')

            nInstructor = 0
            for i in filtered2:
                if i.Name == cInstructorValue:
                    nInstructor = i.Id

            # print ('.')
            # print ('#### nInstructor: ', nInstructor)
            # print ('.')

            appointment = db.session.execute(db.select(Appointments).filter_by(Id=a [0])).scalar_one()
            dDate = datetime.datetime(int(cDateValue[0:4]), int(cDateValue[5:7]), int(cDateValue[8:10]), int(cTimeValue[0:2]), int(cTimeValue[3:5]))
            appointment.Date = dDate
            appointment.Staff = nInstructor
            appointment.Assistants = cAssistantValue
            db.session.commit()
        print ('=================================================================')

        #lRBAC = get_rbac(request.url_rule.endpoint)

        #users = Users.query.all()

        if cFrom == 'usersinfo':
            return redirect(url_for('usersinfo', id = nPrevUser))

        return redirect(url_for('users'))

    instructors = db.session.execute(db.select(Instructors.Id, Instructors.User, Instructors.Name).where(Instructors.Active).order_by(Instructors.Name))

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('usersproductform.html', form=form, instructors = filtered2, appointments = filtered, lRBAC = lRBAC, cInstructors = cInstructors, cOptions = cOptions, assistants = assistants)

#------------------------------------------------------------------------------------------

##     ##  ######  ######## ########   ######  ########  ########   #######  ########  ##     ##  ######  ########  ######  ##    ## ######## ##     ## ######## 
##     ## ##    ## ##       ##     ## ##    ## ##     ## ##     ## ##     ## ##     ## ##     ## ##    ##    ##    ##    ## ###   ## ##        ##   ##     ##    
##     ## ##       ##       ##     ## ##       ##     ## ##     ## ##     ## ##     ## ##     ## ##          ##    ##       ####  ## ##         ## ##      ##    
##     ##  ######  ######   ########   ######  ########  ########  ##     ## ##     ## ##     ## ##          ##     ######  ## ## ## ######      ###       ##    
##     ##       ## ##       ##   ##         ## ##        ##   ##   ##     ## ##     ## ##     ## ##          ##          ## ##  #### ##         ## ##      ##    
##     ## ##    ## ##       ##    ##  ##    ## ##        ##    ##  ##     ## ##     ## ##     ## ##    ##    ##    ##    ## ##   ### ##        ##   ##     ##    
 #######   ######  ######## ##     ##  ######  ##        ##     ##  #######  ########   #######   ######     ##     ######  ##    ## ######## ##     ##    ##    

@app.route('/usersproductnext/<id>/<cFrom>/', methods=['GET', 'POST'])
def usersproductnext(id, cFrom):

    logtext('usersproductsnext ' + str(id) + ' from:' + cFrom, 'i')


    print("id: ", id)

    if current_user.is_anonymous:
        logtext('anonymous','w')
        return (no_access_text())

    #                                          0                1                  2                3               4                     5                  6                  7                   8                 9               10                    11
    appointment = db.session.execute(db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name, Instructors.Id, Appointments.Product, Appointments.Assistants). \
                                order_by(Appointments.Date). \
                                filter(Appointments.Id == id). \
                                join(Users,       Appointments.User    == Users.Id). \
                                join(Instructors, Appointments.Staff   == Instructors.Id). \
                                join(Products,    Appointments.Product == Products.Id) ).one()

    print("type(appointment): ", type(appointment))

    form = UsersProductNext()

    user     = appointment.User
    nProduct = appointment.Product
    cPart    = appointment.Part
    print("user: ", user)
    print("cPart: ", cPart)

    nPrevUser = user

    cPart = appointment.Part

    # get parts from product
    product = db.session.execute(db.select(Products).filter_by(Id=nProduct)).scalar_one()

    cParts = product.Parts
    print("parts: " , cParts)

    nCurrentPart = cParts.find(cPart)

    print("nCurrentPart: ", nCurrentPart)
    cNextCurrentPart = cParts[nCurrentPart+len(cPart)+1:]
    print("cNextCurrentPart: ", cNextCurrentPart)
    nNextColon = cNextCurrentPart.find(":")
    print("nNextColon: ", nNextColon)
    if nNextColon > 0:
        cNextCurrentPart = cNextCurrentPart[:nNextColon]

    print("cNextCurrentPart: ", cNextCurrentPart)

    lTemp = cParts.split(":")

    aParts = []
    for l in lTemp:
        aParts.append([l, ""])

    #if cFrom == 'usersinfo':
    #    return redirect(url_for('usersinfo', id = nPrevUser))

    if form.validate_on_submit():
        logtext('validate_on_submit ' + str(id), 'i')

        print('validated')

        if request.form.get('cancel') == 'cancel':
            logtext('cancelled ' + str(id), 'i')
            print('cancel')

            if cFrom == 'usersinfo':
                return redirect(url_for('usersinfo', id = nPrevUser))

            return redirect(url_for('users'))

        cDateValue = request.form.get("date")         # formatted input
        cTimeValue = request.form.get("time")         # formatted input

        print("date: ", cDateValue, " time: ", cTimeValue)

        for a in aParts:
           cValue = chr(34) + "part-" + a[0] + chr(34)
           # print("cValue: ", cValue)
           cFormValue = request.form.get(eval(cValue))
           # print("cValue: ", cValue, " cFormValue: ", cFormValue)
           if cFormValue is not None:
                print("saving appointment")
                nYearTo   = int(cDateValue[0:4])
                nMonthTo  = int(cDateValue[5:7])
                nDayTo    = int(cDateValue[8:10])
                nHourTo   = int(cTimeValue[0:2])
                nMinuteTo = int(cTimeValue[3:5])
                print(nYearTo,"-", nMonthTo,"-", nDayTo," ", nHourTo,":", nMinuteTo)
                date0 = datetime.datetime.combine(datetime.date(nYearTo, nMonthTo, nDayTo), datetime.time(nHourTo,nMinuteTo))
                A0 = Appointments(User = user, Product = nProduct, Part = a[0], Date = date0, Staff = 1, Assistants = '')
                db.session.add(A0)
                db.session.commit()


        return redirect(url_for('usersinfo', id = nPrevUser))

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('usersproductnext.html', aParts = aParts , cNextCurrentPart = cNextCurrentPart, appointment = appointment, lRBAC = lRBAC, form=form)


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

    logtext('usersregisterform', 'i')

    form = UsersRegisterForm()

    if form.validate_on_submit():

        logtext('usersregisterform > form_is_validated', 'i')

        cDateToday        = datetime.datetime.today()
        cDate             = cDateToday.strftime("%d-%m-%Y")
        cTime             = cDateToday.strftime("%H:%M:%S")

        # source: https://stackoverflow.com/questions/3759981/get-ip-address-of-visitors-using-flask-for-python
        cInfo = 'date: ' + cDate + ', time: ' + cTime + ', ip:' + request.environ.get('HTTP_X_REAL_IP', request.remote_addr)   

        pw_hash = bcrypt.generate_password_hash(form.password1.data).decode('utf-8')

        cUsername     = form.username.data
        cFirstname    = form.firstname.data
        cLastname     = form.lastname.data
        cPhone        = form.phone.data
        cEmailaddress = form.username.data
        cPasswordhash = pw_hash

        user_to_create = Users( Username     = cUsername,
                                Firstname    = cFirstname,
                                Lastname     = cLastname,
                                Phone        = cPhone,
                                Emailaddress = cEmailaddress,
                                Passwordhash = cPasswordhash,
                                Active       = True,
                                Info         = cInfo,
                                Status       = "new" )

        logtext("usersregisterform > cInfo=" + cInfo, "i")

        logtext("add user:" + cUsername + "," + cFirstname + "," + cLastname + "," + cPhone,"i")

        db.session.add(user_to_create)
        db.session.commit()
        
        return redirect(url_for('users'))
   
    if form.errors != {}: # no errors?
        for err_msg in form.errors.values():
            flash(f'error: {err_msg}', category = 'danger')

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('usersregisterform.html', form=form , lRBAC = lRBAC)

# ---------------------------------------------------------------------------------------


from io import StringIO
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

#------------------------------------------------------------------------------------------
