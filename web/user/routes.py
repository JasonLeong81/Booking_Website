from flask import Blueprint, render_template, flash, redirect, url_for
from web.user.forms import RegistrationForm, LoginForm, UpdateEmailForm, UpdatePasswordForm, UpdateUsernameForm
from web.models import User, Feedback, Booking
from flask_login import login_required, logout_user, login_user, current_user
from bcrypt import *
from web import mail, Message, db
user = Blueprint('user',__name__)


@user.route('/account',methods=['GET','POST'])
@login_required
def account():
    # db.session.query(User).filter(User.username == 'Jason').update({User.username: 'Jasoni'}) # updating rows in database
    # hashed = hashpw(bytes(form.password.data, encoding='utf-8'), gensalt())
    # if user and checkpw(bytes(form.password.data, encoding='utf-8'), p):

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
    form.current_email.data = ''
    form.new_email.data = ''

    form1 = UpdatePasswordForm()
    if form1.validate_on_submit():
        new_password = form1.new_password.data.strip()
        current_password = form1.current_password.data.strip()
        if not checkpw(bytes(current_password, encoding='utf-8'), current_user.password):
            flash('Current password is not entered correctly.')
        else:
            db.session.query(User).filter(User.email == current_user.email).update({User.password: hashpw(bytes(new_password, encoding='utf-8'), gensalt())})
            db.session.commit()
            flash('Your password has been updated.')
    form1.current_password.data = ''
    form1.new_password.data = ''

    form2 = UpdateUsernameForm()
    if form2.validate_on_submit():
        new_username = form2.new_username.data.strip()
        current_username = form2.current_username.data.strip()
        if current_user.username != current_username:
            flash('Current username is not entered correctly.')
        else:
            db.session.query(User).filter(User.email == current_user.email).update({User.username:new_username })
            db.session.commit()
            flash('Your username has been updated.')
    form2.current_username.data = ''
    form2.new_username.data = ''


    return render_template('account.html',title='Account',r=resp,courts_booked=courts_booked,feedbacks_provided=feedbacks_provided,form=form,form1=form1,form2=form2)

@user.route('/login',methods=['GET','POST'])
def login():
    # aaa.1
    #
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        p = user.password
        # if user and form.password.data == p:
        if user and checkpw(bytes(form.password.data,encoding='utf-8'),p):
            login_user(user)
            # msg = Message('Hello', sender='leongjason822@gmail.com', recipients=['leongjason3781@gmail.com'])
            # msg.body = 'Hi, someone just locked into your favourite account. Was this you?'
            # mail.send(msg)
            flash('You have been logged in.')
            return redirect(url_for('user.account'))
        else:
            flash('Login unsuccessful. Please check email and password.')
    else:
        flash('Please check your email and password again.')
    return render_template('login.html',title='Login',form=form)

@user.route('/register',methods=['POST','GET'])
def register():
    confirm = 0
    form = RegistrationForm()
    if form.validate_on_submit(): # from Flaskform
        hashed = hashpw(bytes(form.password.data,encoding='utf-8'),gensalt())
        user = User(username=form.username.data,email=form.email.data,password=hashed)
        if User.query.filter_by(username=form.username.data.strip()).first():
            flash('This username has been taken. Please try a different one.')
            confirm += 1
        if User.query.filter_by(email=form.email.data.strip()).first():
            if confirm == 0:
                flash('This email has been taken. Please try a different one.')
            else:
                pass
            confirm += 1
        if confirm == 0:
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



















