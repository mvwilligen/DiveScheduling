############################################################################################
##                                                                                        ##
##  ███████╗ ██████╗ ██████╗ ███╗   ███╗███████╗   ██████╗ ██╗   ██╗                      ##
##  ██╔════╝██╔═══██╗██╔══██╗████╗ ████║██╔════╝   ██╔══██╗╚██╗ ██╔╝                      ##
##  █████╗  ██║   ██║██████╔╝██╔████╔██║███████╗   ██████╔╝ ╚████╔╝                       ##
##  ██╔══╝  ██║   ██║██╔══██╗██║╚██╔╝██║╚════██║   ██╔═══╝   ╚██╔╝                        ##
##  ██║     ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████║██╗██║        ██║                         ##
##  ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝╚═╝        ╚═╝                         ##
##                                                                                        ## 
############################################################################################ 
                                                               
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from Package.models import Users, Products

#https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class AppointmentsEditForm(FlaskForm):

    firstname    = StringField(label   = 'firstname')
    lastname     = StringField(label   = 'lastname')
    phone        = StringField(label   = 'phone')
    emailaddress = StringField(label   = 'emailaddress') # , validators = [Email()])
    password     = PasswordField(label = 'password')    # , validators = [Length(min = 8)])
    note         = TextAreaField('note')
    date        = StringField(label   = 'date')
    time        = StringField(label   = 'time')
    
    save         = SubmitField(label   = 'save')
    cancel       = SubmitField(label   = 'cancel')

class AppointmentsEventsForm(FlaskForm):

    firstname    = StringField(label   = 'firstname')
    lastname     = StringField(label   = 'lastname')
    name         = StringField(label   = 'name')
    phone        = StringField(label   = 'phone')
    emailaddress = StringField(label   = 'emailaddress') # , validators = [Email()])
    password     = PasswordField(label = 'password')    # , validators = [Length(min = 8)])
    
    save         = SubmitField(label   = 'save')
    cancel       = SubmitField(label   = 'cancel')

class AppointmentsDateForm2(FlaskForm):

    firstname    = StringField(label   = 'firstname')
    lastname     = StringField(label   = 'lastname')
    phone        = StringField(label   = 'phone')
    emailaddress = StringField(label   = 'emailaddress') # , validators = [Email()])
    password     = PasswordField(label = 'password')     # , validators = [Length(min = 8)])
    
    save         = SubmitField(label   = 'save')
    cancel       = SubmitField(label   = 'cancel')

class LoginForm(FlaskForm):
    username     = StringField('username',   validators=[DataRequired()])
    password     = PasswordField('password', validators=[DataRequired()])
    remember_me  = BooleanField('remember Me')
    submit       = SubmitField('login')
    cancel       = SubmitField(label   = 'cancel')

class ProductsEditForm(FlaskForm):

    abbr         = StringField(label   = 'abbr')  # , validators=[DataRequired()])
    parts        = StringField(label   = 'parts') # , validators=[DataRequired()])
    description  = StringField(label   = 'description')
    note         = TextAreaField('note')
    save         = SubmitField(label   = 'save')
    cancel       = SubmitField(label   = 'cancel')

class ProductsNewForm(FlaskForm):

    productname  = StringField(label   = 'productname', validators=[DataRequired()])
    parts        = StringField(label   = 'parts', validators=[DataRequired()])
    abbr         = StringField(label   = 'abbr', validators=[DataRequired()])
    description  = StringField(label   = 'description')
    note         = TextAreaField('note')
    save         = SubmitField(label   = 'save')
    cancel       = SubmitField(label   = 'cancel')

class ProductsUsersForm(FlaskForm):

    productname  = StringField(label   = 'productname')
    parts        = StringField(label   = 'parts')
    abbr         = StringField(label   = 'abbr')
    description  = StringField(label   = 'description')
    save         = SubmitField(label   = 'save')
    cancel       = SubmitField(label   = 'cancel')

class UsersEditForm(FlaskForm):

    firstname    = StringField(label   = 'firstname')
    lastname     = StringField(label   = 'lastname')
    phone        = StringField(label   = 'phone')
    emailaddress = StringField(label   = 'emailaddress') # , validators = [Email()])
    password     = PasswordField(label = 'password')    # , validators = [Length(min = 8)])
    save         = SubmitField(label   = 'save')
    cancel       = SubmitField(label   = 'cancel')

class UsersInfoForm(FlaskForm):

    firstname    = StringField(label   = 'firstname')
    save         = SubmitField(label   = 'save')
    cancel       = SubmitField(label   = 'cancel')

class UsersRegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = Users.query.filter_by(Username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists, please assign a different username')

    username     = StringField(label   = 'username', validators = [Length(min = 2, max = 30), DataRequired()])
    firstname    = StringField(label   = 'firstname', validators = [DataRequired()])
    lastname     = StringField(label   = 'lastname', validators = [DataRequired()])
    phone        = StringField(label   = 'phone')
    emailaddress = StringField(label   = 'emailaddress', validators = [Email()])
    password1    = PasswordField(label = 'password1', validators = [Length(min = 8)])
    password2    = PasswordField(label = 'password2', validators = [EqualTo('password1')])

    submit       = SubmitField(label   = 'create user')
    cancel       = SubmitField(label   = 'cancel')

class UsersEditForm2(FlaskForm):

    firstname    = StringField(label   = 'firstname')
    lastname     = StringField(label   = 'lastname')
    phone        = StringField(label   = 'phone')
    password     = StringField(label   = 'password')
    note         = TextAreaField('note')
    emailaddress = StringField(label   = 'emailaddress') # , validators = [Email()])
    # 20240826 - MvW
    status       = SelectMultipleField('status', choices=[('new', 'new'), ('student', 'student'), ('staff', 'staff'), ('assistant', 'assistant'), ('instructor', 'instructor'), ('admin', 'administrator')])

    save         = SubmitField(label   = 'save')
    cancel       = SubmitField(label   = 'cancel')

class UsersProductForm2(FlaskForm):

    firstname    = StringField(label   = 'firstname')
    lastname     = StringField(label   = 'lastname')
    phone        = StringField(label   = 'phone')
    emailaddress = StringField(label   = 'emailaddress') # , validators = [Email()])
    password     = PasswordField(label = 'password')     # , validators = [Length(min = 8)])
    
    save         = SubmitField(label   = 'save')
    cancel       = SubmitField(label   = 'cancel')
