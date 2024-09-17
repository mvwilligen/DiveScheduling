from flask_login import current_user
from Package import db
from Package.models import Users, Products, Instructors, Appointments

def get_rbac():
    if current_user.is_authenticated:
        lResult = [ current_user.Username ]

        user = db.session.execute(db.select(Users).filter_by(Username = current_user.Username)).scalar_one()
        print ('user.Username:     ' + user.Username)
        lResult.append(user.Status)
        lResult.append(user.Id)
 
        return lResult
    
    else:
        lResult = []
        return lResult
