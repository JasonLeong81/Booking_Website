from flask import Blueprint, request, render_template, flash, redirect, url_for, session
from web.main.forms import FeedbackForm, CourtBookingForm, MessagesForm
from web import db,mail, Message
from web.models import Feedback, Booking, Messages, User, Booking_Hair_Cut
from flask_login import login_required, logout_user, login_user, current_user
from bcrypt import *
from datetime import date, datetime, timedelta
from sqlalchemy import cast, Date

admin = Blueprint('admin',__name__) # name, import_name (for easy navigation from root)
# cannot have a function same as blueprint



@admin.route('/admin_Account',methods=['GET','POST'])
@login_required
def admin_Account():
    # Pending: create a user, CTR of every button and IP addresses of who logged in and where,


    find_user = None
    hair_cut_appointments = None
    test = f""" select * from Booking where date == '{date.today()}'; """

    # db.session.query(User).filter(User.username == 'admin').update({User.admin: 'True'})
    # db.session.commit()
    if User.query.filter_by(id=current_user.id).first().admin == 'True':
        feedbacks = Feedback.query.all()
        courts_booked = Booking.query.all()
        users = User.query.all()

    if request.method == 'POST':

        if 'Reply_customer_feedback' in request.form:
            if request.form['Reply_customer_feedback'] == 'Reply':
                id_feedback_table_to_be_updated = int(request.form['id_feedback_table_to_update'])
                session['id_feedback_table_to_be_updated'] = id_feedback_table_to_be_updated
                return redirect(url_for('admin.ReplyFeedback'))


        if 'submit_delete_user' in request.form: # deleting a user
            if request.form['submit_delete_user'] == 'Delete User':
                id_of_user_to_be_deleted = int(request.form['delete_user'])
                user_to_be_deleted = User.query.filter_by(id=id_of_user_to_be_deleted).first()
                db.session.delete(user_to_be_deleted)
                db.session.commit()
                flash('User has been deleted. This cannot be undone.')
                return redirect(url_for('admin.admin_Account'))


        if 'make_remove_admin' in request.form: ### make admin
            if request.form['make_remove_admin'] == 'Make Admin':
                if User.query.filter_by(username=request.form['new_admin'].strip()).first() != None:
                    if User.query.filter_by(username=request.form['new_admin'].strip()).first().admin == 'True':
                        flash(f'{request.form["new_admin"].strip()} is already an admin!')
                    else:
                        db.session.query(User).filter(User.username == request.form['new_admin'].strip()).update({User.admin: 'True'})
                        db.session.commit()
                        flash(f'{request.form["new_admin"].strip()} has been made admin!')
                else:
                    flash(f"User '{request.form['new_admin'].strip()}' not found. Please create an account first.")
            elif request.form['make_remove_admin'] == 'Remove Admin':
                if User.query.filter_by(username=request.form['new_admin'].strip()).first() != None:
                    if User.query.filter_by(username=request.form['new_admin'].strip()).first().admin == 'True':
                        db.session.query(User).filter(User.username == request.form['new_admin'].strip()).update({User.admin: 'False'})
                        db.session.commit()
                        flash(f'{request.form["new_admin"].strip()} has been removed as admin!')
                else:
                    flash(f"User '{request.form['new_admin'].strip()}' not found. Please create an account first.")
            return redirect(url_for('admin.admin_Account'))





        if 'find_user' in request.form:
            if request.form['find_user'] == 'Find User': # if name==value
                user = User.query.filter_by(id=int(request.form['find_user_by_id'])).first()
                if user:
                    find_user = []
                    find_user.append(user)
                else:
                    flash(f'User with id {int(request.form["find_user_by_id"])} not found.')
                    return redirect(url_for('admin.admin_Account'))

        if 'recover_password' in request.form:
            user_id = int(request.form['recover_password'])
            session['user_id_recoverPassword'] = user_id
            return redirect(url_for('admin.recover_password'))

        if 'date_court_booking_submit' in request.form:
            date_wanted = request.form['date_court_booking']
            test = f""" select * from Booking where date == '{date_wanted}'; """

        if 'Show_Hair_Cut_Appointments' in request.form:
            if request.form['Show_Hair_Cut_Appointments'] == 'Show':
                # a = request.form['Date_For_Hair_Cut_Appointments']
                # print(type(a),a)
                if len(Booking_Hair_Cut.query.all()) > 0:
                    day_wanted_show_appointment_hair_cut = request.form['Date_For_Hair_Cut_Appointments']
                    today = datetime(int(day_wanted_show_appointment_hair_cut[0:4]),int(day_wanted_show_appointment_hair_cut[5:7]),int(day_wanted_show_appointment_hair_cut[8:]),0,0,0)
                    tomorrow = today + timedelta(hours=24)
                    # print(today,tomorrow)
                    hair_cut_appointments = Booking_Hair_Cut.query.filter(Booking_Hair_Cut.Date >= today,Booking_Hair_Cut.Date < tomorrow).all()
                    # print(hair_cut_appointments)
                else:
                    flash('No rows in Booking Hair Cut database.')


    # test = f""" select date from Booking; """
    test = db.session.execute(test)
    return render_template('admin.html',title='AdminPage',users=users,courts_booked=courts_booked,feedbacks=feedbacks,find_user=find_user,test=test,today=date.today(),hair_cut_appointments=hair_cut_appointments)

@admin.route('/recover_password',methods=['GET','POST'])
@login_required
def recover_password():
    db.session.query(User).filter(User.id == session['user_id_recoverPassword']).update({User.password:hashpw(bytes('123',encoding='utf-8'),gensalt())}) # change password to '123'
    db.session.commit()
    flash(f"Customer {User.query.filter_by(id=session['user_id_recoverPassword']).first().username}'s password has been changed to 123. Please notify customer.")
    session.pop('user_id_recoverPassword',None)
    return redirect(url_for('admin.admin_Account'))


@admin.route('/reply_feedback',methods=['GET','POST'])
@login_required
def ReplyFeedback():
    customer_feedback = Feedback.query.filter_by(id=int(session['id_feedback_table_to_be_updated'])).first().feedback
    if request.method == 'POST':
        if 'Submit_Admin_Feedback' in request.form:
            if request.form['Submit_Admin_Feedback'] == 'Reply':
                db.session.query(Feedback).filter(Feedback.id==int(session['id_feedback_table_to_be_updated'])).update({Feedback.response_feedback: str(request.form['Admin_Feedback'].strip()),Feedback.Feedback_Status:1})
                db.session.commit()
                flash(f"""A Feedback response to user "{Feedback.query.filter_by(id=int(session['id_feedback_table_to_be_updated'])).first().owner.username}" has been sent.""")
                session.pop('id_feedback_table_to_be_updated',None)
                return redirect(url_for('admin.admin_Account'))
    return render_template('replyfeedback.html',title='Reply_Feedback',customer_feedback=customer_feedback)

