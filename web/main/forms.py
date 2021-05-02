from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, IntegerField
from wtforms.validators import DataRequired

class FeedbackForm(FlaskForm):
    feedback = StringField('Feedback',validators=[DataRequired()])
    submit = SubmitField('Submit')

class CourtBookingForm(FlaskForm):
    court = IntegerField('Court Number',validators=[DataRequired()])
    submit = SubmitField('Submit')

class MessagesForm(FlaskForm):
    messages = StringField('Messages')
    submit = SubmitField('Send')

class AddFriendForm(FlaskForm): # this is only a button on a person's profile for others to add him/her
    Friend_username = StringField("Friend's username", validators=[DataRequired()],default='')
    submit = SubmitField('Add Friend')