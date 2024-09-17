from Package import db, login_manager
from Package import bcrypt
from flask_login import UserMixin
from sqlalchemy.orm import relationship 
from sqlalchemy       import Integer, ForeignKey, String, Column

# source: https://flask-login.readthedocs.io/en/latest/
# 20240819 - 1311
@login_manager.user_loader
def load_user(user_id):
    return Users.get(user_id)

# -----------------------------
class Appointments(db.Model):
    __tablename__ = "Appointments"
    Id      = db.Column(db.Integer(),                primary_key=True)
    # 20240824 - MvW - 2:     b_a_id = db.Column(db.Integer(), ForeignKey('as.a_id'))
    # User    = db.Column(db.Integer(),                ForeignKey('Users.Id'),    nullable=False, unique=False)
    User    = db.Column(db.Integer(),          ForeignKey('Users.Id'),         nullable=False, unique=False)
    Product = db.Column(db.Integer(),          ForeignKey('Products.Id'),      nullable=False, unique=False)
    Part    = db.Column(db.String(length=5),                                   nullable=True,  unique=False)
    Date    = db.Column(db.DateTime(timezone=True))
    Time    = db.Column(db.String(length=5),                                   nullable=True,  unique=False)
    Notes   = db.Column(db.String(length=128),                                 nullable=True,  unique=False)
    # Staff   = db.Column(db.Integer(),                                          nullable=True,  unique=False)
    Staff   = db.Column(db.Integer(),          ForeignKey('Instructors.Id'),   nullable=True,  unique=False) # 1 - 20240829

    app2nam = relationship('Users',       back_populates = 'Appointments')
    app2pro = relationship('Products',    back_populates = 'Appointments')
    app2ins = relationship('Instructors', back_populates = 'Appointments') # 2 - 20240829

    def __repr__(self):
       return f'appointments {self.name}'
# -----------------------------

class Instructors(db.Model):
    __tablename__ = "Instructors"
    Id      = db.Column(db.Integer(),         primary_key=True)
    User    = db.Column(db.Integer(),         ForeignKey('Users.Id')       )
    Name    = db.Column(db.String(length=30) )

    # relatrionship to Users
    ins2nam = relationship('Users', back_populates = 'Instructors')
    # relationship from Appointments
    Appointments  = relationship('Appointments', back_populates = "app2ins") # 3 - 20240829

# -----------------------------

class Users(db.Model, UserMixin):
    __tablename__= "Users"
    Id           = db.Column(db.Integer(),   primary_key=True)
    Username     = db.Column(db.String(length=30))
    Firstname    = db.Column(db.String(length=50))
    Lastname     = db.Column(db.String(length=50))
    Phone        = db.Column(db.String(length=50))
    Passwordhash = db.Column(db.String(length=30))
    Emailaddress = db.Column(db.String(length=50))
    Status       = db.Column(db.String(length=16))
    Info         = db.Column(db.String(length=1024))

    # Relationships from
    Appointments  = relationship('Appointments', back_populates = "app2nam")
    Instructors   = relationship('Instructors', back_populates = "ins2nam")

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.Passwordhash, attempted_password)

    def is_active(self):
       return True

# -----------------------------

class Products(db.Model):
    __tablename__ = 'Products'
    Id           = db.Column(db.Integer(),    primary_key=True)
    Productname  = db.Column(db.String(30),   nullable=True)
    Price        = db.Column(db.Integer(),    nullable=True)
    Abbr         = db.Column(db.String(5),    nullable=True)
    Parts        = db.Column(db.String(50),   nullable=True)
    Description  = db.Column(db.String(1024), nullable=True)

    Appointments = relationship('Appointments', back_populates = "app2pro")

    def __repr__(self):
        return f'products {self.name}'

# -----------------------------

class Studentrecords(db.Model):
    Id          = db.Column(db.Integer(),                primary_key=True)
    User        = db.Column(db.Integer(),                nullable=True, unique=False)
    Appointment = db.Column(db.Integer(),                nullable=True, unique=False)
    Date        = db.Column(db.DateTime(timezone=True))
    Time        = db.Column(db.String(length=5),         nullable=True, unique=False)
    Description = db.Column(db.String(1024),             nullable=True, unique=False)

    def __repr__(self):
        return f'products {self.name}'

# -----------------------------
# source: https://www.geeksforgeeks.org/sqlalchemy-core-joins/
# works!
#
#class a(db.Model):
#    __tablename__ = 'as'
#    a_id    = db.Column(db.Integer(),                  primary_key=True)
#    a_name  = db.Column(db.String(30))
#    a_text  = db.Column(db.String(30))
#    a_new   = db.Column(db.String(30))
 
#    bs = relationship('b', back_populates = "customer")         #1

#    def __repr__(self):
#        return f'products {self.name}'

#class b(db.Model):
#    __tablename__ = 'bs'
#    b_id   = db.Column(db.Integer(),                  primary_key=True)
#    b_a_id = db.Column(db.Integer(), ForeignKey('as.a_id'))     #2
#    b_name = db.Column(db.String(30))
#
#    customer = relationship('a', back_populates="bs")           #3
#
#    def __repr__(self):
#        return f'products {self.name}'
# -----------------------------

class names(db.Model):
    names_id    = db.Column(db.Integer(),                  primary_key=True)
    names_name  = db.Column(db.String(30))
    names_text  = db.Column(db.String(30))
    names_new   = db.Column(db.String(30))
 
    numbers     = relationship('numbers', back_populates = "num2nam")         #1

    def __repr__(self):
        return f'products {self.name}'

class numbers(db.Model):
    numbers_id       = db.Column(db.Integer(),                  primary_key=True)
    numbers_names_id = db.Column(db.Integer(), ForeignKey('names.names_id'))     #2
    numbers_name     = db.Column(db.String(30))

    num2nam    = relationship('names', back_populates="numbers")           #3

    def __repr__(self):
        return f'products {self.name}'

# results = db.session.execute(    db.select(numbers.numbers_id, numbers.numbers_name, names.names_name, names.names_text).select_from(numbers).join(names, numbers.numbers_names_id == names.names_id) ) 
# for row in results: 
#     print(row) 


# ------------------------------------------------------------------------
# source: https://realpython.com/flask-database/#close-database-connections
#
# def init_app(app):
#    app.teardown_appcontext(close_db)
#    app.cli.add_command(init_db_command)
#
#
# def close_db(e=None):
#    db = g.pop("db", None)
#
#    if db is not None:
#        db.close()
#
# ------------------------------------------------------------------------

