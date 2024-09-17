
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
from sqlalchemy import func, and_

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

    print('type(user): ', type(user))

    cUsername = ""
    for u in user:
        cUsername = u.Username
        print (u.Username)
    print('cUsername: ', cUsername)
    print('---------------------')

    cText = 'Laura Maissan'
    # cFirstPart   = cMessageHtml[0:cMessageHtml.find('<style>')]
    cFirstname = cText[0:cText.find(' ')]
    print('cFirstname: [' + cFirstname + ']')
    cLastname = cText[cText.find(' ')+1:]
    print('cLastname:  [' + cLastname + ']')

    user = Users.query.filter(and_((Users.Firstname == cFirstname), (Users.Lastname == cLastname)))

    cUsername = ""
    for u in user:
        cUsername = u.Username
        print (u.Username)
    print('cUsername: ', cUsername)

    print('===========================================================================')

    return render_template('home.html')