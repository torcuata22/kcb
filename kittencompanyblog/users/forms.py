from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileAllowed, FileField #allows to update png file for profil pics

from flask_login import current_user
from kittencompanyblog.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()]) #we don't save the string, just the hash
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    username = StringField('UserName', validators = [DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(), EqualTo('pass_confirm', message = "Passwords must match!")])
    pass_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Your email is already registered')
        
    def user_name(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Your user name is already registered')
        
class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    username = StringField('UserName', validators = [DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def check_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Your email is already registered')
        
    def user_name(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Your user name is already registered')
        
    

