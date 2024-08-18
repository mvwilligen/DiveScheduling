
from homepage import app, db
with app.app_context():
    db.create_all()

from homepage import db
from homepage import app
from homepage import products
#from homepage import users
#from homepage import events

#products0 = products(name = "DiscoverScubaDiving")

from homepage import products
from homepage import db
Products1 = Products(Productname = "DiscoverScubaDiving", Abbr = "DSD", Parts = "DSD",                                            Price = 50,  Description = "omschrijving DSD")
Products2 = Products(Productname = "Open Water",          Abbr = "OW",  Parts = "Intro|ZW1|ZW2|ZW3|Exam|BW1|BW2|BW3",             Price = 300, Description = 'omschrijving OW')
Products3 = Products(Productname = "AdvancedOpenWater",   Abbr = "DSD", Parts = "Intro|ZW1|ZW2|ZW3|ZW4|ZW5|Exam|BW1|BW2|BW3|BW4", Price = 500, Description = 'omschrijving AOW')
with app.app_context():
    db.session.add(Products1)
    db.session.add(Products2)
    db.session.add(Products3)
    db.session.commit()

Products.query.all()

from homepage import products
from homepage import db
from homepage import app
with app.app_context():
    for Product in Products.query.all():
        Product.Id
        Product.Productname
        Product.Abbr
        Product.Parts
        Product.Price


with app.app_context():
    Products.query.filter_by(Price=300)

with app.app_context():
    from homepage import Products
    #for Product in Products.query.filter_by(Price=500):
    for Product in Products.query.all():
        Product.Id
        Product.Productname
        Product.Abbr
        Product.Parts
        Product.Price

result = 

#--------------------------------------------------------------------------
from homepage import products
with app.app_context():
    pro0=products(name = 'DSD')
    db.session.add(pro0)
    db.session.commit()
#--------------------------------------------------------------------------
from homepage import products
pro0=products(name = 'DSD')
db.session.add(pro0)
db.session.commit()
#--------------------------------------------------------------------------
from homepage import products
pro0 = products(abbr = 'DSD')
db.session.add(pro0)
db.session.commit()
#--------------------------------------------------------------------------
#source: https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/
from homepage import products
me = products(4,'DiscoverScubaDiving', 'DSD', 'DSD', 50)
db.session.add(me)
db.session.commit()

from homepage import appointments
#me = appointments('4','1','1','23:45','test','1')
me = appointments(4)
# id,user,product,time,name,staff
db.session.add(me)
db.session.commit()

#--------------------------------------------------------------------------
from homepage import Test, app

test0 = Test(firstname='martin', lastname="van willigen", email="mvwilligen@hotmail.com")

with app.app_context():
    db.session.add(test0)
    db.session.commit()
#--------------------------------------------------------------------------
from homepage import app, Products

Prod0 = Products(Productname='martin', Abbr='MVW')

with app.app_context():
    db.session.add(Prod0)
    db.session.commit()
#--------------------------------------------------------------------------
from homepage import appointments
with app.app_context():
    app0=appointments(time = '12:34')
    db.session.add(app0)
    db.session.commit()


from homepage import appointments
with app.app_context():
    for appointment in appointments.query.filter_by(time='12:34'):
        appointment.id
        appointment.time
    
