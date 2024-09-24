###########################################################################################
##                                                                                       ##
##  ##     ##  #######  ########  ######## ##        ######      ########  ##    ##      ##
##  ###   ### ##     ## ##     ## ##       ##       ##    ##     ##     ##  ##  ##       ##
##  #### #### ##     ## ##     ## ##       ##       ##           ##     ##   ####        ##
##  ## ### ## ##     ## ##     ## ######   ##        ######      ########     ##         ##
##  ##     ## ##     ## ##     ## ##       ##             ##     ##           ##         ##
##  ##     ## ##     ## ##     ## ##       ##       ##    ## ### ##           ##         ##
##  ##     ##  #######  ########  ######## ########  ######  ### ##           ##         ##
##                                                                                       ##
###########################################################################################


from Package          import db
from Package          import app
from flask            import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy       import Integer, ForeignKey, String, Column, func, and_
from sqlalchemy.orm   import DeclarativeBase
from sqlalchemy.orm   import relationship
from flask_login      import UserMixin

# -----------------------------

class Appointments(db.Model):
    __tablename__ = "Appointments"
    Id          = db.Column(db.Integer(),                primary_key=True)
    User        = db.Column(db.Integer(),          ForeignKey('Users.Id'),         nullable=False, unique=False)
    Product     = db.Column(db.Integer(),          ForeignKey('Products.Id'),      nullable=False, unique=False)
    Part        = db.Column(db.String(length=5),                                   nullable=True,  unique=False)
    Date        = db.Column(db.DateTime(timezone=True))
    # Notes     = db.Column(db.String(length=128),                                 nullable=True,  unique=False)
    Staff       = db.Column(db.Integer(),          ForeignKey('Instructors.Id'),   nullable=True,  unique=False) # 1 - 20240829
    Assistants  = db.Column(db.String(length=64),                                  nullable=True,  unique=False)
    Lastwritten = db.Column(db.DateTime(timezone=True))

    app2nam = relationship('Users',       back_populates = 'Appointments')
    app2pro = relationship('Products',    back_populates = 'Appointments')
    app2ins = relationship('Instructors', back_populates = 'Appointments') # 2 - 20240829

    def __repr__(self):
       return f'appointments {self.name}'

# Appointments.Id, Appointments.User, Appointments.Product, Appointments.Part, Appointments.Date, Appointments.Notes, Appointments.Staff
# -----------------------------

class Instructors(db.Model):
    __tablename__   = "Instructors"
    Id              = db.Column(db.Integer(),         primary_key=True)
    User            = db.Column(db.Integer(),         ForeignKey('Users.Id')       )
    Name            = db.Column(db.String(length=30) )
    Active          = db.Column(db.Boolean() )
    Products        = db.Column(db.String(length=60) )
    # DateLastWritten = db.Column(db.DateTime(timezone=True))
    Lastwritten = db.Column(db.DateTime(timezone=True))

    # relatrionship to Users
    ins2nam = relationship('Users', back_populates = 'Instructors')

    # relationship from Appointments
    Appointments  = relationship('Appointments', back_populates = "app2ins") # 3 - 20240829

# -----------------------------

class Notes(db.Model):
    __tablename__   = 'Notes'
    Id              = db.Column(db.Integer(),                primary_key=True)
    Author          = db.Column(db.Integer(),                nullable=True, unique=False)
    Date            = db.Column(db.DateTime(timezone=True))
    Description     = db.Column(db.String(60),               nullable=True, unique=False)
    Note            = db.Column(db.Text,                     nullable=True, unique=False)
    # Datelastwritten = db.Column(db.DateTime(timezone=True))
    User            = db.Column(db.Integer(),                nullable=True, unique=False)
    Type            = db.Column(db.String(2) ,               nullable=True, unique=False) # st, re, ap, in, pr
    Lastwritten = db.Column(db.DateTime(timezone=True))
    # Product         = db.Column(db.Integer(),                nullable=True, unique=False)
    # Appointment     = db.Column(db.Integer(),                nullable=True, unique=False)
    # Instructor      = db.Column(db.Integer(),                nullable=True, unique=False)
    # Studentrecord   = db.Column(db.Integer(),                nullable=True, unique=False)
    # Text            = db.Column(db.Text(),                   nullable=True, unique=False)

# -----------------------------

class Products(db.Model):
    __tablename__ = 'Products'
    Id              = db.Column(db.Integer(),    primary_key=True)
    Productname     = db.Column(db.String(30),   nullable=True)
    Abbr            = db.Column(db.String(5),    nullable=True)
    Parts           = db.Column(db.String(50),   nullable=True)
    Description     = db.Column(db.String(1024), nullable=True)
    Active          = db.Column(db.Boolean() )
    # DateLastWritten = db.Column(db.DateTime(timezone=True))
    Lastwritten = db.Column(db.DateTime(timezone=True))

    Appointments    = relationship('Appointments', back_populates = "app2pro")

    def __repr__(self):
        return f'products {self.name}'

# -----------------------------

class Status(db.Model):
    Id              = db.Column(db.Integer(),                primary_key=True)
    Name            = db.Column(db.String(length=20))

# -----------------------------

# class Studentrecords(db.Model):
#     Id              = db.Column(db.Integer(),                primary_key=True)
#     User            = db.Column(db.Integer(),                nullable=True, unique=False)
#     Appointment     = db.Column(db.Integer(),                nullable=True, unique=False)
#     Author          = db.Column(db.Integer(),                nullable=True, unique=False)
#     Date            = db.Column(db.DateTime(timezone=True))
#     Description     = db.Column(db.String(1024),             nullable=True, unique=False)
#     # DateLastWritten = db.Column(db.DateTime(timezone=True))
#     Lastwritten = db.Column(db.DateTime(timezone=True))

#     def __repr__(self):
#         return f'products {self.name}'

# -----------------------------

class Users(db.Model, UserMixin):
    __tablename__   = "Users"
    Id              = db.Column(db.Integer(),   primary_key=True)
    Username        = db.Column(db.String(length=30))
    Firstname       = db.Column(db.String(length=50))
    Lastname        = db.Column(db.String(length=50))
    Phone           = db.Column(db.String(length=50))
    Passwordhash    = db.Column(db.String(length=30))
    Emailaddress    = db.Column(db.String(length=50))
    Status          = db.Column(db.String(length=16))
    Info            = db.Column(db.String(length=1024))
    Active          = db.Column(db.Boolean())
    # DateLastWritten = db.Column(db.DateTime(timezone=True))
    Lastwritten = db.Column(db.DateTime(timezone=True))

    # Relationships from
    Appointments   = relationship('Appointments', back_populates = "app2nam")
    Instructors    = relationship('Instructors', back_populates = "ins2nam")
    
    def get_id(self):
        return (self.Id)

    def is_active(self):
       return True

# -----------------------------
