
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

import os

from dotenv import dotenv_values
import glob
from ftplib import FTP


#------------------------------------------------------------------------------------------

##     ## ######## ##     ## ##       
##     ##    ##    ###   ### ##       
##     ##    ##    #### #### ##       
#########    ##    ## ### ## ##       
##     ##    ##    ##     ## ##       
##     ##    ##    ##     ## ##       
##     ##    ##    ##     ## ######## 

@app.route('/html/')
def html():

    if current_user.is_anonymous:
        return (no_access_text())

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('htmlexport.html', lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

##     ## ######## ##     ## ##       ######## ##     ## ########   #######  ########  ######## 
##     ##    ##    ###   ### ##       ##        ##   ##  ##     ## ##     ## ##     ##    ##    
##     ##    ##    #### #### ##       ##         ## ##   ##     ## ##     ## ##     ##    ##    
#########    ##    ## ### ## ##       ######      ###    ########  ##     ## ########     ##    
##     ##    ##    ##     ## ##       ##         ## ##   ##        ##     ## ##   ##      ##    
##     ##    ##    ##     ## ##       ##        ##   ##  ##        ##     ## ##    ##     ##    
##     ##    ##    ##     ## ######## ######## ##     ## ##         #######  ##     ##    ##    

@app.route('/htmlexport/')
def htmlexport():

    aSpecialDates = []
    aSpecialDates.append(['18-08-2024', 'Hello World!'])
    aSpecialDates.append(['05-12-2024', 'St. Nicholas'])
    aSpecialDates.append(['25-12-2024', 'Christmas'])
    aSpecialDates.append(['26-12-2024', 'Christmas'])
    aSpecialDates.append(['31-12-2024', 'Old Year'])
    aSpecialDates.append(['01-01-2025', 'New Year'])
    aSpecialDates.append(['14-03-2025', 'Pi Day'])
    aSpecialDates.append(['29-03-2025', 'Good Friday'])
    aSpecialDates.append(['31-03-2025', 'Easter'])
    aSpecialDates.append(['01-04-2025', 'Easter'])
    aSpecialDates.append(['27-04-2025', 'Kings Day'])
    aSpecialDates.append(['04-05-2025', 'Star Wars Day'])
    aSpecialDates.append(['05-05-2025', 'Freedom Day'])
    aSpecialDates.append(['09-05-2025', 'Ascension Day'])
    aSpecialDates.append(['19-05-2025', 'Pentecost'])
    aSpecialDates.append(['20-05-2025', 'Pentecost'])
    aSpecialDates.append(['22-07-2025', 'Martin'])
    aSpecialDates.append(['18-08-2024', ':-)'])
    aSpecialDates.append(['05-12-2024', 'St. Nicholas'])
    aSpecialDates.append(['25-12-2025', 'Christmas'])
    aSpecialDates.append(['26-12-2025', 'Christmas'])
    aSpecialDates.append(['31-12-2025', 'Old Year'])
    aSpecialDates.append(['01-01-2026', 'New Year'])
    aSpecialDates.append(['14-03-2026', 'Pi Day'])
    aSpecialDates.append(['27-04-2026', 'Kings Day'])
    aSpecialDates.append(['04-05-2026', 'Star Wars Day'])
    aSpecialDates.append(['05-05-2026', 'Freedom Day'])
    aSpecialDates.append(['22-07-2026', 'Martin'])
    aSpecialDates.append(['18-08-2026', ':-)'])
    aSpecialDates.append(['05-12-2026', 'St. Nicholas'])
    aSpecialDates.append(['25-12-2026', 'Christmas'])
    aSpecialDates.append(['26-12-2026', 'Christmas'])
    aSpecialDates.append(['31-12-2026', 'Old Year'])
    aSpecialDates.append(['01-01-2027', 'New Year'])
    aSpecialDates.append(['14-03-2027', 'Pi Day'])
    aSpecialDates.append(['27-04-2027', 'Kings Day'])
    aSpecialDates.append(['04-05-2027', 'Star Wars Day'])
    aSpecialDates.append(['05-05-2027', 'Freedom Day'])
    aSpecialDates.append(['22-07-2027', 'Martin'])
    aSpecialDates.append(['18-08-2027', ':-)'])
    aSpecialDates.append(['05-12-2027', 'St. Nicholas'])
    aSpecialDates.append(['25-12-2027', 'Christmas'])
    aSpecialDates.append(['26-12-2027', 'Christmas'])
    aSpecialDates.append(['31-12-2027', 'Old Year'])

    cCRLF = chr(13) + chr(10)
    cCRLF = chr(10)

    from calendar import monthrange

    cWhiteSpace = "" # "&nbsp;&nbsp;&nbsp;"

    nStartTime = datetime.datetime.today()

    cDateToday = datetime.datetime.today()
    cDate2     = cDateToday.strftime("%d-%b-%Y")
    cDate4     = cDateToday.strftime("%Y%m%d")
    cDate5     = cDateToday.strftime("%d-%m-%Y")
    cTime      = cDateToday.strftime("%H%M")
    cTime2     = cDateToday.strftime("%H:%M")

    dDateFrom  = datetime.date.today() - timedelta(days=14)
    dDateTo    = datetime.date.today() + timedelta(92)
    dDateTo    = datetime.date.today() + timedelta(int(4 * 30.5))

    nYearFrom  = dDateFrom.year
    nMonthFrom = dDateFrom.month  
    nYearTo    = dDateTo.year
    nMonthTo   = dDateTo.month

    print('nYearFrom:  ', nYearFrom)
    print('nMonthFrom: ', nMonthFrom)
    print('nYearTo:    ', nYearTo)
    print('nMonthTo:   ', nMonthTo)
    
    if nMonthTo < nMonthFrom:
        nMonthTo = nMonthTo + 12

    # necessary for links in html files?
    # there is no folder structure?
    ##cFolderNameOS   = './Exports/divescheduling_' + cDate4 + '_' + cTime + '/'
    ##cFolderNameHtml = '../divescheduling_' + cDate4 + '_' + cTime + '/'
    cFolderNameOS   = ''
    cFolderNameHtml = ''

    print("--[exporthtml]--------------------------------------------------------------------")

    lMonthNames = ['','January','February','March','April','May','June','July','August','September','October','November','December']
    lDayNames   = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    cStyle = '<style>' + cCRLF
    cStyle = cStyle + 'td { text-align:left; vertical-align:top; padding-left:5px;padding-right:5px;padding-bottom:5px;padding-top:5px;' + cCRLF
    cStyle = cStyle + 'font-family:verdana; }' + cCRLF
    cStyle = cStyle + 'table { border-collapse: collapse; }' + cCRLF
    cStyle = cStyle + 'a, p, h3 {font-family:verdana;}' + cCRLF
    cStyle = cStyle + 'table, th, td { border: 1px solid};' + cCRLF
    cStyle = cStyle + '</style>' + cCRLF
    cStyle = cStyle + '' + cCRLF

    cHead = "<head><link rel='icon' type='image/x-icon' href='favicon.ico'></head>" + cCRLF

    cHtmlCal = '<html>' + cHead + cStyle + '<body>[cInstructorsMenu]<br>' + cCRLF

    # start instructorsmenu with link to calendar
    #cInstructorsMenu = "<a href=" + cFolderNameHtml + "calendar_" + cDate4 + "_" + cTime + ".html>Calendar</a>"
    cInstructorsMenu = ""

    # 'prefill' for week height
    cWeekLines = "" # "<br><br><br><br><br><br>"

    nYear = nYearFrom

    # repair an unknown issue with same years in range
    nAddYear = 0
    if nYearFrom == nYearTo:
        nAddYear = 1

    aInstructor     = []
    aHtmlFiles      = []
    nInstructor     = 0
    aStudentHtml    = []
    cStudentMenu    = ''
    nStudent        = 0
    cAssistantsMenu = ''

    for nYears in range(nYearFrom, nYearTo + nAddYear):

        print('processing year: ', nYear)

        for nMonths in range(nMonthFrom, nMonthTo):

            if nMonths > 12:
                nMonth = nMonths - 12
                nYear = nYearFrom + 1
            else:
                nMonth = nMonths

            if True:
                print('processing month: ', nMonth)

                cHtmlCal = cHtmlCal + "<table><tr><td colspan=8 style='text-align: center;'><h3 style='margin-bottom: 0;'>" + lMonthNames [nMonth] + " " + str(nYear) + "</h3></td></tr>" + cCRLF
                cHtmlCal = cHtmlCal + '<tr><td><b>week' + cWhiteSpace + '</b></td>' + cCRLF

                # table header with daynames
                for n in lDayNames:
                    cHtmlCal = cHtmlCal + "<td style='width:200px'><b>" + n + cWhiteSpace + "</b></td>" + cCRLF

                cHtmlCal = cHtmlCal + '</tr>' + cCRLF

                lResult = monthrange(nYear, nMonth)

                nFirstDay = lResult [0]
                nLastDay  = lResult [1]

                # weeknumber
                nDay = 1
                cWeekNumber = datetime.date(int(nYear), int(nMonth), int(nDay)).strftime('%V')
                cWeekNumber = str(int(cWeekNumber) - 1)
                cHtmlCal = cHtmlCal + "<tr><td style='height:150px'>" + str(cWeekNumber) + cWeekLines + "</td>"

                cWhiteSpace2 = ""

                cHtmlCal = cHtmlCal + '<!-- new month -->' + cCRLF

                # add before cells to table
                for nDay in range(nFirstDay):
                    cHtmlCal = cHtmlCal + '<td></td>' + cCRLF

                cHtmlCal = cHtmlCal + '<!-- new week -->' + cCRLF

                for nDays in range(nLastDay):
                    cHtmlDat = ''

                    # correct 0-based range
                    nDay = nDays + 1

                    #print('processing: ', nYear, nMonth, nDay)

                    cProducts = ''
                    nDayOfWeek = (nDay + nFirstDay - 1) % 7
                    
                    cDate = str(nDay).rjust(2, '0') + '-' + str(nMonth).rjust(2,'0') + '-' + str(nYear) 

                    cSpecialDate = ''
                    for d in aSpecialDates:
                        if d [0] == cDate:
                            cSpecialDate = '<p style="color:gray;font-family:courier;font-size:75%;display:inline;">' + ' '  + d [1] + '</p>' + cCRLF

                    cDate = str(nYear) + '-' + str(nMonth).rjust(2,'0') + '-' + str(nDay + 1).rjust(2, '0')

                    cHtmlCal = cHtmlCal + '<td>' + str(nDay) + cSpecialDate + '<br>'
                    
                    dDate = datetime.date(nYear, nMonth, nDay)
                    #                                           0                1                  2                3               4                     5                  6                  7                   8                 9               10                    11
                    appointments = db.session.execute(db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date, Appointments.Staff, Instructors.Name, Instructors.Id, Appointments.Product, Appointments.Assistants). \
                                   where(func.date(Appointments.Date) == dDate). \
                                   order_by(Appointments.Product). \
                                   join(Users,       Appointments.User    == Users.Id). \
                                   join(Instructors, Appointments.Staff   == Instructors.Id). \
                                   join(Products,    Appointments.Product == Products.Id) )

                    cOldProduct = ''

                    cHtmlIns = ''

                    cDate3 = str(nYear) + str(nMonth).rjust(2,'0') + str(nDay + 1).rjust(2, '0')

                    cEmptyTR = ''

                    cAddHtmlHeader = "<tr><td style='width:200px'><b>date</b></td><td style='width:200px'><b>product</b></td><td style='width:200px'><b>part</b></td><td style='width:200px'><b>student</b></td><td style='width:200px'><b>instructor</b></td><td style='width:200px'><b>assistant</b></td></tr>" + cCRLF

                    for a in appointments:
 
                        # date html
                        cDateline = "<tr><td>" + a [6].strftime('%d-%m-%Y %H:%M') + "</td><td>" + a[4] + "</td><td>" + a[5] + "</td><td>"  + a[2] + " " + a[3] + "</td><td>" + a[8] + "</td><td>" + a[11] + "</td>" + cCRLF
                        cHtmlDat = cHtmlDat + cDateline

                        #---------------------------------------
                        # process student info

                        nFound = 0
                        nCounter = 0
                        for i in aStudentHtml:
                            nCounter = nCounter + 1
                            if i [1] == a [1]:
                                nFound = nCounter

                        # html student
                        cAddHtmlLine = "<tr><td>" + a [6].strftime("%d-%m-%Y %H:%M") + "</td><td>" + a [4] + "</td><td>" + a [5] + "</td><td>" + a [2] + " " + a [3] + "</td><td>" + a [8] + "</td><td>" + a [11] + "</td></tr>" + cCRLF

                        if nFound == 0:
 
                            nStudent = nStudent + 1
                            aStudentHtml.append([nStudent, a [1], a [2] + ' ' + a [3], cAddHtmlHeader + cAddHtmlLine])

                            cStudentName = a [2] + " " + a [3]
                            if not cStudentName in cStudentMenu:
                                cStudentMenu = cStudentMenu + ";<a href=" + cFolderNameHtml + "calendar_st_" + cStudentName.replace(' ', '_') + ".html>" + cStudentName + "</a>"

                        else:
 
                            aStudentHtml [nFound-1][3] = aStudentHtml [nFound-1][3] + cAddHtmlLine

                        #---------------------------------------
                        # process instructor info
                        nFound = 0
                        nCounter = 0
                        for i in aInstructor:
                            nCounter = nCounter + 1
                            if i [1] == a [9]:
                                nFound = nCounter
 
                        # html instructor
                        cAddHtmlIns = "<tr><td>" + a [6].strftime("%d-%m-%Y %H:%M") + "</td><td>" + a [4] + "</td><td>" + a [5] + "</td><td>" + a [2] + " " + a [3] + "</td><td>" + a [8] + "</td><td>" + a [11] + "</td></tr>" + cCRLF

                        if nFound == 0:
                            nInstructor = nInstructor + 1

                            aInstructor.append([nInstructor, a [9], a [8], cAddHtmlHeader + cAddHtmlIns])

                            if not a [8] in cInstructorsMenu:
                                cInstructorsMenu = cInstructorsMenu + ";<a href=" + cFolderNameHtml + "calendar_in_" + a [8].replace(' ', '_') + ".html>" + a [8] + "</a>"

                            cEmptyTR = cEmptyTR + '|'+ str(a[9]) + '|'

                        else:
 
                            aInstructor [nFound - 1][3] = aInstructor [nFound - 1][3] + cAddHtmlIns

                            cEmptyTR = cEmptyTR + '|'+ str(a[9]) + '|'
                        
                        #---------------------------------------
                        # process assistant info

                        if len(a[11]) > 0:
                            print('-----------------------------------------------------')
                            print('process assistant info')

                            cText = a[11]
                            cFirstname = cText[0:cText.find(' ')]
                            print('cFirstname: [' + cFirstname + ']')
                            cLastname = cText[cText.find(' ')+1:]
                            print('cLastname:  [' + cLastname + ']')

                            user = Users.query.filter(and_((Users.Firstname == cFirstname), (Users.Lastname == cLastname)))

                            cUsername = ""

                            for u in user:
                                cUsername = u.Username
                                print ('Found: ', u.Username)
                                cStatus = u.Status

                            print('cUsername: ' + cUsername + ' [' + cStatus + ']')

                            if 'instructor' in cStatus:
                                print (cText + ' is an instructor.')

                                instructor = Instructors.query.filter(Instructors.Name == cText)
                                
                                nId = 0
                                for i in instructor:
                                    if i.Name == cText:
                                        print('i.Name: ', i.Name)
                                        nId = i.Id

                                if not cText in cInstructorsMenu:
                                    print('not in cInstructorsMenu')
                                    nInstructor = nInstructor + 1
                                    aInstructor.append([nInstructor, nId, cText, cAddHtmlHeader + cAddHtmlIns])

                                    cInstructorsMenu = cInstructorsMenu + ";<a href=" + cFolderNameHtml + "calendar_in_" + cText.replace(' ', '_') + ".html>" + cText + "</a>"

                                    for i in aInstructor:
                                        print('    i: ', i[0], i[1], i[2])

                                else:

                                    # search instructor in list
                                    nFound = 0
                                    print('nId: ', nId)
                                    for i in aInstructor:
                                        nCounter = nCounter + 1
                                        print('i: ', i[0], i[1], i[2])
                                        if i[1] == nId:
                                            print('found: ', i[1], nId, nCounter)
                                            nFound = i[0]

                                    if nFound > 0:
                                        print('nFound: ', nFound)
                                        aInstructor [nFound - 1][3] = aInstructor [nFound - 1][3] + cAddHtmlIns
                                    else:
                                        print('#### issue with finding assistant in list instructors')
                            else:
                                print ('#### ' + cText + ' is NOT an instructor.')

                                nFound = 0
                                print('cText: ', cText)
                                for i in aInstructor:
                                    nCounter = nCounter + 1
                                    print('i: ', i[0], i[1], i[2])
                                    if i[2] == cText:
                                        print('found: ', i[2], cText, nCounter)
                                        nFound = i[0]

                                if nFound > 0:
                                    print('nFound: ', nFound)
                                    aInstructor [nFound - 1][3] = aInstructor [nFound - 1][3] + cAddHtmlIns
                                else:
                                    print(cText + ' is not found in list instructors')
                                    aInstructor.append([nCounter, -1, cText, cAddHtmlHeader + cAddHtmlIns])

                                    if not cText in cInstructorsMenu:
                                        cInstructorsMenu = cInstructorsMenu + ";<a href=" + cFolderNameHtml + "calendar_in_" + cText.replace(' ', '_') + ".html>" + cText + "</a>"
                            
                            print('-----------------------------------------------------')


                        #---------------------------------------

                        # check if product is already in calendar (for this date)
                        if not a [4] in cProducts:
                            cHtmlCal = cHtmlCal + cCRLF + '<a href=' + cFolderNameHtml + 'calendar_da_' + cDate3 + '.html>' + a [4] + '</a><br>' + cCRLF
                            cProducts = cProducts + a [4] + '|'

                    #### for a in appointments:

                    # add empty row in instructor table
                    for i in aInstructor:
                        if '|' + str(i [1]) + '|' in cEmptyTR: 
                            i [3] = i [3] + "<tr><td colspan = 6>&nbsp;</td></tr>"
                    
                    # end of week
                    if nDayOfWeek == 6:
                        cWhiteSpace2 = ''
                        cHtmlCal = cHtmlCal + '</tr>'
                        if nDay != nLastDay:
                            # weeknumber
                            # print('#### ', nYear, nMonth, nDay)
                            cHtmlCal = cHtmlCal + '<!-- new week -->' + cCRLF
                            cHtmlCal = cHtmlCal + "<tr><td style='height:150px'>" + str(datetime.date(int(nYear), int(nMonth), int(nDay)).strftime('%V')) + cWeekLines + "</td>" + cCRLF

                    if len(cHtmlDat) > 0:
                        # date html
                        cHtmlDat2 = '<html>' + cHead + cStyle + '<body>[cInstructorsMenu]<br><br><table>' + cCRLF

                        cWeekdayName = lDayNames[datetime.date(nYear, nMonth, nDay).weekday()]

                        cHtmlDat2 = cHtmlDat2 + "<tr><td colspan=6 style='text-align: center;'><h3 style='margin-bottom: 0;'>" + str(nDay) + " " + lMonthNames[nMonth] + " " + str(nYear) + " - " + cWeekdayName + "</h3></td></tr>" + cCRLF
                        cHtmlDat2 = cHtmlDat2 + "<tr><td style='width:200px'><b>time</b></td><td style='width:200px'><b>product</b></td><td style='width:200px'><b>part</b></td><td style='width:200px'><b>student</b></td><td style='width:200px'><b>instructor</b></td><td style='width:200px'><b>assistant</b></td><tr>" + cCRLF
                        cHtmlDat2 = cHtmlDat2 + cHtmlDat + cCRLF
                        cHtmlDat2 = cHtmlDat2 + '</table>' + cCRLF

                        cFileName = cFolderNameOS + '/calendar_da_' + cDate3 + '.html'

                        aHtmlFiles.append([cFileName, cHtmlDat2])
                
                #### for nDay in range(nLastDay):

                # after cells
                nCounter = 1    
                for nDay in range(nDayOfWeek + 1, 7):
                    #print('----'.ljust(17), end='')
                    cHtmlCal = cHtmlCal + '<td>' + '</td>'
                    nCounter = nCounter + 1

                cHtmlCal = cHtmlCal + '</tr></table><br><br>' + cCRLF

        #### for nMonth in range(12):

    #### for nYear in range(nYearFrom, nYearTo):

    #------------------------------------------------------------------------------
    # split students to list
    newList = list(cStudentMenu.split(";"))

    # sort list
    sortedList = sorted(newList)

    print('')
 
    cNewStudentMenu = ''
 
    for n in sortedList:
        cNewStudentMenu = cNewStudentMenu + ' ' + n + cCRLF

    cStudentMenu = cNewStudentMenu + '<br>'

    #------------------------------------------------------------------------------
    # split instructors to list
    cAllMenus = cAssistantsMenu + cInstructorsMenu
    newList = list(cAllMenus.split(";"))

    # sort list
    sortedList = sorted(newList)
 
    cNewInstructorsMenu = ''
 
    for n in sortedList:
        cNewInstructorsMenu = cNewInstructorsMenu + ' ' + n + cCRLF

    #------------------------------------------------------------------------------

    cInstructorsMenu = cNewInstructorsMenu + '<br>'

    for i in aStudentHtml:

        # replace spaces in instructorname with underscores for filename
        cInsName = i[2].replace(' ', '_')

        cFileName = cFolderNameOS + '/calendar_st_' + cInsName + '.html'
        cHtmlIns = "<html>" + cHead + cStyle + "<body>[cInstructorsMenu]<br><br><table><tr><td colspan=6 style='text-align: center;'><h3 style='margin-bottom: 0;'>" + i [2] + "</h3></td></tr>" + i [3] + "</table>"
        aHtmlFiles.append([cFileName, cHtmlIns])

    for i in aInstructor:

        # replace spaces in instructorname with underscores for filename
        cInsName = i [2].replace(' ', '_')

        cFileName = cFolderNameOS + '/calendar_in_' + cInsName + '.html'
        cHtmlIns = "<html>" + cHead + cStyle + "<body>[cInstructorsMenu]<br><br><table><tr><td colspan=6 style='text-align: center;'><h3 style='margin-bottom: 0;'>" + i [2] + "</h3></td></tr>" + i [3] + "</table>"
        aHtmlFiles.append([cFileName, cHtmlIns])

    # add Calendar html to html list
    cFileName = cFolderNameOS + '/calendar_' + cDate4 + '_' + cTime + '.html'
    aHtmlFiles.append([cFileName, cHtmlCal])
    aHtmlFiles.append(['index.html', cHtmlCal])

    cHtmlCalendar = cHtmlCal

    cHeader =           "<!--BeginCut --><table style='border-style: hidden;'><tr><td style='border:none;'>" + cCRLF
    cHeader = cHeader + "<a href='http://127.0.0.1:5000/'><img src='logo.png' alt='ds'></a></td><td style='border:none;'>" + cCRLF
    cHeader = cHeader + "<a href='index.html'><img src='calendar.png' alt='calendar' width='60' height='60'></a></td>" + cCRLF
    cHeader = cHeader + "<td style='border:none;'>" + cCRLF
    cHeader = cHeader + cInstructorsMenu + cCRLF
    cHeader = cHeader + '<br>' + cCRLF
    cHeader = cHeader + cStudentMenu + cCRLF
    cHeader = cHeader + "</td></tr></table><p style='font-size: 10px;'>created: " + cDate5 + " " + cTime2 + "</p><br><!--EndCut -->" + cCRLF

    cFooterHtml = "<br><br>" + cCRLF +"<p style='font-size: 12px;'>powered by divescheduling. created: " + cDate5 + " " + cTime2 + "</p></body></html>"

    cFolderNameOSHtmlDay  = './Exports/' + cDate4 + '/'
    cFolderNameOSHtml     = './Exports/' + cDate4+ '/divescheduling_' + cDate4 + '_' + cTime + '/'
    cFolderNameOSMail     = './Exports/Mail/'
    cFolderNameOSInternal = './Exports/Internal/'

    if not os.path.exists('Exports'):
        os.makedirs('Exports') 

    if not os.path.exists(cFolderNameOSHtmlDay):
        os.makedirs(cFolderNameOSHtmlDay) 

    if not os.path.exists(cFolderNameOSHtml):
        os.makedirs(cFolderNameOSHtml) 

    if not os.path.exists(cFolderNameOSInternal):
        os.makedirs(cFolderNameOSInternal) 

    import glob
    files = glob.glob(cFolderNameOSInternal + '/*')
    for f in files:
        # print('removing: ', f)
        os.remove(f)

    print('---- start create html files')
    # create html files
    for h in aHtmlFiles:

        # replace tag with links to instructor html files
        # cHtml = h [1].replace('[cInstructorsMenu]', cInstructorsMenu + '<br>' + cStudentMenu + '<br>') 
        cHtml = h [1].replace('[cInstructorsMenu]', cHeader) 

        # remove last empty table row
        cHtml = cHtml.replace('</tr><tr><td colspan = 6>&nbsp;</td></tr></table>', '</tr></table>') 

        # add footer
        cHtml = cHtml + cFooterHtml + cCRLF

        cFileName = cFolderNameOSHtml + h [0]

        f = open(cFileName, 'w')
        f.write(cHtml)
        f.close()

        cFileName = cFolderNameOSInternal + h [0]

        f = open(cFileName, 'w')
        f.write(cHtml)
        f.close()

    print('---- end create html files')

    # copy static image files
    import shutil
    aFiles = []
    aFiles.append(['C:/Data/Python/DiveScheduling/Exports/logo.png',     cFolderNameOSHtml     + 'logo.png'])
    aFiles.append(['C:/Data/Python/DiveScheduling/Exports/logo.png',     cFolderNameOSInternal + 'logo.png'])
    aFiles.append(['C:/Data/Python/DiveScheduling/Exports/calendar.png', cFolderNameOSHtml     + 'calendar.png'])
    aFiles.append(['C:/Data/Python/DiveScheduling/Exports/calendar.png', cFolderNameOSInternal + 'calendar.png'])
    aFiles.append(['C:/Data/Python/DiveScheduling/Exports/favicon.ico',  cFolderNameOSHtml     + 'favicon.ico'])
    aFiles.append(['C:/Data/Python/DiveScheduling/Exports/favicon.ico',  cFolderNameOSInternal + 'favicon.ico'])

    for f in aFiles:
        # print(f[0], f[1])
        shutil.copyfile(f[0], f[1])

    # copy folder
    src = './Exports/Internal'
    dst = "C:/Data/Python/DiveScheduling/Package/static/Internal"
    # print('src: ', src)
    # print('dst: ', dst)
    # cleanup dst folder
    shutil.rmtree(dst)
    # copy folder
    shutil.copytree(src, dst)

    nFinishTime = datetime.datetime.today()

    print()
    print('export start: ', nStartTime, ' export finish: ', nFinishTime)

    cMessage = "html export is ready."

    lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('result.html', cMessage = cMessage, lRBAC = lRBAC)

#------------------------------------------------------------------------------------------

######## ######## ########  
##          ##    ##     ## 
##          ##    ##     ## 
######      ##    ########  
##          ##    ##        
##          ##    ##        
##          ##    ##        

@app.route('/ftp/')
def ftp():

    # inspiration: https://pythonprogramming.net/ftp-transfers-python-ftplib/

    cFolderNameOSInternal = './Exports/Internal/'

    if True:

        print('---- start ftp')

        secrets = dotenv_values(".env")

        ftp     = FTP('ftp.maidiving.nl')
        ftpuser = secrets['FTP_USER']
        ftppw   = secrets['FTP_PASSWORD']
        ftp.login(user = ftpuser, passwd = ftppw)

        listfiles = glob.glob(cFolderNameOSInternal+ "*.*")

        for l in listfiles:
            filenamefrom = l
            filenameto = 'divescheduling/' + l[19:]
            ftp.storbinary('STOR ' + filenameto, open(filenamefrom, 'rb'))
            # print ('filenameto: ', filenameto)

        ftp.quit()

        print('---- end ftp')

        cMessage = "ftp is ready."

        lRBAC = get_rbac(request.url_rule.endpoint)

    return render_template('result.html', cMessage = cMessage, lRBAC = lRBAC)

#------------------------------------------------------------------------------------------