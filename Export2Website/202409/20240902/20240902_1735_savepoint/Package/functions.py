from flask_login import current_user
from Package import db
from Package.models import Users, Products, Instructors, Appointments
import datetime


def get_rbac():
    if current_user.is_authenticated:

        user = db.session.execute(db.select(Users).filter_by(Username = current_user.Username)).scalar_one()

        print ('user.Username:     ' + user.Username)        
        lResult = [ current_user.Username ]                  # 0
        lResult.append(user.Status)                          # 1
        lResult.append(user.Id)                              # 2
        lResult.append(user.Firstname + ' ' + user.Lastname) # 3
        lResult.append(datetime.datetime.now())              # 4
 
        return lResult
    
    else:
        lResult = []
        return lResult
