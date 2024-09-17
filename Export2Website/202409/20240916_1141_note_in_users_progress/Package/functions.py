from flask_login import current_user
from Package import db
from Package.models import Users, Products, Instructors, Appointments, Notes
import datetime
from sqlalchemy import func, and_

def get_rbac(cPath):
    if current_user.is_authenticated:

        user = db.session.execute(db.select(Users).filter_by(Username = current_user.Username)).scalar_one()

        # print ('user.Username:     ' + user.Username)        
        lResult = [ current_user.Username ]                  # 0
        lResult.append(user.Status)                          # 1
        lResult.append(user.Id)                              # 2
        lResult.append(user.Firstname + ' ' + user.Lastname) # 3
        lResult.append(datetime.datetime.now())              # 4
        lResult.append("")              # 5 page path
        if len(cPath) > 0:
            lResult [5] = cPath
 
        return lResult
    
    else:
        lResult = []
        return lResult

#def string2safe(text):
#
#    cText = text
#    cReplace = '<>,;:[]{}|()*&^%$#!=+~'
#    for x in cReplace:
#        cText = cText.replace(x, '_')
#   
#    if text != cText:
#        print('#### old text: ', text, ' new text: ', cText)
#
#    return cText

def no_access_text():
    cText = ""
    cText = cText + "<html>"
    cText = cText + "<head><style>h3 {text-align: center;}p {text-align: center;}div {text-align: center;}</style></head>"
    cText = cText + "<body><br><br><br><br>"
    cText = cText + "<h3 style='font-family:verdana'>Welcome to the webapp 'DiveScheduling'</h3><br>"
    cText = cText + "<p style='font-family:verdana'>Please <a href='login'>login</a> or <a href='usersregisterform'>register</a></p>"
    cText = cText + "<br>" 
    cText = cText + "<br>" 
    cText = cText + "<br>" 
    cText = cText + "<br>" 
    cText = cText + "<br>" 
    cText = cText + "<br>" 
    cText = cText + "<br>" 
    cText = cText + "<p style='font-size:12px; font-family:verdana'><b>Muy importante:</b><br>" 
    cText = cText + "This is a demo-environment.<br>"
    cText = cText + "Dot not use personal data.<br></p>"
    cText = cText + "</body></html>" 
    return (cText)


def GetNote(id, type):

    # add ', GetNote, SaveNote' to: from Package.functions import get_rbac, no_access_text, GetNote, SaveNote
    # add before validation of input
    # cNote = GetNote(user.Id, 'st')
    # form.note.data = cNote

    # add to '<template>.html
    # {{ form.note.label() }}<br>
    # {{ form.note(placeholder="note", cols="148", rows="8" ) }}

    # add to 'forms.py'
    # note         = TextAreaField('note')

    print('--- start getnote ------------------------------')
    print('id: ', id, ' type: ', type)

    note = Notes.query.filter(and_((Notes.User == id), (Notes.Type == type)))

    #print('type(note): ', type(note))
    print('note: ', note[0:60])
    print('Notes.Id:   ', Notes.Id)

    cNote = ""

    if note:
        print('note is True')
        for n in note:
            print('n: ', n)
            cNote = n.Note
    else:
        print('note is False')
        cNote = ""

    print('')
    print('cNote: ', cNote[0:40], ' ('+str(len(cNote))+' characters)')
    print('--- finish getnote ------------------------------')

    return(cNote)

def SaveNote(id, type, text, action):

    # add after validation of input
    # cNote          = request.form["note"]
    # SaveNote(user.Id, 'st', cNote, 'replace')

    print('--- start savenote ------------------------------')

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
        #     Product         = db.Column(db.Integer(),                nullable=True, unique=False)
        #     Appointment     = db.Column(db.Integer(),                nullable=True, unique=False)
        #     Instructor      = db.Column(db.Integer(),                nullable=True, unique=False)
        #     Studentrecord   = db.Column(db.Integer(),                nullable=True, unique=False)
        #     Text            = db.Column(db.Text(),                   nullable=True, unique=False)

        print('params: ', id, type, text[0:10], action)
        note = Notes.query.where(and_((Notes.User == id),(Notes.Type == type))).first()

        lRBAC = get_rbac('')
    
        if (not note) or (action == 'add'):
            print('adding new note')
            note_to_create = Notes(Author          = lRBAC[2],  
                                    Date            = datetime.datetime.now(),
                                    Description     = "notes: " + type,
                                    Datelastwritten = datetime.datetime.now(),
                                    User            = id,
                                    Type            = type,
                                    Note            = text)
    
            db.session.add(note_to_create)
            db.session.commit()      
        else:
            print('updating note')
            print('id:   ', id)
            print('type: ', type)
            print('text: ', text)

            note = Notes.query.where(and_((Notes.User == id),(Notes.Type == type))).first()
            x = db.session.query(Notes).get(note.Id)
            x.Note = text
            db.session.commit()      

    print('--- finish savenote ------------------------------')

    return('')