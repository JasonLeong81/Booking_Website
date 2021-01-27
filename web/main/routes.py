from flask import Blueprint, request, render_template, flash, redirect, url_for
from web.main.forms import FeedbackForm, CourtBookingForm
from web import db
from web.models import Feedback, Booking
from flask_login import login_required, current_user
from datetime import datetime, timedelta

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
    # hourly, even if you booked 1:59-2:00, you still pay for 1 hour (count at least one hour)
    form = CourtBookingForm()
    if request.method == 'POST':
        # print('y' * 50)
        if form.validate_on_submit():

            raw_date = request.form['date']
            cleaned_date = datetime(int(raw_date[0:4]),int(raw_date[5:7]),int(raw_date[8:]),0,0)
            raw_start_time = request.form['start_time']
            raw_end_time = request.form['end_time']
            cleaned_start_time =  datetime( int(raw_date[0:4]),int(raw_date[5:7]),int(raw_date[8:]),int(raw_start_time[0:2]),int(raw_start_time[3:]) )
            cleaned_end_time = datetime( int(raw_date[0:4]),int(raw_date[5:7]),int(raw_date[8:]),int(raw_end_time[0:2]),int(raw_end_time[3:]) )

            available = []
            booked = []
            booked_from_db = Booking.query.filter_by(court=form.court.data)

            for i in booked_from_db:
                if i.start_time.day == cleaned_date.day:
                    booked.append([i.start_time,i.end_time])
            booked = sorted(booked)

            for i in range(len(booked)-1):
                if booked[i][-1] < booked[i+1][0]:
                    available.append([booked[i][1],booked[i+1][0]])
            else:
                for i in range(24):
                    if available: # exclude next day
                        if int(cleaned_date.day) != int(available[0][0].day):
                            break
                    if booked:
                        if -int(cleaned_date.hour) + int(booked[0][0].hour) == 1: # hourly
                            available.append([cleaned_date, cleaned_date + timedelta(hours=1)]) # able to book for back to back
                            cleaned_date = booked[-1][1]
                            continue
                    available.append([cleaned_date, cleaned_date + timedelta(hours=1)])
                    cleaned_date += timedelta(hours=1)

            for i in available:
                temp = (int(i[0].hour),int(i[1].hour))
                temp1 = (int(cleaned_start_time.hour),int(cleaned_end_time.hour))
                if temp1 == temp:
                    booking = Booking(start_time=cleaned_start_time,end_time=cleaned_end_time, court=form.court.data,owner=current_user)
                    db.session.add(booking)
                    db.session.commit()
                    flash('Your court has been booked.')
                    return redirect(url_for('user.account'))
            else:
                flash('This court is not available.')
    return render_template('booking.html',title='Booking',form=form)

@main.route('/delete',methods=['POST','GET'])
@login_required
def delete_court_booking():
    booking_to_be_deleted = Booking.query.filter_by(id=request.form['id']).first()
    db.session.delete(booking_to_be_deleted)
    db.session.commit()
    flash('Your court reservation has been deleted.')
    return redirect(url_for('user.account'))
