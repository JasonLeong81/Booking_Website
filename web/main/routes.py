from flask import Blueprint, request, render_template, flash, redirect, url_for
from web.main.forms import FeedbackForm, CourtBookingForm, MessagesForm, AddFriendForm
from web import db,mail, Message
from web.models import Feedback, Booking, Messages, User, Friends
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
        feedback = Feedback(feedback=form.feedback.data,owner=current_user,Feedback_Status=0)
        db.session.add(feedback)
        db.session.commit()
        flash('You feedback has been received in good order. Thank you for your time and feedback.')
        return redirect(url_for('user.account'))
        # return redirect(url_for('main.home')) # doesnt matter

    form1 = MessagesForm()
    if form1.validate_on_submit():
        if form1.messages.data:
            new_message = Messages(messages=form1.messages.data,dates=datetime.utcnow(),owner=current_user)
            db.session.add(new_message)
            db.session.commit()
            form1.messages.data = ''
            return redirect(url_for('main.home')) # redirect to start fresh
    m = Messages.query.all()

    form2 = AddFriendForm() ### friend's system
    if request.method == 'POST':
        if form2.validate_on_submit():

            ### checking critirea to add a friend ###
            Friend_to_add = str(form2.Friend_username.data.strip())
            if Friend_to_add == User.query.filter_by(id=current_user.id).first().username: # cannot add yourself
                flash('Cannot add yourself.')
            else:
                try:
                    if User.query.filter_by(username=Friend_to_add).first() == None: # this user does not exist in our database
                        flash(f'This user "{Friend_to_add}" does not exist in our database.')
                        raise ValueError  # just for fun
                    else:
                        sent_friend_request_AlreadyAccepted = Friends.query.filter_by(From_id=current_user.id, Status=1,
                                                                                      To_id=User.query.filter_by(
                                                                                          username=Friend_to_add).first().id).first()  # check if they are already friends
                        if sent_friend_request_AlreadyAccepted == None:  # not friends
                            print('Not friends yet.', 111111111111111111111111111)
                            pass
                        elif len(
                                sent_friend_request_AlreadyAccepted.From.username) > 0:  # this means we are already friends
                            flash(f'You and {Friend_to_add} are already friends.')
                            raise ValueError  # so that "else" would not be run, we can actually raise any error here we like
                        sent_friend_request_temp = Friends.query.filter_by(From_id=current_user.id,Status=0,To_id=User.query.filter_by(username=Friend_to_add).first().id).first() # see if current_user has any pending friend request sent
                        if sent_friend_request_temp == None: # we have not sent one before
                            print('No pending friend request.',1111111111111111111111)
                            pass
                        else:
                            sent_friend_request = Friends.query.filter_by(From_id=current_user.id,Status=0,To_id=User.query.filter_by(username=Friend_to_add).first().id).first().From.username # request sent from me and status is pending and the request is to "who"
                            if sent_friend_request or len(sent_friend_request)>0:  ### have you had a "sent friend request" that is still pending and not rejected (optional: within the time frame of 1 month)
                                flash(f'You have already sent a friend request to {Friend_to_add}.')
                                raise ValueError # so that "else" would not be run, we can actually raise any error here we like
                except Exception as msg:
                    print(msg)
                    for i in range(10):
                        print()
                else:
                    # print(sent_friend_request)
                    To = User.query.filter_by(username=Friend_to_add).first()
                    add_friend = Friends(Date=datetime.today(), From=current_user, To=To, Status=0, Friend_of_id=0,Priviledged=0) # adding a friend # sending a request
                    db.session.add(add_friend)
                    db.session.commit()
                    flash(f'A friend request has been sent to {Friend_to_add}.')
            return redirect(url_for('main.home'))

    ### show all my friends ###
    try:
        myFriends = Friends.query.filter_by(From_id=current_user.id,Status=1) # all friends that accepted my request and the request is from me
    except:
        myFriends = []

    return render_template('home.html',title='Home',form=form,MESSAGES=m,form1=form1,number_of_users=len(number_of_users),list_of_online_people=list_of_online_people,friends=myFriends,form2=form2)

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
        if form.validate_on_submit():
            # print(request.form['date'],f'User {current_user.username} booked a court')
            raw_date = request.form['date'].strip()
            # print('raw_date: ',raw_date,type(raw_date)) # 2021-04-27 # str
            cleaned_date = datetime(int(raw_date[0:4]),int(raw_date[5:7]),int(raw_date[8:]),0,0)
            # print('cleaned_date: ',cleaned_date,type(cleaned_date)) # 2021-04-27 00:00:00 # datetime.datetime
            raw_start_time = request.form['start_time']
            # print('raw_start_time: ',raw_start_time,type(raw_start_time)) # 16:50 # str
            raw_end_time = request.form['end_time']
            # print('raw_end_time: ',raw_end_time,type(raw_end_time)) # 17:50 # str
            cleaned_start_time =  datetime( int(raw_date[0:4]),int(raw_date[5:7]),int(raw_date[8:]),int(raw_start_time[0:2]),int(raw_start_time[3:]) )
            # print('cleaned_start_time: ',cleaned_start_time,type(cleaned_start_time)) # 2021-04-27 16:50:00 # datetime.datetime
            cleaned_end_time = datetime( int(raw_date[0:4]),int(raw_date[5:7]),int(raw_date[8:]),int(raw_end_time[0:2]),int(raw_end_time[3:]) )
            # print('cleaned_end_time: ',cleaned_end_time,type(cleaned_end_time)) # 2021-04-27 17:50:00 # datetime.datetime
            # for i in range(10):
            #     print()
            available = []
            booked = []
            booked_from_db = Booking.query.filter_by(court=form.court.data) # selecting courts (from database) that have the same number as the court number entered in form by user

            for i in booked_from_db:
                if i.start_time.date() == cleaned_date.date(): # selecting courts (from database) that have the same booking date as the date entered in form by user based on starting time. Not based on ending time because those courts have been used.
                    booked.append([i.start_time,i.end_time]) # booked = [start_time,end_time], where both "start_time" and "end_time" are <class 'datetime.datetime'>
            booked = sorted(booked)

            for i in range(len(booked)-1):
                if booked[i][-1] < booked[i+1][0]: # if end time of first < start time of second, then append [end time of first,start time of second] to available
                    available.append([booked[i][1],booked[i+1][0]])
            else:
                for i in range(24):
                    if len(available) > 0:
                        if int(cleaned_date.day) != int(available[0][0].day): # exclude next day # cleaned date starts from 12 (12am)
                            break
                    if len(booked) > 0:
                        if -int(cleaned_date.hour) + int(booked[0][0].hour) == 1: # if at the start of the -day's hour (12 am or 12 in this case) + the earliest start_time of booked == 1, this means that there is exactly one hour in between that people can play
                            # print(-int(cleaned_date.hour),int(booked[0][0].hour),'111111111111111111111')
                            available.append([cleaned_date, cleaned_date + timedelta(hours=1)])
                            if booked[-1][1].minute > 0: # making sure that you book the hour (or not) # if the last booking's end_time's minute is more than 0, then we make the next available booking starting from the next hour
                                cleaned_date = booked[-1][1]
                                cleaned_date = cleaned_date.replace(hour=booked[-1][1].hour+1,minute=0) # cleaned_date becomes the next hour
                            else:
                                cleaned_date = booked[-1][1] # otherwise cleaned date becomes the last booking's end time exactly
                            continue
                    available.append([cleaned_date, cleaned_date + timedelta(hours=1)])
                    cleaned_date += timedelta(hours=1)


            number_of_hours = cleaned_end_time.hour - cleaned_start_time.hour
            number_of_hours_counter = 0
            cleaned_start_time_temp = cleaned_start_time
            available_temp = [(start.hour,end.hour) for start,end in available] # available_temp = [start time's hour, end time's hour]
            for _ in range(number_of_hours): # lets say if I have two hours
                temp1 = (int(cleaned_start_time_temp.hour),int(cleaned_start_time_temp.hour+1)) # temp1 = (1,2) if i book from 1 to 3
                cleaned_start_time_temp = cleaned_start_time_temp + timedelta(hours=1) # increment cleaned_start_time_temp so that the next round temp1 will be (2,3)
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
                flash('This court is not available.') # one of the hours might have been taken
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