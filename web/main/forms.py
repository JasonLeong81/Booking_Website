from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, IntegerField
from wtforms.validators import DataRequired

class FeedbackForm(FlaskForm):
    feedback = StringField('Feedback',validators=[DataRequired()])
    submit = SubmitField('Submit')

class CourtBookingForm(FlaskForm):
    court = IntegerField('Court Number',validators=[DataRequired()])
    submit = SubmitField('Submit')

