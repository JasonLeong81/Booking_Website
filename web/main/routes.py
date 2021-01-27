from flask import Blueprint, request, render_template, flash, redirect, url_for
from web.main.forms import FeedbackForm, CourtBookingForm
from web import db
from web.models import Feedback, Booking
from flask_login import login_required, current_user
from datetime import datetime

main = Blueprint('main',__name__)

@main.route('/',methods=['POST','GET'])
def home():
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(feedback=form.feedback.data,owner=current_user)
        db.session.add(feedback)
        db.session.commit()
        flash('You feedback has been received in good order. Thank you for your time and feedback.')
        return redirect(url_for('user.account'))
    return render_template('home.html',title='Home',form=form)

@main.route('/about')
def about():
    return render_template('about.html',title='About')

@main.route('/join_us')
def join_us():
    return render_template('join_us.html',title='Join Us')

@main.route('/faq')
def faq():
    return render_template('faq.html',title='FAQs')

@main.route('/contact')
def contact():
    return render_template('contact.html',title='Contact')

@main.route('/training')
def training():
    return render_template('training.html',title='Training')

@main.route('/competition')
def competition():
    return render_template('competition.html',title='Competition')

@main.route('/booking',methods=['POST','GET'])
@login_required
def booking():
    form = CourtBookingForm()
    if request.method == 'POST':
        # print('y' * 50)
        if form.validate_on_submit():
            date = request.form['date']
            time = request.form['time']
            court = Booking.query.filter_by(time=datetime( int(date[0:4]),int(date[5:7]),int(date[8:]),int(time[0:2]),int(time[3:]) ), court=form.court.data).first() # prevent two groups booking the same court
            if not court:
                booking = Booking(time=datetime( int(date[0:4]),int(date[5:7]),int(date[8:]),int(time[0:2]),int(time[3:]) ),court=form.court.data,owner=current_user)
                db.session.add(booking)
                db.session.commit()
                flash('Your court has been booked.')
                return redirect(url_for('user.account'))
            else:
                flash('This court is not available.')
    return render_template('booking.html',title='Booking',form=form)


