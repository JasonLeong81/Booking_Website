from flask import Blueprint, request, render_template, flash, redirect, url_for, session
from web.main.forms import FeedbackForm, CourtBookingForm, MessagesForm
from web import db,mail, Message
from web.models import Feedback, Booking, Messages, User
from flask_login import login_required, logout_user, login_user, current_user
from bcrypt import *
from datetime import date, datetime

admin = Blueprint('admin',__name__) # name, import_name (for easy navigation from root)
# cannot have a function same as blueprint



@admin.route('/admin_Account',methods=['GET','POST'])
@login_required
def admin_Account():
    find_user = None

    # db.session.query(User).filter(User.username == 'admin').update({User.admin: 'True'})
    # db.session.commit()
    if User.query.filter_by(id=current_user.id).first().admin == 'True':
        feedbacks = Feedback.query.all()
        courts_booked = Booking.query.all()
        users = User.query.all()

    if request.method == 'POST':

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
            if request.form['find_user'] == 'Find User':
                user = User.query.filter_by(id=int(request.form['find_user_by_id'])).first()
                if user:
                    find_user = []
                    find_user.append(user)
                else:
                    flash(f'User with id {int(request.form["find_user_by_id"])} not found.')
                    return render_template('admin.html', title='AdminPage', users=users, courts_booked=courts_booked,feedbacks=feedbacks)

        if 'recover_password' in request.form:
            user_id = int(request.form['recover_password'])
            session['user_id_recoverPassword'] = user_id
            return redirect(url_for('admin.recover_password'))

    # test = f""" select date from Booking; """
    test = f""" select * from Booking where date == '{date.today()}'; """
    test = db.session.execute(test)
    return render_template('admin.html',title='AdminPage',users=users,courts_booked=courts_booked,feedbacks=feedbacks,find_user=find_user,test=test)

@admin.route('/recover_password',methods=['GET','POST'])
@login_required
def recover_password():
    db.session.query(User).filter(User.id == session['user_id_recoverPassword']).update({User.password:hashpw(bytes('123',encoding='utf-8'),gensalt())}) # change password to '123'
    db.session.commit()
    flash(f"Customer {User.query.filter_by(id=session['user_id_recoverPassword']).first().username}'s password has been changed to 123. Please notify customer.")
    session.pop('user_id_recoverPassword',None)
    return redirect(url_for('admin.admin_Account'))
