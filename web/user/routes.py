from flask import Blueprint, render_template, flash, redirect, url_for
from web.user.forms import RegistrationForm, LoginForm, UpdateEmailForm
from web.models import User, Feedback, Booking
from flask_login import login_required, logout_user, login_user, current_user
from bcrypt import *
from web import mail, Message, db
user = Blueprint('user',__name__)


@user.route('/account',methods=['GET','POST'])
@login_required
def account():
    # db.session.query(User).filter(User.username == 'Jason').update({User.username: 'Jasoni'}) # updating rows in database


    courts_booked = Booking.query.filter_by(user_id=current_user.id)
    feedbacks_provided = Feedback.query.filter_by(user_id=current_user.id)
    if current_user.is_authenticated:
        resp = {"result": 200,
                "data": current_user}
    else:
        resp = {"result": 401,
                "data": {"message": "user no login"}}
    form = UpdateEmailForm()
    if form.validate_on_submit():
        new_email = form.new_email.data.strip()
        current_email = form.current_email.data.strip()
        if current_user.email != current_email:
            flash('Current email is not entered correctly.')
        else:
            if User.query.filter_by(email=new_email).first() or current_email == new_email:
                flash('This email has been taken. Please try a different one.')
            else:
                db.session.query(User).filter(User.email == current_email).update({User.email: new_email})
                db.session.commit()
                flash('Your email has been updated.')
    return render_template('account.html',title='Account',r=resp,courts_booked=courts_booked,feedbacks_provided=feedbacks_provided,form=form)

@user.route('/login',methods=['GET','POST'])
def login():
    ### aaa@gmail.com
    ### 123
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        p = user.password
        # if user and form.password.data == p:
        if user and checkpw(bytes(form.password.data,encoding='utf-8'),p):
            login_user(user)
            msg = Message('Hello', sender='leongjason822@gmail.com', recipients=['leongjason3781@gmail.com'])
            msg.body = 'Hi, someone just locked into your favourite account. Was this you?'
            mail.send(msg)
            flash('You have been logged in.')
            return redirect(url_for('user.account'))
        else:
            flash('Login unsuccessful. Please check email and password.')
    return render_template('login.html',title='Login',form=form)

@user.route('/register',methods=['POST','GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # from Flaskform
        hashed = hashpw(bytes(form.password.data,encoding='utf-8'),gensalt())
        user = User(username=form.username.data,email=form.email.data,password=hashed)
        db.session.add(user)
        db.session.commit()
        flash("You're account has been created. ")
        return redirect(url_for('user.login'))
    return render_template('register.html',title='Register',form=form)

@user.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('about.html',title='About')



















