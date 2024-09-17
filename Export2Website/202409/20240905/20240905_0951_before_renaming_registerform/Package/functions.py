from flask_login import current_user
from Package import db
from Package.models import Users, Products, Instructors, Appointments
import datetime


def get_rbac():
    if current_user.is_authenticated:

        user = db.session.execute(db.select(Users).filter_by(Username = current_user.Username)).scalar_one()

        # print ('user.Username:     ' + user.Username)        
        lResult = [ current_user.Username ]                  # 0
        lResult.append(user.Status)                          # 1
        lResult.append(user.Id)                              # 2
        lResult.append(user.Firstname + ' ' + user.Lastname) # 3
        lResult.append(datetime.datetime.now())              # 4
 
        return lResult
    
    else:
        lResult = []
        return lResult

def string2safe(text):

    cText = text
    cReplace = '<>,;:[]{}|()*&^%$#!=+~\\'
    for x in cReplace:
        cText = cText.replace(x, '_')
    
    if text != cText:
        print('#### old text: ', text, ' new text: ', cText)

    return cText

def no_access_text():
    cText = ""
    cText = cText + "<html>"
    cText = cText + "<head><style>h3 {text-align: center;}p {text-align: center;}div {text-align: center;}</style></head>"
    cText = cText + "<body><br><br><br><br>"
    cText = cText + "<h3 style='font-family:verdana'>Welcome to the webapp 'DiveScheduling'</h3><br>"
    cText = cText + "<p style='font-family:verdana'>Please <a href='login'>login</a> or <a href='register'>register</a></p>"
    cText = cText + "<br>" 
    cText = cText + "<br>" 
    cText = cText + "<br>" 
    cText = cText + "<br>" 
    cText = cText + "<br>" 
    cText = cText + "<br>" 
    cText = cText + "<br>" 
    cText = cText + "<br>" 
    cText = cText + "This is a demo-environment.<br>"
    cText = cText + "Dot not use personal data.<br>" 
    cText = cText + "</body></html>" 
    return (cText)
