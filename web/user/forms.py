from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from web.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[Length(min=2, max=20)],default='username')
    email = StringField('Email', validators=[Email()],default='xxx@gmail.com')
    password = PasswordField('Password', validators=[])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Log In')

class UpdateEmailForm(FlaskForm):
    current_email = StringField('Current email', validators=[Email()],default='')
    new_email = StringField('New email', validators=[Email()],default='')
    submit = SubmitField('Confirm')

class UpdatePasswordForm(FlaskForm):
    current_password = StringField('Current password', validators=[DataRequired()],default='')
    new_password = StringField('New password', validators=[DataRequired()],default='')
    submit = SubmitField('Confirm')

class UpdateUsernameForm(FlaskForm):
    current_username = StringField('Current username', validators=[DataRequired()],default='')
    new_username = StringField('New username', validators=[DataRequired()],default='')
    submit = SubmitField('Confirm')

class ShoppingListForm(FlaskForm):
    Item = StringField('Item name', validators=[DataRequired()],default='')
    # Date = # get from javascript
    Description = StringField('Item description',default='')
    submit = SubmitField('Add')

class MakePriviledged(FlaskForm):
    Good_Friend_username = StringField("Friend's username", validators=[DataRequired()], default='')
    submit_grant = SubmitField('Grant Priviledge.')
    submit_remove = SubmitField('Remove Priviledge.')


