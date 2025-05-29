
from Package import db
from Package import app
from Package.models import Appointments, Users, Instructors, Products
from flask import Flask, render_template, redirect, url_for, flash, request

from flask_login import current_user

from Package.functions import get_rbac, no_access_text

from Package.forms import AppointmentsEditForm, LoginForm, ProductsEditForm, ProductsUsersForm, ProductsNewForm, UsersRegisterForm, UsersInfoForm, UsersEditForm2, UsersProductForm2, AppointmentsDateForm2

import datetime
from datetime import timedelta

from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy import func, and_

from Package.functions import logtext
from Package.functions import myquery


#### ##    ##  ######  ######## ########  ##     ##  ######  ########  #######  ########   ######  
 ##  ###   ## ##    ##    ##    ##     ## ##     ## ##    ##    ##    ##     ## ##     ## ##    ## 
 ##  ####  ## ##          ##    ##     ## ##     ## ##          ##    ##     ## ##     ## ##       
 ##  ## ## ##  ######     ##    ########  ##     ## ##          ##    ##     ## ########   ######  
 ##  ##  ####       ##    ##    ##   ##   ##     ## ##          ##    ##     ## ##   ##         ## 
 ##  ##   ### ##    ##    ##    ##    ##  ##     ## ##    ##    ##    ##     ## ##    ##  ##    ## 
#### ##    ##  ######     ##    ##     ##  #######   ######     ##     #######  ##     ##  ######  

@app.route('/instructors')
def instructors():

    logtext('/instructors', 'i')

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

    logtext('/instructorsinfo id:' + str(id), 'i')

    if current_user.is_anonymous:
        return (no_access_text())

    instructor = db.session.execute( db.select(Instructors.Id, Instructors.User, Instructors.Name). \
                                order_by(Instructors.Name). \
                                where(Instructors.Id == id).\
                                select_from(Instructors). \
                                join(Users, Instructors.User    == Users.Id) )

    instructor2 = []

    # export data in csv-format
    cCSV = ""

    for row in instructor:

        instructor2.append(row)

        # for element in row:
        #     if isinstance(element, int):
        #         cCSV = cCSV + str(element) + "; "
        #     elif isinstance(element, datetime.date):
        #         cCSV = cCSV + element.strftime("%d-%m-%Y") + "; "
        #     elif isinstance(element, datetime.datetime):
        #         cCSV = cCSV + element.strftime("%d-%m-%Y") + "; "
        #     else:
        #         cCSV = cCSV + element + "; "
        # cCSV = cCSV + '#BR#'

    #                                            0                1                  2                3               4                    5                   6                  7                   8                 9                   10
    appointments = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name, Instructors.Active, Appointments.Assistants). \
                                order_by(Appointments.Date). \
                                select_from(Appointments). \
                                where(Appointments.Staff == id). \
                                join(Users,       Appointments.User == Users.Id). \
                                join(Instructors, Appointments.Staff == Instructors.Id). \
                                join(Products,    Appointments.Product == Products.Id) )

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('instructorsinfo.html', instructor = instructor2, appointments = appointments , lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

