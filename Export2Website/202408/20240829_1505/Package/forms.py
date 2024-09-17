from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from Package.models import Users, Products

class AppointmentsEditForm(FlaskForm):

    firstname    = StringField(label   = 'firstname')
    lastname     = StringField(label   = 'lastname')
    phone        = StringField(label   = 'phone')
    emailaddress = StringField(label   = 'emailaddress') # , validators = [Email()])
    password     = PasswordField(label = 'password')    # , validators = [Length(min = 8)])
    
    submit       = SubmitField(label   = 'save')

class LoginForm(FlaskForm):

    username     = StringField(label   = "username", validators={DataRequired()})
    password     = PasswordField(label = "password", validators={DataRequired()})

    submit       = SubmitField(label   = 'login')

class ProductsEditForm(FlaskForm):

    productname  = StringField(label   = 'productname')
    parts        = StringField(label   = 'parts')
    abbr         = StringField(label   = 'abbr')
    description  = StringField(label   = 'description')

    submit       = SubmitField(label   = 'save')

class ProductsNewForm(FlaskForm):

    productname  = StringField(label   = 'productname')
    parts        = StringField(label   = 'parts')
    abbr         = StringField(label   = 'abbr')
    description  = StringField(label   = 'description')

    submit       = SubmitField(label   = 'save')

class ProductsUsersForm(FlaskForm):

    productname  = StringField(label   = 'productname')
    parts        = StringField(label   = 'parts')
    abbr         = StringField(label   = 'abbr')
    description  = StringField(label   = 'description')

    submit       = SubmitField(label   = 'save')

class UsersEditForm(FlaskForm):

    firstname    = StringField(label   = 'firstname')
    lastname     = StringField(label   = 'lastname')
    phone        = StringField(label   = 'phone')
    emailaddress = StringField(label   = 'emailaddress') # , validators = [Email()])
    password     = PasswordField(label = 'password')    # , validators = [Length(min = 8)])
    
    submit       = SubmitField(label   = 'save')

class UsersInfoForm(FlaskForm):

    firstname    = StringField(label   = 'firstname')
    submit       = SubmitField(label   = 'save')

#usersnew
class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = Users.query.filter_by(Username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists, please assign a different username')

    username     = StringField(label   = 'username', validators = [Length(min = 2, max = 30), DataRequired()])
    firstname    = StringField(label   = 'firstname')
    lastname     = StringField(label   = 'lastname')
    phone        = StringField(label   = 'phone')
    emailaddress = StringField(label   = 'emailaddress') # , validators = [Email()])
    password1    = PasswordField(label = 'password1')    # , validators = [Length(min = 8)])
    password2    = PasswordField(label = 'password2')    # , validators = [EqualTo('password1')])

    submit       = SubmitField(label   = 'create user')

#usersedit
class RegisterForm2(FlaskForm):

    firstname    = StringField(label   = 'firstname')
    lastname     = StringField(label   = 'lastname')
    phone        = StringField(label   = 'phone')
    password     = StringField(label   = 'password')
    emailaddress = StringField(label   = 'emailaddress') # , validators = [Email()])
    # 20240826 - MvW
    status       = SelectMultipleField('status', choices=[('new', 'new'), ('student', 'student'), ('staff', 'staff'), ('instructor', 'instructor'), ('admin', 'administrator')])

    submit       = SubmitField(label   = 'save user')

