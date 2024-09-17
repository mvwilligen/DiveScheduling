
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
from Package.functions import get_rbac, no_access_text, string2safe

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

    if False:
        user = Users.query.filter_by(Username='Laura')

        print('type(user): ', type(user))
        # print('len(user): ', len(user)) # TypeError: object of type 'Query' has no len()

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

        print('')
        print('type(user): ', type(user))
        print('user: ', user)
        print('')

        print('------------------------------------------------------')
        print('first pass')
        cUsername = ""
        for u in user:
            cUsername = u.Username
            print (u.Username)
        print('cUsername: ', cUsername)

        print('------------------------------------------------------')
        print('second pass')
        cUsername = ""
        for u in user:
            cUsername = u.Username
            print (u.Username)
        print('cUsername: ', cUsername)

        print('===========================================================================')

    print('')
    strings = []
    strings.append("<b>Martin</b>")
    strings.append("Martin")
    strings.append("<>,;:[]{}|()*&^%$#!=+~")

    for s in strings:
        print('string2safe(' + s + '): ', string2safe(s))

    print('')

    lRBAC = get_rbac('')

    return render_template('home.html', lRBAC = lRBAC)