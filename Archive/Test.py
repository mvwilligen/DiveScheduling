


# ████████╗███████╗███████╗████████╗██████╗ ██╗   ██╗    
# ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔══██╗╚██╗ ██╔╝    
#    ██║   █████╗  ███████╗   ██║   ██████╔╝ ╚████╔╝     
#    ██║   ██╔══╝  ╚════██║   ██║   ██╔═══╝   ╚██╔╝      
#    ██║   ███████╗███████║   ██║██╗██║        ██║       
#    ╚═╝   ╚══════╝╚══════╝   ╚═╝╚═╝╚═╝        ╚═╝       
#
# https://patorjk.com/software/taag/#p=display&f=ANSI%20Shadow&t=routes.py%20                                                                           
                                                       

#--------------------------------------------------------------------------

import os
os.urandom(12).hex(12)

>>> os.urandom(12).hex()
'ec9bb7d32448dd860d3199a2'
>>>


>>> import secrets
>>> secrets.token_hex()
'c874b801a7caf1be80c5ff8900a3dad08c7de89c'


#--------------------------------------------------------------------------
# create new tables

from Package import app
from Package import db

with app.app_context():
    db.drop_all()
    db.create_all()


#--------------------------------------------------------------------------

from Package import db, app
from Package.models import Products

P1 = Products(Productname = "DiscoverScubaDiving", Abbr = "DSD", Parts = "DSD",                                            Price = 50,  Description = "omschrijving DSD")
P2 = Products(Productname = "Open Water",          Abbr = "OW",  Parts = "Intro|ZW1|ZW2|ZW3|Exam|BW1|BW2|BW3",             Price = 300, Description = 'omschrijving OW')
P3 = Products(Productname = "AdvancedOpenWater",   Abbr = "DSD", Parts = "Intro|ZW1|ZW2|ZW3|ZW4|ZW5|Exam|BW1|BW2|BW3|BW4", Price = 500, Description = 'omschrijving AOW')
P4 = Products(Productname = "DiveMaster",          Abbr = "DM",  Parts = "Intro|ZW1|ZW2|ZW3|Exam|BW1|BW2|BW3|BW4",         Price = 500, Description = 'omschrijving DM')
P5 = Products(Productname = "Nachtduikert",        Abbr = "N",   Parts = "Theory|BW",                                      Price = 110, Description = 'omschrijving ND')
with app.app_context():
    db.session.add(P1)
    db.session.add(P2)
    db.session.add(P3)
    db.session.add(P4)
    db.session.add(P5)
    db.session.commit()

from Package.models import Products
from Package import db
from Package import app
with app.app_context():
    for Product in Products.query.all():
        Product.Id
        Product.Productname
        Product.Abbr
        Product.Parts
        Product.Price

#--------------------------------------------------------------------------
from Package.models import Users
from Package import app, db

U0 = Users(Username = "Admin",    Lastname = "Aaaaa",    Firstname = "Aa", Phone = "06-12000000", Passwordhash = "abc", Emailaddress = "Admin@mwisoftware.nl",    Status = "admin, staff, student")
U1 = Users(Username = "Laura",    Lastname = "Bbbbbbb",  Firstname = "Bb", Phone = "06-23000000", Passwordhash = "abc", Emailaddress = "laura@mwisoftware.nl",    Status = "admin, staff, student")
U2 = Users(Username = "Vincent",  Lastname = "Ccccc",    Firstname = "Cc", Phone = "06-34000000", Passwordhash = "abc", Emailaddress = "vincent@mwisoftware.nl",  Status = "staff, student")
U3 = Users(Username = "Annelies", Lastname = "Dddddddd", Firstname = "Dd", Phone = "06-45000000", Passwordhash = "abc", Emailaddress = "Annelies@mwisoftware.nl", Status = "student")
U4 = Users(Username = "Bea",      Lastname = "Eeeee",    Firstname = "Ee", Phone = "06-56000000", Passwordhash = "abc", Emailaddress = "Bea@mwisoftware.nl",      Status = "student")
U5 = Users(Username = "Caroline", Lastname = "Fffff",    Firstname = "Ff", Phone = "06-67000000", Passwordhash = "abc", Emailaddress = "Caroline@mwisoftware.nl", Status = "student")
U6 = Users(Username = "Debora",   Lastname = "Gggg",     Firstname = "Gg", Phone = "06-78000000", Passwordhash = "abc", Emailaddress = "debora@mwisoftware.nl",   Status = "student")
U7 = Users(Username = "Evelien",  Lastname = "Hhhhh",    Firstname = "Hh", Phone = "06-89000000", Passwordhash = "abc", Emailaddress = "evelien@mwisoftware.nl",  Status = "student")
with app.app_context():
    db.session.add(U0)
    db.session.add(U1)
    db.session.add(U2)
    db.session.add(U3)
    db.session.add(U4)
    db.session.add(U5)
    db.session.add(U6)
    db.session.add(U7)
    db.session.commit()

#--------------------------------------------------------------------------

from Package.models import Appointments
from Package import app, db

# source: https://docs.python.org/3/library/datetime.html#examples-of-usage-datetime

from datetime import datetime, date, time, timezone
date1 = datetime.now() 
d = date(2024, 8, 25)
t = time(19,30)
date2 = datetime.combine(d, t)
d = date(2024, 8, 25)
t = time(19,15)
date3 = datetime.combine(d, t)

A0 = Appointments(User = 3, Product = 2, Part = "ZW1", Date = date3, Time = "19.00", Notes = "free text 11", Staff = 3)
A1 = Appointments(User = 3, Product = 2, Part = "ZW2", Date = date2, Time = "19.00", Notes = "free text 222222", Staff = 4)
with app.app_context():
    db.session.add(A0)
    db.session.add(A1)
    db.session.commit()

#Id, User, Product, Part, Date, Time, Notes, Staff

#--------------------------------------------------------------------------


from Package import Users
from Package import db
from Package import app
with app.app_context():
    for User in Users.query.all():
        User.Id
        User.Username
        User.Emailaddress
        User.Status
#--------------------------------------------------------------------------



with app.app_context():
    Products.query.filter_by(Price=300)

with app.app_context():
    from Package import Products
    #for Product in Products.query.filter_by(Price=500):
    for Product in Products.query.all():
        Product.Id
        Product.Productname
        Product.Abbr
        Product.Parts
        Product.Price
#--------------------------------------------------------------------------
from Package import products
with app.app_context():
    pro0=products(name = 'DSD')
    db.session.add(pro0)
    db.session.commit()
#--------------------------------------------------------------------------
from Package import products
pro0=products(name = 'DSD')
db.session.add(pro0)
db.session.commit()
#--------------------------------------------------------------------------
from Package import products
pro0 = products(abbr = 'DSD')
db.session.add(pro0)
db.session.commit()
#--------------------------------------------------------------------------
#source: https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/
from Package import products
me = products(4,'DiscoverScubaDiving', 'DSD', 'DSD', 50)
db.session.add(me)
db.session.commit()

from Package import appointments
#me = appointments('4','1','1','23:45','test','1')
me = appointments(4)
# id,user,product,time,name,staff
db.session.add(me)
db.session.commit()

#--------------------------------------------------------------------------
from Package import Test, app

test0 = Test(firstname='martin', lastname="van willigen", email="mvwilligen@hotmail.com")

with app.app_context():
    db.session.add(test0)
    db.session.commit()
#--------------------------------------------------------------------------
from Package import app, Products

Prod0 = Products(Productname='martin', Abbr='MVW')

with app.app_context():
    db.session.add(Prod0)
    db.session.commit()
#--------------------------------------------------------------------------
from Package import appointments
with app.app_context():
    app0=appointments(time = '12:34')
    db.session.add(app0)
    db.session.commit()


from Package import appointments
with app.app_context():
    for appointment in appointments.query.filter_by(time='12:34'):
        appointment.id
        appointment.time

        
#--------------------------------------------------------------------------
from Package import app
from Package import db
from Package.models import Users

with app.app_context():
    Users.query.filter_by(Firstname='abc').all()
    Users.query.filter_by(Firstname='abc').first()

#--------------------------------------------------------------------------
#works

from Package import app
from Package import db
from Package.models import Users, Products

with app.app_context():
    products = Products.query.all()
    for product in products:
        product.Id
        product.Productname


#--------------------------------------------------------------------------
# works also! :-D

from Package import app
from Package import db
from Package.models import Users, Products

app.app_context().push()

products = Products.query.all()

for product in products:
    product.Id
    product.Productname

#--------------------------------------------------------------------------
# works

from Package import app
from Package import db
from Package.models import Users
user = db.session.execute(db.select(Users).filter_by(Id=int(9))).scalar_one()
user.Firstname='testt'
user.Lastname='testing'
user.Emailaddress='test@testing.nl'
user.Phone='06-12345678'
user.Status='new'
db.session.commit()


#--------------------------------------------------------------------------
# works

from Package.models import Users
id=9
user = Users.query.filter_by(Id=int(id)).first()
user.Id
user.Firstname



# --------------------------------------------------------------------------
# source: https://waynerv.github.io/flask-mailman/
# does not work yet

from flask import Flask #, render_template

app = Flask(__name__)

app.app_context().push()

from flask_mailman import Mail
app.config['MAIL_SERVER'] = 'mail.nwilligen.nl'
app.config['MAIL_PORT'] = '465'
app.config['MAIL_USERNAME'] = 'pv'
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

from flask_mailman import EmailMessage
msg = EmailMessage(
    'Hello',
    'Body goes here',
    'pv@nwilligen.nl',
    ['mvwilligen@hotmail.com'],
    headers={'Message-ID': 'foo'},
    )
msg.send()

# --------------------------------------------------------------------------

from Package import app
from Package import db
from Package.models import Users, Products, Appointments

appointments = db.session.execute(db.select(Appointments).filter_by(User=1)).scalars()

for a in appointments:
    a.Id
    a.User
    a.User.Username


# --------------------------------------------------------------------------

parts = "Intro|ZW1|ZW2|ZW3|Exam|BW1|BW2|BW3"
part = ""
for b in parts:
    if b == "|":
        print(part)
        part = ""
    else:
        part = part + b

# --------------------------------------------------------------------------

from Package import app, db
from Package.models import Users, Products, Appointments
from datetime import datetime
from sqlalchemy import func, and_
for m in range(9,10):
    for d in range(4,5):
        seldate = datetime(2024, m, d)
        seldate2 = datetime(2024, m, d + 1)
        # works: appointments = db.session.query(Appointments).order_by(Appointments.Date).filter(func.DATE(Appointments.Date) >= datetime(2024,9,1)).all()
        print("----------------------------------")
        appointments = db.session.query(Appointments).order_by(Appointments.Date).filter(func.DATE(Appointments.Date) >= datetime(2024,9,6)).all()
        for a in appointments:
            print(a.Date.strftime("%d-%m-%Y %H:%M:%S") + " " + "user:"+str(a.User) +  "  product:" + str(a.Product) + " part:" + a.Part + " " + a.Time + " staff:" + str(a.Staff) + " " + a. Notes)
        print("----------------------------------")
        # works: 
        appointments = db.session.query(Appointments).order_by(Appointments.Date).where(and_(func.DATE(Appointments.Date) > datetime(2024,9,6), func.DATE(Appointments.Date) <= datetime(2024,9,7))).all()
        for a in appointments:
            print(str(a.User) +  "  " + str(a.Product) + " " + a.Part + " " + a.Date.strftime("%d-%m-%Y %H:%M:%S") + " " + a.Time + " " + str(a.Staff) + " " + a. Notes)
        print("----------------------------------")
        # does not work: 
        appointments = db.session.query(Appointments).order_by(Appointments.Date).where(func.DATE(Appointments.Date) == datetime(2024,9,7)).all()
        appointments = db.session.query(Appointments).order_by(Appointments.Date).filter(func.DATE(Appointments.Date) == datetime(2024,9,7)).all()
        for a in appointments:
            print(str(a.User) +  "  " + str(a.Product) + " " + a.Part + " " + a.Date.strftime("%d-%m-%Y %H:%M:%S") + " " + a.Time + " " + str(a.Staff) + " " + a. Notes)
        print("----------------------------------")

# --------------------------------------------------------------------------

today = datetime.datetime.now()
day_of_year = (today - datetime.datetime(today.year, 1, 1)).days + 1
print(day_of_year)

from datetime import date

# date object of today's date
today = date.today() 

print("Current year:", today.year)
print("Current month:", today.month)
print("Current day:", today.day)

datetime.datetime.today().weekday()

datetime.datetime(2024,8,24).weekday()
datetime.datetime(2024,8,1).weekday()

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
        return s[offset:offset+amount]

datetime.datetime(2024,8,26).weekday()
cWeekdays = "MonTueWedThuFriSatSun"
cWeekday = mid(cWeekdays, ((datetime.datetime(2024,8,26).weekday()) * 3), 3)
print(cWeekday)               

# --------------------------------------------------------------------------
# works
from Package.models import a, b
results = db.session.execute(    db.select(b.b_id, b.b_name, a.a_name).select_from(b).join(a, b.b_a_id == a.a_id)    ) 
for row in results: 
    print(row) 

# testing
results = db.session.execute(    db.select(numbers2.numbers2_id, numbers2.numbers2_name, names2.names2_name).select_from(numbers).join(names2, numbers2.numbers2_names2_id == names2.names2_id) ) 
for row in results: 
    print(row) 

# works

results = db.session.execute(    db.select(Appointments.Id, Appointments.User, Appointments.Notes, Users.Username).select_from(Appointments).join(Users, Appointments.User == Users.Id) ) 
for row in results: 
    print(row) 

# works

results = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname).select_from(Appointments).join(Users, Appointments.User == Users.Id).join(Products, Appointments.Product == Products.Id) ) 
for row in results: 
    print(row) 

#works! :-D
#                                          0                  1                  2                3                  4                      5             6
from sqlalchemy import func, and_
results = db.session.execute( db.select(Appointments.Id, Appointments.User, Users.Firstname, Users.Lastname, Products.Productname, Appointments.Part, Appointments.Date). \
                              order_by(Appointments.Date). \
                              where(and_(func.DATE(Appointments.Date) > datetime(2024,9,1), func.DATE(Appointments.Date) <= datetime(2024,9,10))). \
                              select_from(Appointments). \
                              join(Users, Appointments.User == Users.Id). \
                              join(Products, Appointments.Product == Products.Id) ) 
for row in results:
    print ( row[6].strftime("%d-%m-%Y %H:%M:%S") + " - " + row [2]  + " " + row [3] + " - " +  row[4] + "-" + row[5])


# models.py
# class a(db.Model):
#    __tablename__ = 'as'
#    a_id    = db.Column(db.Integer(),                  primary_key=True)
#    a_name  = db.Column(db.String(30))
#    a_text  = db.Column(db.String(30))
#
#    bs = relationship('b', back_populates = "customer")
#
#    def __repr__(self):
#        return f'products {self.name}'
#
#
# class b(db.Model):
#    __tablename__ = 'bs'
#    b_id   = db.Column(db.Integer(),                  primary_key=True)
#    b_a_id = db.Column(db.Integer(), ForeignKey('as.a_id'))
#    b_name = db.Column(db.String(30))
#
#    customer = relationship('a', back_populates="bs")
#
#    def __repr__(self):
#        return f'products {self.name}'
# --------------------------------------------------------------------------

exec(open('c:\data\python\divescheduling\package\__init__.py').read())

# --------------------------------------------------------------------------

# import os
# os.urandom(12).hex(12)

# >>> os.urandom(12).hex()
# 'ec9bb7d32448dd860d3199a2'
# >>>

#--------------------------------------------------------------------------

#jinja2:start<br>
#{% for a in appointment %}
#  a:{{ a }}<br>
#  {% for b in a %}
#    b:{{ b }}<br>
#  {% endfor %}
#{% endfor %}
#jinja2:finish<br>


#cDebug:<br><br>
#{% autoescape false %}
#{{ cDebug | replace("#BR#", "<br>") }}
#{% endautoescape %}
#
#    {% autoescape false %}
#    {{ cAppointments | replace("#BR#", "<br>") }}
#    {% endautoescape %}

#--------------------------------------------------------------------------

    appointments2 = []

    # export data in csv-format
    cAppointments = ""
    cUser = ""
    for row in appointments:
        if cUser != row [3] + row [4]:
            cUser = row [3] + row [4]

            appointments2.append(row)

            for element in row:
                if isinstance(element, int):
                    cAppointments = cAppointments + str(element) + "; "
                elif isinstance(element, datetime.date):
                    cAppointments = cAppointments + element.strftime("%d-%m-%Y") + "; "
                elif isinstance(element, datetime.datetime):
                    cAppointments = cAppointments + element.strftime("%d-%m-%Y") + "; "
                else:
                    cAppointments = cAppointments + element + "; "
            cAppointments = cAppointments + '#BR#'


#    current_user.name: {{ current_user.name }}
#    | current_user.is_active:
#    {% if current_user.is_active %}
#        true
#    {% else %}
#        false
#    {% endif %}
#    | current_user.is_authenticated:
#    {% if current_user.is_authenticated %}
#        true
#    {% else %}
#        false
#    {% endif %}
#    | current_user.is_anonymous:
#    {% if current_user.is_anonymous %}
#        true
#    {% else %}
#        false
#    {% endif %}
#    | current_user.get_id:
#    {% if current_user.get_id %}
#        true
#    {% else %}
#        false
#    {% endif %}

cInstructors: {{ cInstructors|safe }}



    #     ######  ##     ## ######## ########  
    #    ##    ## ###   ###    ##    ##     ## 
    #    ##       #### ####    ##    ##     ## 
    #     ######  ## ### ##    ##    ########  
    #          ## ##     ##    ##    ##        
    #    ##    ## ##     ##    ##    ##        
    #     ######  ##     ##    ##    ##        

    # inspiration: https://realpython.com/python-send-email/

    if False:

        import smtplib, ssl

        port           = 587  # For starttls
        smtp_server    = "mail.mwihosting.nl"
        sender_email   = "martin@mwihosting.nl"
        receiver_email = "mvwilligen@hotmail.com"
        password       = "hjhjJFGHJHGF689769876!:-oi"

        Message = "From: martin@mwihosting.nl" + chr(13) + chr(10)
        Message = Message + "To: mvwilligen@hotmail.com" + chr(13) + chr(10)
        Message = Message + "Subject: Hello World! [0718]" + chr(13) + chr(10)
        Message = Message + "1... 2... 3... 4...." + chr(13) + chr(10)
        Message = Message + "Hoedje van papier..." + chr(13) + chr(10)
        Message = Message + "" + chr(13) + chr(10)

        context        = ssl.create_default_context()

        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, Message)

        receiver_email = "mvwilligen@gmail.com"

        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, Message)

    if False:

        import smtplib, ssl
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        sender_email       = "martin@mwihosting.nl"
        receiver_email     = "mvwilligen@gmail.com"
        password           = "hjhjJFGHJHGF689769876!:-oi"

        message            = MIMEMultipart("alternative")
        message["Subject"] = "multipart test"
        message["From"]    = sender_email
        message["To"]      = receiver_email

        cMessageHtml =                "<html><body>" + chr(13) + chr(10)
        cMessageHtml = cMessageHtml + "<br>" + chr(13) + chr(10)
        cMessageHtml = cMessageHtml + "Hello, here are the results for the first three weeks.<br>" + chr(13) + chr(10)
        cMessageHtml = cMessageHtml + "<br>" + chr(13) + chr(10)
        cMessageHtml = cMessageHtml + "<table style='border: 1px solid;'>" + chr(13) + chr(10)
        cMessageHtml = cMessageHtml + "<tr style='border: 1px solid;'><td colspan=3 style='text-align: center;' >Results</td></tr>" + chr(13) + chr(10)
        cMessageHtml = cMessageHtml + "<tr><td><b>week</b></td><td><b>product</b></td><td><b>total</b></td></tr>" + chr(13) + chr(10)
        cMessageHtml = cMessageHtml + "<tr><td>1</td><td>DSD</td><td>100</td></tr>" + chr(13) + chr(10)
        cMessageHtml = cMessageHtml + "<tr><td>2</td><td>OW</td><td>900</td></tr>" + chr(13) + chr(10)
        cMessageHtml = cMessageHtml + "<tr><td>3</td><td>AOW</td><td>1900</td></tr>" + chr(13) + chr(10)
        cMessageHtml = cMessageHtml + "<tr><td></td><td>total</td><td>2900</td></tr>" + chr(13) + chr(10)
        cMessageHtml = cMessageHtml + "</table>" + chr(13) + chr(10)
        cMessageHtml = cMessageHtml + "<br>" + chr(13) + chr(10)
        cMessageHtml = cMessageHtml + "With regards,<br>" + chr(13) + chr(10)
        cMessageHtml = cMessageHtml + "<br>" + chr(13) + chr(10)
        cMessageHtml = cMessageHtml + "Martin<br>" + chr(13) + chr(10)
        cDate5 = "01-01-2024"
        cTime2 = "12:34"
        cMessageHtml = cMessageHtml + "<br><br><p style='font-size: 12px;'>powered by divescheduling. created:" + cDate5 + " " + cTime2 + "</p>"
        cMessageHtml = cMessageHtml + "</body></html>" + chr(13) + chr(10)

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(cMessage, "plain")
        part2 = MIMEText(cMessageHtml, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("mail.mwihosting.nl", 465, context=context) as server:   #587
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )


   ###    ########   ######  ########  ######## ########                                                                              
  ## ##   ##     ## ##    ## ##     ## ##       ##                                                                                    
 ##   ##  ##     ## ##       ##     ## ##       ##                                                                                    
##     ## ########  ##       ##     ## ######   ######                                                                                
######### ##     ## ##       ##     ## ##       ##                                                                                    
##     ## ##     ## ##    ## ##     ## ##       ##                                                                                    
##     ## ########   ######  ########  ######## ##                      
                                                                 
 ######   ##     ## ####       ## ##    ## ##                                                                                         
##    ##  ##     ##  ##        ## ##   ##  ##                                                                                         
##        ##     ##  ##        ## ##  ##   ##                                                                                         
##   #### #########  ##        ## #####    ##                                                                                         
##    ##  ##     ##  ##  ##    ## ##  ##   ##                                                                                         
##    ##  ##     ##  ##  ##    ## ##   ##  ##                                                                                         
 ######   ##     ## ####  ######  ##    ## ########                                                                                   

##     ## ##    ##  #######  ########   #######  ########                                                                             
###   ### ###   ## ##     ## ##     ## ##     ## ##     ##                                                                            
#### #### ####  ## ##     ## ##     ## ##     ## ##     ##                                                                            
## ### ## ## ## ## ##     ## ########  ##     ## ########                                                                             
##     ## ##  #### ##     ## ##        ##  ## ## ##   ##                                                                              
##     ## ##   ### ##     ## ##        ##    ##  ##    ##                                                                             
##     ## ##    ##  #######  ##         ##### ## ##     ##                                                                            

 ######  ######## ##     ## ##     ## ##      ## ##     ##                                                                            
##    ##    ##    ##     ## ##     ## ##  ##  ##  ##   ##                                                                             
##          ##    ##     ## ##     ## ##  ##  ##   ## ##                                                                              
 ######     ##    ##     ## ##     ## ##  ##  ##    ###                                                                               
      ##    ##    ##     ##  ##   ##  ##  ##  ##   ## ##                                                                              
##    ##    ##    ##     ##   ## ##   ##  ##  ##  ##   ##                                                                             
 ######     ##     #######     ###     ###  ###  ##     ##                                                                            

##    ## ########                                                                                                                     
 ##  ##       ##                                                                                                                      
  ####       ##                                                                                                                       
   ##       ##                                                                                                                        
   ##      ##                                                                                                                         
   ##     ##                                                                                                                          
   ##    ########                                                                                                                     

  #####      ##    #######   #######  ##        ########  #######  ########  #######   #######    #####                               
 ##   ##   ####   ##     ## ##     ## ##    ##  ##       ##     ## ##    ## ##     ## ##     ##  ##   ##                              
##     ##    ##          ##        ## ##    ##  ##       ##            ##   ##     ## ##     ## ##     ##                             
##     ##    ##    #######   #######  ##    ##  #######  ########     ##     #######   ######## ##     ##                             
##     ##    ##   ##               ## #########       ## ##     ##   ##     ##     ##        ## ##     ##                             
 ##   ##     ##   ##        ##     ##       ##  ##    ## ##     ##   ##     ##     ## ##     ##  ##   ##                              
  #####    ###### #########  #######        ##   ######   #######    ##      #######   #######    #####                               

####  ####      ####  #######    ## ##    ########  #####   ##     ###     ####                ### ###                                
#### ##  ##  ## #### ##     ##   ## ##   ##  ##  ## ## ##  ##     ## ##   ##  ##    ##   ##   ##     ##                    ##         
 ##       ####  #### ## ### ## ######### ##  ##     ##### ##     ##   ##   ####      ## ##   ##       ##                   ##   ##### 
  ##             ##  ## ### ##   ## ##    ########       ##               ####     ######### ##       ##         ####### ######       
                     ## #####  #########     ##  ##     ## #####         ##  ## ##   ## ##   ##       ##                   ##   ##### 
                #### ##          ## ##   ##  ##  ##    ##  ## ##         ##   ##    ##   ##   ##     ##                    ##         
                ####  #######    ## ##    ########    ##   #####          ####  ##             ### ###   #######                      

###### ###### ##         #### ####   ##                                                                                               
##         ##  ##       ##       ##  ##                                                                                               
##         ##   ##      ##       ##  ##                                                                                               
##         ##    ##    ###       ###                                                                                                  
##         ##     ##    ##       ##  ##                                                                                               
##         ##      ##   ##       ##  ##                                                                                               
###### ######       ##   #### ####   ##                                                                                               

#### ####  ##  #### ####                ##    ## ##     #######                                                                       
#### #### #### #### ####               ##    ##   ##   ##     ##                                                                      
      ##   ##   ##   ##               ##    ##     ##        ##                                                                       
#### ##                  ####        ##    ##       ##     ###                                                                        
####       ##            ####       ##      ##     ##     ##                                                                          
 ##       ####            ##  ###  ##        ##   ##                                                                                  
##         ##            ##   ### ##          ## ##       ##                                                                          

      ##                                                                                                                              
     ##   ##   ##            ##                                                                                                       
    ##     ## ##             ##                                                                                                       
   ##    ######### ####### ######                                                                                                     
  ##       ## ##             ##                                                                                                       
 ##       ##   ##            ##   ###                                                                                                 
##                                ###                                                                                                 


                                                                                                                                      
                                                                                                                                      
                                                                                                                                      
                                                                                                                                      
                                                                                                                                      
                                                                                                                                      
                                                                                                                                      

   ###       
  ## ##      
 ##   ##     
##     ##    
#########    
##     ##    
##     ##    
########     
##     ##    
##     ##    
########     
##     ##    
##     ##    
########     
 ######      
##    ##     
##           
##           
##           
##    ##     
 ######      
########     
##     ##    
##     ##    
##     ##    
##     ##    
##     ##    
########     
########     
##           
##           
######       
##           
##           
########     
########     
##           
##           
######       
##           
##           
##           
 ######      
##    ##     
##           
##   ####    
##    ##     
##    ##     
 ######      
##     ##    
##     ##    
##     ##    
#########    
##     ##    
##     ##    
##     ##    
####         
 ##          
 ##          
 ##          
 ##          
 ##          
####         
      ##     
      ##     
      ##     
      ##     
##    ##     
##    ##     
 ######      
##    ##     
##   ##      
##  ##       
#####        
##  ##       
##   ##      
##    ##     
##           
##           
##           
##           
##           
##           
########     
##     ##    
###   ###    
#### ####    
## ### ##    
##     ##    
##     ##    
##     ##    
##    ##     
###   ##     
####  ##     
## ## ##     
##  ####     
##   ###     
##    ##     
 #######     
##     ##    
##     ##    
##     ##    
##     ##    
##     ##    
 #######     
########     
##     ##    
##     ##    
########     
##           
##           
##           
 #######     
##     ##    
##     ##    
##     ##    
##  ## ##    
##    ##     
 ##### ##    
########     
##     ##    
##     ##    
########     
##   ##      
##    ##     
##     ##    
 ######      
##    ##     
##           
 ######      
      ##     
##    ##     
 ######      
########     
   ##        
   ##        
   ##        
   ##        
   ##        
   ##        
##     ##    
##     ##    
##     ##    
##     ##    
##     ##    
##     ##    
 #######     
##     ##    
##     ##    
##     ##    
##     ##    
 ##   ##     
  ## ##      
   ###       
##      ##   
##  ##  ##   
##  ##  ##   
##  ##  ##   
##  ##  ##   
##  ##  ##   
 ###  ###    
##     ##    
 ##   ##     
  ## ##      
   ###       
  ## ##      
 ##   ##     
##     ##    
##    ##     
 ##  ##      
  ####       
   ##        
   ##        
   ##        
   ##        
########     
     ##      
    ##       
   ##        
  ##         
 ##          
########     
   ##        
 ####        
   ##        
   ##        
   ##        
   ##        
 ######      
 #######     
##     ##    
       ##    
 #######     
##           
##           
#########    
 #######     
##     ##    
       ##    
 #######     
       ##    
##     ##    
 #######     
##           
##    ##     
##    ##     
##    ##     
#########    
      ##     
      ##     
########     
##           
##           
#######      
      ##     
##    ##     
 ######      
 #######     
##     ##    
##           
########     
##     ##    
##     ##    
 #######     
########     
##    ##     
    ##       
   ##        
  ##         
  ##         
  ##         
 #######     
##     ##    
##     ##    
 #######     
##     ##    
##     ##    
 #######     
 #######     
##     ##    
##     ##    
 ########    
       ##    
##     ##    
 #######     
  #####      
 ##   ##     
##     ##    
##     ##    
##     ##    
 ##   ##     
  #####      
####         
####         
 ##          
  ##         
             
             
             
 ####        
##  ##  ##   
     ####    
             
             
             
             
####         
####         
####         
 ##          
             
####         
####         
 #######     
##     ##    
## ### ##    
## ### ##    
## #####     
##           
 #######     
  ## ##      
  ## ##      
#########    
  ## ##      
#########    
  ## ##      
  ## ##      
 ########    
##  ##  ##   
##  ##       
 ########    
    ##  ##   
##  ##  ##   
 ########    
#####   ##   
## ##  ##    
##### ##     
     ##      
    ## ##### 
   ##  ## ## 
  ##   ##### 
  ###        
 ## ##       
##   ##      
             
             
             
             
  ####       
 ##  ##      
  ####       
 ####        
##  ## ##    
##   ##      
 ####  ##    
             
 ##   ##     
  ## ##      
#########    
  ## ##      
 ##   ##     
             
  ###        
 ##          
##           
##           
##           
 ##          
  ###        
###          
  ##         
   ##        
   ##        
   ##        
  ##         
###          
             
             
             
             
             
             
#######      
             
  ##         
  ##         
######       
  ##         
  ##         
             
             
             
             
#######      
             
             
             
             
             
#####        
             
#####        
             
             
######       
##           
##           
##           
##           
##           
######       
######       
    ##       
    ##       
    ##       
    ##       
    ##       
######       
##           
 ##          
  ##         
   ##        
    ##       
     ##      
      ##     
  ####       
 ##          
 ##          
###          
 ##          
 ##          
  ####       
####         
   ##        
   ##        
   ###       
   ##        
   ##        
####         
##           
##           
##           
             
##           
##           
##           
####         
####         
             
####         
####         
 ##          
##           
####         
####         
 ##          
##           
             
             
             
 ##          
####         
 ##          
             
 ##          
####         
 ##          
#### ####    
#### ####    
 ##   ##     
             
             
             
             
             
             
             
####         
####         
 ##          
##           
             
             
             
             
             
###          
###          
      ##     
     ##      
    ##       
   ##        
  ##         
 ##          
##           
   ##        
  ##         
 ##          
##           
 ##          
  ##         
   ##        
##           
 ##          
  ##         
   ##        
  ##         
 ##          
##           
 #######     
##     ##    
      ##     
    ###      
   ##        
             
   ##        
             
             
             
             
             
             
             
      ##     
     ##      
    ##       
   ##        
  ##         
 ##          
##           
             
 ##   ##     
  ## ##      
#########    
  ## ##      
 ##   ##     
             
             
             
             
#######      
             
             
             
             
  ##         
  ##         
######       
  ##         
  ##         
             
             
             
             
             
             
###          
###          
             
##################################################
# source: https://www.w3schools.com/howto/howto_js_filter_lists.asp

# <script>
#     function myFunction() {
#       // Declare variables
#       var input, filter, ul, li, a, i, txtValue;
#       input = document.getElementById('myInput');
#       filter = input.value.toUpperCase();
#       ul = document.getElementById("myUL");
#       li = ul.getElementsByTagName('li');
    
#       // Loop through all list items, and hide those who don't match the search query
#       for (i = 0; i < li.length; i++) {
#         a = li[i].getElementsByTagName("a")[0];
#         txtValue = a.textContent || a.innerText;
#         if (txtValue.toUpperCase().indexOf(filter) > -1) {
#           li[i].style.display = "";
#         } else {
#           li[i].style.display = "none";
#         }
#       }
#     }
# </script>

# <h3>users</h3><br>

# <input type="text" id="myInput" onkeyup="myFunction()" placeholder="Search for names..">

# <ul id="myUL">
#     {% for u in users %}
#         <li><a href="#">{{ u.Firstname }} {{ u.Lastname }}</a></li>
#     {% endfor %}
# </ul>


# {% extends 'base.html' %}

# {% block title %}
# users
# {% endblock %}

# {% block content %}

# <script>
#     function myFunction() {
#       // Declare variables
#       var input, filter, ul, li, a, i, txtValue;
#       input = document.getElementById('myInput');
#       filter = input.value.toUpperCase();
#       ul = document.getElementById("myUL");
#       li = ul.getElementsByTagName('li');
    
#       // Loop through all list items, and hide those who don't match the search query
#       for (i = 0; i < li.length; i++) {
#         a = li[i].getElementsByTagName("a")[0];
#         txtValue = a.textContent || a.innerText;
#         if (txtValue.toUpperCase().indexOf(filter) > -1) {
#           li[i].style.display = "";
#         } else {
#           li[i].style.display = "none";
#         }
#       }
#     }
# </script>

# <h3>users</h3><br>

# <input type="text" id="myInput" onkeyup="myFunction()" placeholder="Search for names..">

# <ul id="myUL">
#     {% for u in users %}
#         <li><a href="#">{{ u.Firstname }} {{ u.Lastname }}</a></li>
#     {% endfor %}
# </ul>

# {% endblock %}
