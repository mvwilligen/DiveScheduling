from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///divescheduling.db'

db = SQLAlchemy(app)

class Products(db.Model):
    Id = db.Column(db.Integer(),           primary_key=True)
    Productname = db.Column(db.String(30),   nullable=True)
    Price = db.Column(db.Integer(),           nullable=True)
    Abbr = db.Column(db.String(5),    nullable=True)
    Parts = db.Column(db.String(50),   nullable=True)
    Description = db.Column(db.String(1024), nullable=True)

    def __repr__(self):
        return f'products {self.name}'


    
class users(db.Model):
    id=db.Column(db.Integer(),           primary_key=True)
    name=db.Column(db.String(length=30),   nullable=False, unique=False)
    passwordhash=db.Column(db.String(length=30),   nullable=False, unique=False)
    emailaddress=db.Column(db.String(length=50),   nullable=False, unique=False)
#
#    def __repr__(self):
#        return f'users {self.name}'

class appointments(db.Model):
    id=db.Column(db.Integer(),           primary_key=True)
    user=db.Column(db.Integer(),           nullable=True, unique=True)
    product=db.Column(db.Integer(),           nullable=True, unique=True)
    date=db.Column(db.DateTime(timezone=True))
    time=db.Column(db.String(length=5),    nullable=True, unique=False)
    name=db.Column(db.String(length=5),    nullable=True, unique=False)
    staff=db.Column(db.Integer(),           nullable=True, unique=True)
#
#    def __repr__(self):
#        return f'appointments {self.name}'



class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True))
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<Student {self.firstname}>'




@app.route('/')
@app.route('/home')
def homepage():
    return render_template('home.html')

@app.route('/products')
def products():
#    items = [
#    {'id': 1, 'name': 'DiscoverScubaDiving', 'abbr': 'DSD', 'parts': 'DSD','price':  50},
#    {'id': 2, 'name': 'OpenWater'          , 'abbr': 'OW',  'parts': 'Intro|ZW1|ZW2|ZW3|Exam|BW1|BW2|BW3','price': 300},
#    {'id': 3, 'name': 'AdvancedOpenWater'  , 'abbr': 'AOW', 'parts': 'Intro|ZW1|ZW2|ZW3|ZW4|ZW5|Exam|BW1|BW2|BW3|BW4','price': 500},
#    ]
    return render_template('products.html')

@app.route('/users')
def users():
    return render_template('users.html')

