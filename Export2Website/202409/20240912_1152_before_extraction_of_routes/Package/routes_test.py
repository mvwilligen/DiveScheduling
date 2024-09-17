
######## ########  ######  ######## 
   ##    ##       ##    ##    ##    
   ##    ##       ##          ##    
   ##    ######    ######     ##    
   ##    ##             ##    ##    
   ##    ##       ##    ##    ##    
   ##    ########  ######     ##    


from Package import db
from Package import app
from Package.models import Appointments, Users, Instructors, Products
from flask import Flask, render_template, redirect, url_for, flash, request


@app.route('/test/')
def test():

    # inspiration: https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application#step-4-displaying-a-single-record
    
    print('===========================================================================')
    print('')
    print('######## ########  ######  ######## ')
    print('   ##    ##       ##    ##    ##    ')
    print('   ##    ##       ##          ##    ')
    print('   ##    ######    ######     ##    ')
    print('   ##    ##             ##    ##    ')
    print('   ##    ##       ##    ##    ##    ')
    print('   ##    ########  ######     ##    ')
    print('')

    user = Users.query.filter_by(Username='Laura')

    for u in user:
        print (u.Username)

    print('===========================================================================')

    return render_template('home.html')