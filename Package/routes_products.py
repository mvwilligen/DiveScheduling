
from Package import db
from Package import app
from Package.models import Appointments, Users, Instructors, Products
from flask import Flask, render_template, redirect, url_for, flash, request

from flask_login import current_user

from Package.functions import get_rbac, no_access_text, GetNote, SaveNote, string2safe

from Package.forms import AppointmentsEditForm, LoginForm, ProductsEditForm, ProductsUsersForm, ProductsNewForm, UsersRegisterForm, UsersInfoForm, UsersEditForm2, UsersProductForm2, AppointmentsDateForm2

import datetime
from datetime import timedelta

from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy import func, and_



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

    cNote = GetNote(product.Id, 'pr')
    form.note.data = cNote

    if form.validate_on_submit():

        x = db.session.query(Products).get(id)
        x.Date        = string2safe(request.form["abbr"])
        x.Parts       = string2safe(request.form["parts"].replace('|',':'))
        x.Description = string2safe(request.form["description"] )
        db.session.commit()

        cNote         = string2safe(request.form["note"])
        SaveNote(product.Id, 'pr', cNote, 'replace')

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

        newproductname = string2safe(request.form["productname"].replace(' ', '_'))

        product_to_create = Products(Productname = newproductname,
                                     Abbr        = string2safe(request.form["abbr"]),
                                     Parts       = string2safe(request.form["parts"].replace('|',':')),
                                     Description = string2safe(request.form["description"]))
         
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

