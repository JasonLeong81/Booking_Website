from flask import Blueprint, request, render_template, flash, redirect, url_for
from web.main.forms import FeedbackForm, CourtBookingForm, MessagesForm
from web import db,mail, Message
from web.models import Feedback, Booking, Messages, User
from flask_login import login_required, current_user
from datetime import datetime, timedelta, date

main = Blueprint('main',__name__)


# msg = Message('Hello', sender='leongjason822@gmail.com', recipients=['leongjason3781@gmail.com']) ### needed to see ip and location of users
# msg.body = 'Hi, someone just locked into your favourite account. Was this you?'
# mail.send(msg)



@main.route('/',methods=['POST','GET'])
def home():
    number_of_users = User.query.all()

    list_of_online_people = []
    try:
        for i in number_of_users:
            if len(list_of_online_people) > 10:
                break
            if i.logged_in == 'True' and i.id != current_user.id:
                list_of_online_people.append(f'{i.username} is online!')
    except:
        pass


    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(feedback=form.feedback.data,owner=current_user)
        db.session.add(feedback)
        db.session.commit()
        flash('You feedback has been received in good order. Thank you for your time and feedback.')
        return redirect(url_for('user.account'))

    form1 = MessagesForm()
    if form1.validate_on_submit():
        if form1.messages.data:
            new_message = Messages(messages=form1.messages.data,dates=datetime.utcnow(),owner=current_user)
            db.session.add(new_message)
            db.session.commit()
            form1.messages.data = ''
            return redirect(url_for('main.home')) # redirect to start fresh
    m = Messages.query.all()
    return render_template('home.html',title='Home',form=form,MESSAGES=m,form1=form1,number_of_users=len(number_of_users),list_of_online_people=list_of_online_people)

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
            print(request.form['date'],f'User {current_user.username} booked a court')
            raw_date = request.form['date'].strip()
            cleaned_date = datetime(int(raw_date[0:4]),int(raw_date[5:7]),int(raw_date[8:]),0,0)
            raw_start_time = request.form['start_time']
            raw_end_time = request.form['end_time']
            cleaned_start_time =  datetime( int(raw_date[0:4]),int(raw_date[5:7]),int(raw_date[8:]),int(raw_start_time[0:2]),int(raw_start_time[3:]) )
            cleaned_end_time = datetime( int(raw_date[0:4]),int(raw_date[5:7]),int(raw_date[8:]),int(raw_end_time[0:2]),int(raw_end_time[3:]) )

            available = []
            booked = []
            booked_from_db = Booking.query.filter_by(court=form.court.data)

            for i in booked_from_db:
                if i.start_time.day == cleaned_date.day: # getting those courts that are booked on a particular day
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
                            if booked[-1][1].minute > 0: # making sure that you book the hour
                                cleaned_date = booked[-1][1]
                                cleaned_date = cleaned_date.replace(hour=booked[-1][1].hour+1,minute=0)
                            else:
                                cleaned_date = booked[-1][1]
                            # print('SECOND HALF',cleaned_date)
                            continue
                    available.append([cleaned_date, cleaned_date + timedelta(hours=1)])
                    cleaned_date += timedelta(hours=1)
            number_of_hours = cleaned_end_time.hour - cleaned_start_time.hour
            number_of_hours_counter = 0
            cleaned_start_time_temp = cleaned_start_time
            available_temp = [(start.hour,end.hour) for start,end in available]
            # print(number_of_hours)
            for _ in range(number_of_hours):
                temp1 = (int(cleaned_start_time_temp.hour),int(cleaned_start_time_temp.hour+1))
                cleaned_start_time_temp = cleaned_start_time_temp + timedelta(hours=1)
                # print(available)
                # print(temp1)
                if temp1 in available_temp:
                    number_of_hours_counter += 1
                    if number_of_hours_counter == int(number_of_hours):
                        booking = Booking(start_time=cleaned_start_time,end_time=cleaned_end_time, court=form.court.data,owner=current_user,date=date(int(raw_date[0:4]),int(raw_date[5:7]),int(raw_date[8:])))
                        db.session.add(booking)
                        db.session.commit()
                        # print(raw_start_time)
                        flash('Your court has been booked.')
                        return redirect(url_for('user.account'))
                    else:
                        continue
            else:
                flash('This court is not available.')
    return render_template('booking.html',title='Booking',form=form,date_today=date.today())

@main.route('/delete_court',methods=['POST','GET'])
@login_required
def delete_court_booking():
    booking_to_be_deleted = Booking.query.filter_by(id=request.form['id_court']).first()
    db.session.delete(booking_to_be_deleted)
    db.session.commit()
    flash('Your court reservation has been deleted.')
    return redirect(url_for('user.account'))

@main.route('/delete_feedback',methods=['POST','GET'])
@login_required
def delete_Feedback():
    feedback_to_be_deleted = Feedback.query.filter_by(id=request.form['id_feedback']).first()
    db.session.delete(feedback_to_be_deleted)
    db.session.commit()
    flash('Your feedback has been deleted.')
    return redirect(url_for('user.account'))