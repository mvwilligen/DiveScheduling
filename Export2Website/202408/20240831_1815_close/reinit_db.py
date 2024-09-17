# ########  ######## #### ##    ## #### ########         ########  ########      ########  ##    ##    
# ##     ## ##        ##  ###   ##  ##     ##            ##     ## ##     ##     ##     ##  ##  ##     
# ##     ## ##        ##  ####  ##  ##     ##            ##     ## ##     ##     ##     ##   ####      
# ########  ######    ##  ## ## ##  ##     ##            ##     ## ########      ########     ##       
# ##   ##   ##        ##  ##  ####  ##     ##            ##     ## ##     ##     ##           ##       
# ##    ##  ##        ##  ##   ###  ##     ##            ##     ## ##     ## ### ##           ##       
# ##     ## ######## #### ##    ## ####    ##    ####### ########  ########  ### ##           ##  
# 
# https://patorjk.com/software/taag/#p=display&f=Banner3&t=reinit_db.py%20     

# added 20240831 1509 - issues with reinit_db.py
# removed 20240831 1509 - issues with reinit_db.py

from Package          import db
from Package import app
from Package.models import Products, Users, Appointments, names, numbers, Instructors
import datetime

from werkzeug.security import generate_password_hash, check_password_hash

print('---- start:  1.py')

# exec(open('c:\data\python\divescheduling\package\__init__.py').read())

print("---- drop tables")

with app.app_context():
    db.drop_all()

print("---- create db")

with app.app_context():
    db.create_all()

#print('---- populate names')
#
#a1 = names(names_name = "One",   names_text = '1')
#
#with app.app_context():
#    db.session.add(a1)
#    db.session.commit()
#
#print('---- populate names more')
#
#a2 = names(names_name = "Two",   names_text = '22')
#a3 = names(names_name = "Three", names_text = '333')
#a4 = names(names_name = "Four",  names_text = '4444')
#a5 = names(names_name = "Five",  names_text = '55555')
#
#with app.app_context():
#    db.session.add(a2)
#    db.session.add(a3)
#    db.session.add(a4)
#    db.session.add(a5)
#    db.session.commit()
#
# class b(db.model):
#    B_Id   = db.Column(db.Integer(),                  primary_key=True)
#    B_A_ID = db.Column(db.Integer())
#    B_Name = db.Column(db.String(30))
#
#print('---- populate numbers')
#
#b1 = numbers(numbers_names_id = 1,   numbers_name = 'one')
#with app.app_context():
#    db.session.add(b1)
#    db.session.commit()
#
#print('---- populate numbers more')
#
#b2 = numbers(numbers_names_id = 4,   numbers_name = 'four')
#b3 = numbers(numbers_names_id = 3,   numbers_name = 'three')
#b4 = numbers(numbers_names_id = 2,   numbers_name = 'two')
#b5 = numbers(numbers_names_id = 2,   numbers_name = 'two')
#b6 = numbers(numbers_names_id = 1,   numbers_name = 'one')
#b7 = numbers(numbers_names_id = 5,   numbers_name = 'five')
#with app.app_context():
#    db.session.add(b2)
#    db.session.add(b3)
#    db.session.add(b4)
#    db.session.add(b5)
#    db.session.add(b6)
#    db.session.add(b7)
#    db.session.commit()
#
#print('---- list numbers')
#
#results = db.session.execute(    db.select(numbers.numbers_id, numbers.numbers_name, names.names_name, names.names_text).select_from(numbers).join(names, numbers.numbers_names_id == names.names_id) ) 
#for row in results: 
#    print(row) 

print('---- populate products')
P1 = Products(Productname = "DiscoverScubaDiving", Abbr = "DSD", Parts = "DSD",                                            Price = 50,  Description = "omschrijving DSD")
with app.app_context():
    db.session.add(P1)
    db.session.commit()

print('---- populate products more')

P2 = Products(Productname = "OpenWater",           Abbr = "OW",  Parts = "Intro|ZW1|ZW2|ZW3|Exam|BW1|BW2|BW3",             Price = 0, Description = 'omschrijving OW')
P3 = Products(Productname = "AdvancedOpenWater",   Abbr = "AOW", Parts = "Intro|ZW1|ZW2|ZW3|ZW4|ZW5|Exam|BW1|BW2|BW3|BW4", Price = 0, Description = 'omschrijving AOW')
P4 = Products(Productname = "DiveMaster",          Abbr = "DM",  Parts = "Intro|ZW1|ZW2|ZW3|Exam|BW1|BW2|BW3|BW4",         Price = 0, Description = 'omschrijving DM')
P5 = Products(Productname = "Nachtduikert",        Abbr = "N",   Parts = "Theory|BW",                                      Price = 0, Description = 'omschrijving ND')

with app.app_context():
    db.session.add(P2)
    db.session.add(P3)
    db.session.add(P4)
    db.session.add(P5)
    db.session.commit()

print('---- list products')

with app.app_context():
    for Product in Products.query.all():
        #Product.Id
        Product.Productname
        #Product.Abbr
        #Product.Parts
        #Product.Price

print('---- populate users')

pw     = 'abc'
pwhash = '1$UKmP9ivDwtdhcMAh$c22cb651eebf1cfdcf84d131df02621e4e8c64460eddf9d7817f9ad7f91fba40b6b84ffd90352825cb4a5cb4e9fe906571afc27e6ed6b4a964835f612922306a'

# >>> from werkzeug.security import generate_password_hash, check_password_hash
# >>> generate_password_hash('123')
# 'scrypt:32768:8:1$FSkijZHqhuxrKnuf$3cd6828d48e7e32d405b9406a2e7952e05d2e82229199d26d78c660c10fb02a765aa12be7c6cd19a25fc5dd57f8ced3f1cf84264da7d49eb4cea31da7035f208'
pw     = '123'
pwhash = 'scrypt:32768:8:1$FSkijZHqhuxrKnuf$3cd6828d48e7e32d405b9406a2e7952e05d2e82229199d26d78c660c10fb02a765aa12be7c6cd19a25fc5dd57f8ced3f1cf84264da7d49eb4cea31da7035f208'

U = Users(Username = "Admin",      Lastname = "Ad",            Firstname = "Min",      Phone = "06-11111111", Passwordhash = pwhash, Emailaddress = "Admin@mwisoftware.nl",      Status = "admin, staff")
U0 = Users(Username = "-",         Lastname = "-",             Firstname = "-",        Phone = ""           , Passwordhash = pwhash, Emailaddress = "",                          Status = "")
U1 = Users(Username = "Laura",     Lastname = "Maissan",       Firstname = "Laura",    Phone = "06-33333333", Passwordhash = pwhash, Emailaddress = "laura@mwisoftware.nl",      Status = "admin, staff, instructor")
U2 = Users(Username = "Vincent",   Lastname = "Maissan",       Firstname = "Vincent",  Phone = "06-44444444", Passwordhash = pwhash, Emailaddress = "vincent@mwisoftware.nl",    Status = "staff, instructor")
U3 = Users(Username = "Jeroen",    Lastname = "Maissan",       Firstname = "Jeroen",   Phone = "06-55555555", Passwordhash = pwhash, Emailaddress = "jeroen@mwisoftware.nl",     Status = "staff, instructor")
U4 = Users(Username = "Marga",     Lastname = "Maissan",       Firstname = "Marga",    Phone = "06-66666666", Passwordhash = pwhash, Emailaddress = "marga@mwisoftware.nl",      Status = "staff, instructor")
U5 = Users(Username = "Monique",   Lastname = "van der Linde", Firstname = "Monique",  Phone = "06-77777777", Passwordhash = pwhash, Emailaddress = "Monique@mwisoftware.nl",    Status = "staff, instructor")
U6 = Users(Username = "Annelies",  Lastname = "L",             Firstname = "Annelies", Phone = "06-88888888", Passwordhash = pwhash, Emailaddress = "Anneliesl@mwisoftware.nl",  Status = "student")
U6.Passwordhash = generate_password_hash(U6.Firstname.lower())
U7 = Users(Username = "Bea",       Lastname = "L",             Firstname = "Bea",      Phone = "06-99999999", Passwordhash = pwhash, Emailaddress = "Beal@mwisoftware.nl",       Status = "student")
U7.Passwordhash = generate_password_hash(U7.Firstname.lower())
U8 = Users(Username = "Caroline",  Lastname = "dG",            Firstname = "Caar",     Phone = "06-AAAAAAAA", Passwordhash = pwhash, Emailaddress = "Carolinedg@mwisoftware.nl", Status = "student")
U8.Passwordhash = generate_password_hash(U8.Firstname.lower())
U9 = Users(Username = "Debora",    Lastname = "vL",            Firstname = "Debora",   Phone = "06-BBBBBBBB", Passwordhash = pwhash, Emailaddress = "deboravl@mwisoftware.nl",   Status = "student")
U9.Passwordhash = generate_password_hash(U9.Firstname.lower())
U10 = Users(Username = "Evelien",  Lastname = "K",             Firstname = "Evelien",  Phone = "06-CCCCCCCC", Passwordhash = pwhash, Emailaddress = "evelienk@mwisoftware.nl",   Status = "student")
U10.Passwordhash = generate_password_hash(U10.Firstname.lower())
with app.app_context():
    db.session.add(U)
    db.session.add(U0)
    db.session.add(U1)
    db.session.add(U2)
    db.session.add(U3)
    db.session.add(U4)
    db.session.add(U5)
    db.session.add(U6)
    db.session.add(U7)
    db.session.add(U8)
    db.session.add(U9)
    db.session.add(U10)
    db.session.commit()

users = db.session.execute( db.select(Users.Id, Users.Firstname, Users.Lastname, Users.Status))

print('---- list users')

with app.app_context():
    for User in Users.query.all():
        #User.Id
        User.Username

print('---- populate instructors')

instructor_to_create = Instructors(User = 2,
                                   Name = '[none]')        
db.session.add(instructor_to_create)
db.session.commit()

for user in users:
    if 'instructor' in user.Status:

        instructor_to_create = Instructors(User = user.Id,
                                           Name = user.Firstname + " " + user.Lastname)        
        db.session.add(instructor_to_create)
        db.session.commit()

print('---- list instructors')

instructors = Instructors.query.all()
for i in instructors:
    #i.Id
    #i.User
    i.Name
print()

print('---- list instructors with join')

instructors = db.session.execute(db.select(Instructors.Name, Users.Firstname, Users.Lastname, Users.Status). \
                                select_from(Instructors). \
                                join(Users, Instructors.User == Users.Id) )
for i in instructors:
    print('Instructors.Name:' + i [0] + ' | Users.Firstname:' + i [1] + ' | Users.Lastname:' + i [2] + ' - ' + i [3])

print('---- list products')

with app.app_context():
    for Product in Products.query.all():
        #Product.Id
        Product.Productname
        #Product.Abbr
        #Product.Parts
        #Product.Price

print('---- populate appointments')

# from datetime import datetime, date, time, timezone

# source: https://docs.python.org/3/library/datetime.html#examples-of-usage-datetime

#date0 = datetime.datetime.now() 
#date0 = datetime.datetime.combine(datetime.date(2024, 8, 25), datetime.time(19,30))
#date1 = datetime.datetime.combine(datetime.date(2024, 8, 25), datetime.time(19,30))
#date2 = datetime.datetime.combine(datetime.date(2024, 8, 26), datetime.time(19,45))
#date3 = datetime.datetime.combine(datetime.date(2024, 8, 26), datetime.time(19,45))
#date4 = datetime.datetime.combine(datetime.date(2024, 8, 27), datetime.time(19,0))
#date5 = datetime.datetime.combine(datetime.date(2024, 8, 28), datetime.time(19,0))
#
#A0 = Appointments(User = 1, Product = 2, Part = "ZW1", Date = date0, Time = "19.30", Notes = "free text 11",     Staff = 3)
#A1 = Appointments(User = 1, Product = 2, Part = "ZW2", Date = date1, Time = "19.30", Notes = "free text 222222", Staff = 4)
#A2 = Appointments(User = 1, Product = 2, Part = "ZW3", Date = date2, Time = "19.45", Notes = "free text 11",     Staff = 3)
#A3 = Appointments(User = 2, Product = 2, Part = "ZW1", Date = date3, Time = "19.45", Notes = "free text 222222", Staff = 4)
#A4 = Appointments(User = 2, Product = 2, Part = "ZW2", Date = date4, Time = "19.00", Notes = "free text 222222", Staff = 4)
#A5 = Appointments(User = 2, Product = 2, Part = "ZW3", Date = date5, Time = "19.00", Notes = "free text 222222", Staff = 4)
#
#with app.app_context():
#    db.session.add(A0)
#    db.session.add(A1)
#    db.session.add(A2)
#    db.session.add(A3)
#    db.session.add(A4)
#    db.session.add(A5)
#    db.session.commit()

parts = "Intro|ZW1|ZW2|ZW3|Exam|BW1|BW2|BW3"
part = ""
t = 1
for b in parts:
    if b == "|":
        t = t + 3
        # print(part)
        date0 = datetime.datetime.combine(datetime.date(2024, 9, t), datetime.time(19,30))
        A0 = Appointments(User = 3, Product = 3, Part = part, Date = date0, Time = "19.30", Notes = "free text 11",     Staff = 3)
        db.session.add(A0)
        db.session.commit()
        part = ""
    else:
        part = part + b

parts = "Intro|ZW1|ZW2|ZW3|Exam|BW1|BW2|BW3|BW4"
part = ""
t = 1
for b in parts:
    if b == "|":
        t = t + 3
        # print(part)
        date0 = datetime.datetime.combine(datetime.date(2024, 9, t), datetime.time(19,30))
        A0 = Appointments(User = 4, Product = 4, Part = part, Date = date0, Time = "19.30", Notes = "free text 22",     Staff = 4)
        db.session.add(A0)
        db.session.commit()
        part = ""
    else:
        part = part + b

print('---- list appointments')

with app.app_context():
    for A in Appointments.query.all():
        A.Id
        A.User

print('---- finish:  1.py')

exit()
