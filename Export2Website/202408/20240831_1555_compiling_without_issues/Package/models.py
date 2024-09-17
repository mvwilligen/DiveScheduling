##  
##  ##     ##  #######  ########  ######## ##        ######      ########  ##    ##    
##  ###   ### ##     ## ##     ## ##       ##       ##    ##     ##     ##  ##  ##     
##  #### #### ##     ## ##     ## ##       ##       ##           ##     ##   ####      
##  ## ### ## ##     ## ##     ## ######   ##        ######      ########     ##       
##  ##     ## ##     ## ##     ## ##       ##             ##     ##           ##       
##  ##     ## ##     ## ##     ## ##       ##       ##    ## ### ##           ##       
##  ##     ##  #######  ########  ######## ########  ######  ### ##           ##       
##
##  https://patorjk.com/software/taag/#p=display&f=Banner3&t=models.py%20

# added 20240831 1509   - issues with reinit_db.py
# removed 20240831 1510 - issues with reinit_db.py
# added 20240831 1512   - issues with reinit_db.py
# removed 20240831 1514 - issues with reinit_db.py
# from Package          import db
from Package import db

# added   20240831 1535 - issues witrh reinit_db.py

from Package          import app
from flask            import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy       import Integer, ForeignKey, String, Column, func, and_
from sqlalchemy.orm   import DeclarativeBase
from sqlalchemy.orm   import relationship
print(app)

# source: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
from werkzeug.security import generate_password_hash, check_password_hash

# source: https://flask-login.readthedocs.io/en/latest/
# 20240830

from flask_login import UserMixin

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

# source: https://flask-login.readthedocs.io/en/latest/
# 20240830
# class Users(db.Model, UserMixin):
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

    # source: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.Passwordhash, password)

    def get_id(self):
        return (self.Id)

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

