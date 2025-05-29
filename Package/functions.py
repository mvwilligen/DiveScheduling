from flask_login import current_user
from Package import db
from Package.models import Users
from Package.models import Products
from Package.models import Instructors
from Package.models import Appointments
from Package.models import Notes
import datetime
from sqlalchemy import func, and_
import socket
import os.path

# for remote ip address
from flask import request
from flask import jsonify

################################################################################################################'

 ######   ######## ########         ########  ########     ###     ######  
##    ##  ##          ##            ##     ## ##     ##   ## ##   ##    ## 
##        ##          ##            ##     ## ##     ##  ##   ##  ##       
##   #### ######      ##            ########  ########  ##     ## ##       
##    ##  ##          ##            ##   ##   ##     ## ######### ##       
##    ##  ##          ##            ##    ##  ##     ## ##     ## ##    ## 
 ######   ########    ##    ####### ##     ## ########  ##     ##  ######  

################################################################################################################'

def get_rbac(cPath):

    if current_user.is_authenticated:

        user = db.session.execute(db.select(Users).filter_by(Username = current_user.Username)).scalar_one()

        # print ('user.Username:     ' + user.Username)        
        lResult = [ current_user.Username ]                  # 0
        lResult.append(user.Status)                          # 1
        lResult.append(user.Id)                              # 2
        lResult.append(user.Firstname + ' ' + user.Lastname) # 3
        lResult.append(datetime.datetime.now())              # 4
        lResult.append("")                                   # 5 page path
        if len(cPath) > 0:
            lResult [5] = cPath
        lResult.append(socket.gethostname())                 # 6
        lResult.append('1.0.0')                              # 7 - version
        lResult.append(False)                                # 8 - debug

        if "laura" in lResult [0].lower():
            lResult [8] = True    
    else:
        
        lResult = ['']                       # 0
        lResult.append('')                   # 1
        lResult.append('')                   # 2
        lResult.append('')                   # 3
        lResult.append('')                   # 4
        lResult.append('')                   # 5
        lResult.append(socket.gethostname()) # 6
        lResult.append('')                   # 7
        lResult.append(False)                 # 8

    # lResult.append(False)                 # 8

    return lResult


# ################################################################################################################'
#
#  ######  ######## ########  #### ##    ##  ######    #######   ######     ###    ######## ######## 
# ##    ##    ##    ##     ##  ##  ###   ## ##    ##  ##     ## ##    ##   ## ##   ##       ##       
# ##          ##    ##     ##  ##  ####  ## ##               ## ##        ##   ##  ##       ##       
#  ######     ##    ########   ##  ## ## ## ##   ####  #######   ######  ##     ## ######   ######   
#       ##    ##    ##   ##    ##  ##  #### ##    ##  ##              ## ######### ##       ##       
# ##    ##    ##    ##    ##   ##  ##   ### ##    ##  ##        ##    ## ##     ## ##       ##       
#  ######     ##    ##     ## #### ##    ##  ######   #########  ######  ##     ## ##       ######## 
# 
# ################################################################################################################'


def string2safe(text):

    cText = text
    cReplace = '<>;[]{}|()*&^%$#=+~'+chr(34) # : (time) ! (text) , (text) @ (mail) . (text)
    for x in cReplace:
        cText = cText.replace(x, '_')
   
    # if text != cText:
    #     print('#### old text: ', text, ' new text: ', cText)

    return cText


# ###############################################################################################################'
#
# ##    ##  #######             ###     ######   ######  ########  ######   ######          ######## ######## ##     ## ########
# ###   ## ##     ##           ## ##   ##    ## ##    ## ##       ##    ## ##    ##            ##    ##        ##   ##     ##
# ####  ## ##     ##          ##   ##  ##       ##       ##       ##       ##                  ##    ##         ## ##      ##
# ## ## ## ##     ##         ##     ## ##       ##       ######    ######   ######             ##    ######      ###       ##
# ##  #### ##     ##         ######### ##       ##       ##             ##       ##            ##    ##         ## ##      ##
# ##   ### ##     ##         ##     ## ##    ## ##    ## ##       ##    ## ##    ##            ##    ##        ##   ##     ##
# ##    ##  #######  ####### ##     ##  ######   ######  ########  ######   ######  #######    ##    ######## ##     ##    ##
#
# ###############################################################################################################


def no_access_text():

    logtext('no_access_text', 'w')

    cText = ""
    cText = cText + "<html>"
    cText = cText + "<head><style>h3 {text-align: center;}p {text-align: center;}div {text-align: center;}</style></head>"
    cText = cText + "<body><br><br><br><br>"
    cText = cText + "<h3 style='font-family:verdana'>Welcome to the webapp 'DiveScheduling'</h3><br>"

    # added for idcrotterdam.nl
    cLink0 = socket.gethostname()
    cLink1 = ""
    cLink2 = ""

    cLink1 = "/login"
    cLink2 = "/usersregisterform"

    cText = cText + "<p style='font-family:verdana'>Please <a href='" + cLink1 + "'>login</a> or <a href='" + cLink2 + "'>register</a></p>"
    cText = cText + "<br>" 
    cText = cText + "<br>" 
    cText = cText + "<br>" 
    cText = cText + cLink0 + "<br>" 
    cText = cText + "<br>" 
    cText = cText + "<br>" 
    cText = cText + "<br>" 
    cText = cText + "<p style='font-size:12px; font-family:verdana'><b>Muy importante:</b><br>" 
    cText = cText + "This is a demo-environment.<br>"
    cText = cText + "Dot not use personal data.<br></p>"
    cText = cText + "</body></html>" 
    # cMessage = "Hello!"

    return (cText)

################################################################################################################'

 ######   ######## ######## ##    ##  #######  ######## ######## 
##    ##  ##          ##    ###   ## ##     ##    ##    ##       
##        ##          ##    ####  ## ##     ##    ##    ##       
##   #### ######      ##    ## ## ## ##     ##    ##    ######   
##    ##  ##          ##    ##  #### ##     ##    ##    ##       
##    ##  ##          ##    ##   ### ##     ##    ##    ##       
 ######   ########    ##    ##    ##  #######     ##    ######## 

################################################################################################################'

def GetNote(id, type):

    logtext('functions/getnote ' + str(id) + ' type:' + type, 'i')

    # add ', GetNote, SaveNote' to: from Package.functions import get_rbac, no_access_text, GetNote, SaveNote
    # add before validation of input
    # cNote = GetNote(user.Id, 'st')
    # form.note.data = cNote

    # add to '<template>.html
    # {{ form.note.label() }}<br>
    # {{ form.note(placeholder="note", cols="148", rows="8" ) }}

    # add to 'forms.py'
    # note         = TextAreaField('note')

    # print('--- start getnote ------------------------------')
    # print('id: ', id, ' type: ', type)

    note = Notes.query.filter(and_((Notes.User == id), (Notes.Type == type)))

    # #print('type(note): ', type(note))
    # print('note: ', note[0:60])
    # print('Notes.Id:   ', Notes.Id)

    cNote = ""

    if note:
        # print('note is True')
        for n in note:
            # print('n: ', n)
            cNote = n.Note
    else:
        # print('note is False')
        cNote = ""

    # print('')
    # print('cNote: ', cNote[0:40], ' ('+str(len(cNote))+' characters)')
    # print('--- finish getnote ------------------------------')

    return(cNote)

################################################################################################################'

 ######     ###    ##     ## ######## ##    ##  #######  ######## ######## 
##    ##   ## ##   ##     ## ##       ###   ## ##     ##    ##    ##       
##        ##   ##  ##     ## ##       ####  ## ##     ##    ##    ##       
 ######  ##     ## ##     ## ######   ## ## ## ##     ##    ##    ######   
      ## #########  ##   ##  ##       ##  #### ##     ##    ##    ##       
##    ## ##     ##   ## ##   ##       ##   ### ##     ##    ##    ##       
 ######  ##     ##    ###    ######## ##    ##  #######     ##    ######## 

################################################################################################################'

def SaveNote(id, type, text, action):

    logtext('functions/savenote ' + str(id) + ' type:' + type + ' length:' + str(len(text)) + ' action:' + action, 'i')

    # add after validation of input
    # cNote          = request.form["note"]
    # SaveNote(user.Id, 'st', cNote, 'replace')

    #print('--- start savenote ------------------------------')

    if len(text) > 0:

        # class Notes(db.Model):
        #     __tablename__   = 'Notes'
        #  0   Id              = db.Column(db.Integer(),                primary_key=True)
        #  1   Author          = db.Column(db.Integer(),                nullable=True, unique=False)
        #  2   Date            = db.Column(db.DateTime(timezone=True))
        #  3   Description     = db.Column(db.String(60),               nullable=True, unique=False)
        #  4   Note            = db.Column(db.Text,                     nullable=True, unique=False)
        #  5   Datelastwritten = db.Column(db.DateTime(timezone=True))
        #  6   User            = db.Column(db.Integer(),                nullable=True, unique=False)
        #  7   Type            = db.Column(db.String(2) ,               nullable=True, unique=False) # st, re, ap, in, pr
        #      Product         = db.Column(db.Integer(),                nullable=True, unique=False)
        #      Appointment     = db.Column(db.Integer(),                nullable=True, unique=False)
        #      Instructor      = db.Column(db.Integer(),                nullable=True, unique=False)
        #      Studentrecord   = db.Column(db.Integer(),                nullable=True, unique=False)
        #      Text            = db.Column(db.Text(),                   nullable=True, unique=False)

        #print('params: ', id, type, text[0:10], action)
        note = Notes.query.where(and_((Notes.User == id),(Notes.Type == type))).first()

        lRBAC = get_rbac('')
    
        if (not note) or (action == 'add'):
            #print('adding new note')
            note_to_create = Notes(Author          = lRBAC[2],  
                                    Date           = datetime.datetime.now(),
                                    Description    = "notes: " + type,
                                    Lastwritten    = datetime.datetime.now(),
                                    User           = id,
                                    Type           = type,
                                    Note           = text)
    
            db.session.add(note_to_create)
            db.session.commit()      
        else:
            #print('updating note')
            #print('id:   ', id)
            #print('type: ', type)
            #print('text: ', text)

            note = Notes.query.where(and_((Notes.User == id),(Notes.Type == type))).first()
            x = db.session.query(Notes).get(note.Id)
            x.Note = text
            db.session.commit()      

    # print('--- finish savenote ------------------------------')

    return('')


# ################################################################################################################
#
# ##        #######   ######   ######## ######## ##     ## ########
# ##       ##     ## ##    ##     ##    ##        ##   ##     ##
# ##       ##     ## ##           ##    ##         ## ##      ##
# ##       ##     ## ##   ####    ##    ######      ###       ##
# ##       ##     ## ##    ##     ##    ##         ## ##      ##
# ##       ##     ## ##    ##     ##    ##        ##   ##     ##
# ########  #######   ######      ##    ######## ##     ##    ##
#
# ################################################################################################################'

def logtext(text, type):

    lRBAC = get_rbac('')

    cDateToday        = datetime.datetime.today()

    cDate = cDateToday.strftime("%d-%m-%Y")
    cTime = cDateToday.strftime("%H:%M:%S")

    cYYYYMMDD = cDateToday.strftime("%Y%m%d")

    lRBAC = get_rbac('')
    
    cIP1 = request.environ['REMOTE_ADDR']
    cIP2 = request.remote_addr

    if cIP1 == cIP2:
        cIP2 = ""

    if cIP1 == "31.151.235.150":
        cIP1 = "[martin]"

    if cIP1 == "192.168.1.57":
        cIP1 = "[martin]"

    # might solve issue in stderr_20250523_0000.log at 2025-05-18 11:27:47,939 "TypeError: can only concatenate str (not "NoneType") to str"
    user_agent = "" + request.headers.get('User-Agent')

    # 14:05:57 Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36
    user_agent = user_agent.replace("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36","Chrome")
    user_agent = user_agent.replace("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0","Firefox")

    cPath = "_logfile"
    if not os.path.exists(cPath):
        print(cDate + ";" + cTime + ";logtext; path not found:" + cPath)
        os.makedirs(cPath)

    cFile = cPath + '/logfile_' + socket.gethostname() + '_' + cYYYYMMDD + '.txt'

    cHeader = ""
    if not os.path.isfile(cFile):    
        print(cDate + ";" + cTime + ";logtext;file not found:" + cFile)
        cHeader = "date;time;type;ip1;ip2;user;description;agent\n"

    cLine = cHeader + cDate + ";" + cTime + ";" + type + ";"  + cIP1  + ";" + cIP2 + ";" + lRBAC [0] + ";" + text + ";" + user_agent + "\n"

    if lRBAC [8]:
        print (cLine)

    with open(cFile, 'a') as the_file:
        the_file.write(cLine)

    return



# ################################################################################################################
#
# ##     ## ##    ##  #######  ##     ## ######## ########  ##    ##
# ###   ###  ##  ##  ##     ## ##     ## ##       ##     ##  ##  ##
# #### ####   ####   ##     ## ##     ## ##       ##     ##   ####
# ## ### ##    ##    ##     ## ##     ## ######   ########     ##
# ##     ##    ##    ##  ## ## ##     ## ##       ##   ##      ##
# ##     ##    ##    ##    ##  ##     ## ##       ##    ##     ##
# ##     ##    ##     ##### ##  #######  ######## ##     ##    ##
#
# ################################################################################################################

def myquery(dbquery):

    result = []

    if len(dbquery) > 0:

        # print('')
        # print('#### datetime.datetime.now() - dbquery: ', dbquery)
        # print('')

        logtext(dbquery, "i")

        result = eval(dbquery)

    return result


# ################################################################################################################
# 
#  ######  ##     ## ##    ##          ######  ######## ########  ######## ########  ########      ##        #######   ######   
# ##    ## ##     ## ##   ##          ##    ##    ##    ##     ## ##       ##     ## ##     ##     ##       ##     ## ##    ##  
# ##       ##     ## ##  ##           ##          ##    ##     ## ##       ##     ## ##     ##     ##       ##     ## ##        
# ##       ######### #####             ######     ##    ##     ## ######   ########  ########      ##       ##     ## ##   #### 
# ##       ##     ## ##  ##                 ##    ##    ##     ## ##       ##   ##   ##   ##       ##       ##     ## ##    ##  
# ##    ## ##     ## ##   ##          ##    ##    ##    ##     ## ##       ##    ##  ##    ##  ### ##       ##     ## ##    ##  
#  ######  ##     ## ##    ## #######  ######     ##    ########  ######## ##     ## ##     ## ### ########  #######   ######   
#
# ################################################################################################################

from Package import app

@app.route('/chk_stderr_log/')
def chk_stderr_log():

    # excerpt from strerr.log:
    # 
    # file will be copied and moved every night around 00.00


    # finish: __init__.py


    # start:  __init__.py
    # APPLICATION_ROOT: /

    # ===========================================================================================================
    # date and time:        2025-05-17 15:45:13.872324

    # OS version:           posix
    # sys.platform:         linux
    # platform.system():    Linux
    # platform.release():   4.18.0-372.9.1.1.lve.el8.x86_64
    # platform.version():   #1 SMP Tue May 24 07:49:22 EDT 2022
    # platform.platform():  Linux-4.18.0-372.9.1.1.lve.el8.x86_64-x86_64-with-glibc2.28

    # Python version:       3.9.21 (main, Jan 13 2025, 12:41:50) 
    # [GCC 9.2.1 20191120 (Red Hat 9.2.1-2)]

    # Hostname              linux2025.webawere.nl

    # app:                  <Flask 'Package'>
    # -----------------------------------------------------------------------------------------------------------

    # finish: __init__.py

    # submit

    # #### ---------------------------------------------------------------
    # #### before  False   new
    # #### after   False   student 

    # start:  __init__.py
    # APPLICATION_ROOT: /

    # ===========================================================================================================
    # date and time:        2025-05-17 15:45:13.872324

    logtext('chk_stderr.log','i')

    lRBAC = get_rbac('')

    cDateToday        = datetime.datetime.today()

    cDate = cDateToday.strftime("%d-%m-%Y")
    cDate2 = cDateToday.strftime("%Y%m%d")
    cTime = cDateToday.strftime("%H:%M:%S")
    cTime2 = cDateToday.strftime("%H%M%S")

    cOutputFile = "stderr_" + cDate2 + "_" + cTime2 + ".html"

    cYYYYMMDD = cDateToday.strftime("%Y%m%d")

    cTop = "<html><style>\n"
    cTop = cTop + "td { text-align:left; vertical-align:top; padding-left:5px;padding-right:5px;padding-bottom:5px;padding-top:5px; font-size: 11pt;font-family: Arial;width:200px;\n"
    cTop = cTop + "font-family:verdana; }\n"
    cTop = cTop + "table { border-collapse: collapse; }\n"
    cTop = cTop + "a, p, h3 {font-family:verdana;}\n"
    cTop = cTop + "table, th, td { border: 1px solid};\n"
    cTop = cTop + "</style>\n"
    cBottom = "</html>"

    cFilename = "stderr_20250523_0000.log"
    cFilename = "/apps/divescheduler/stderr.log"
    cFilename = "stderr.log"

    if lRBAC[6] == "MWI20":
        cFilename = "stderr.log"

    cOutput = cTop + "<h3>" + cDate + " " + cTime + "</h3><br>\n<p>"
    cOutput = cOutput + "filename: " + cFilename + "<br>\n"

    lToggle = False
    cTimeStamp = ""

    logtext("start reading file '" + cFilename + "'",'i')

    if os.path.isfile(cFilename):

        logtext("file '" +cFilename + "' exists",'i')

        with open(cFilename) as f:

            for x in f:

                if x[:14] == "date and time:":
                    cTimeStamp = "<br>[" + x + "]<br><br>\n"
                if x[:19] == "finish: __init__.py":
                    x = ""
                    lToggle = True
                if x[:19] == "start:  __init__.py":
                    lToggle = False

                if (len(x.strip()) > 0 and lToggle):
                    cOutput = cOutput + cTimeStamp + x + "<br>\n"
                    cTimeStamp = ""

        logtext("finished reading file",'i')

        with open(cOutputFile, "w") as f:
            cOutput = cOutput + "<br>[eof]<br>" + cBottom
            f.write(cOutput)
            logtext("written file",'i')
    else:
        logtext("file '" + cFilename + "' does not exists",'i')

    return cOutput


# ################################################################################################################
#
#  ######  ##     ##  #######  ##      ## ##        #######   ######   ######## #### ##       ######## 
# ##    ## ##     ## ##     ## ##  ##  ## ##       ##     ## ##    ##  ##        ##  ##       ##       
# ##       ##     ## ##     ## ##  ##  ## ##       ##     ## ##        ##        ##  ##       ##       
#  ######  ######### ##     ## ##  ##  ## ##       ##     ## ##   #### ######    ##  ##       ######   
#       ## ##     ## ##     ## ##  ##  ## ##       ##     ## ##    ##  ##        ##  ##       ##       
# ##    ## ##     ## ##     ## ##  ##  ## ##       ##     ## ##    ##  ##        ##  ##       ##       
#  ######  ##     ##  #######   ###  ###  ########  #######   ######   ##       #### ######## ######## 
#
# ################################################################################################################


@app.route('/showlogfile/')
def showlogfile():

    logtext('showlogfile','i')

    lRBAC = get_rbac('')

    cDateToday        = datetime.datetime.today()

    cDate = cDateToday.strftime("%d-%m-%Y")
    cDate2 = cDateToday.strftime("%Y%m%d")
    cTime = cDateToday.strftime("%H:%M:%S")
    cTime2 = cDateToday.strftime("%H%M%S")

    cOutputFile = "stderr_" + cDate2 + "_" + cTime2 + ".html"

    cYYYYMMDD = cDateToday.strftime("%Y%m%d")

    cTop = "<html><style>\n"
    cTop = cTop + "td { text-align:left; vertical-align:top; padding-left:5px;padding-right:5px;padding-bottom:5px;padding-top:5px; font-size: 11pt;font-family: Arial;width:200px;\n"
    cTop = cTop + "font-family:verdana; }\n"
    cTop = cTop + "table { border-collapse: collapse; }\n"
    cTop = cTop + "a, p, h3 {font-family:verdana;}\n"
    cTop = cTop + "table, th, td { border: 1px solid};\n"
    cTop = cTop + "</style>\n"
    cBottom = "</html>"

    cFilename = "/apps/divescheduler/_logfile/logfile_linux2025.webawere.nl_" + cDate2 +".txt"
    cFilename = "_logfile/logfile_linux2025.webawere.nl_" + cDate2 +".txt"

    if lRBAC[6] == "MWI20":
        cFilename = "_logfile\logfile_MWI20_" + cDate2 + ".txt"

    cOutput = cTop + "<h3>" + cDate + " " + cTime + "</h3><br>\n<p>"
    cOutput = cOutput + "filename: " + cFilename + "<br>\n"

    lToggle = False
    cTimeStamp = ""

    logtext("start reading file '" + cFilename + "'",'i')

    if os.path.isfile(cFilename):

        logtext("file '" +cFilename + "' exists",'i')

        with open(cFilename) as f:

            for x in f:

                cOutput = cOutput + x + "<br>\n"

        logtext("finished reading file",'i')

        with open(cOutputFile, "w") as f:
            cOutput = cOutput + "<br>[eof]<br>" + cBottom
            f.write(cOutput)
            logtext("written file",'i')
    else:
        logtext("file does not exists",'w')

    return cOutput
