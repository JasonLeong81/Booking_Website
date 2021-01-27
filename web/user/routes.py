from flask import Blueprint, render_template, flash, redirect, url_for
from web.user.forms import RegistrationForm, LoginForm
from web import db
from web.models import User, Feedback, Booking
from flask_login import login_required, logout_user, login_user, current_user


user = Blueprint('user',__name__)


@user.route('/account',methods=['GET','POST'])
@login_required
def account():
    courts_booked = Booking.query.filter_by(user_id=current_user.id)
    feedbacks_provided = Feedback.query.filter_by(user_id=current_user.id)
    if current_user.is_authenticated:
        resp = {"result": 200,
                "data": current_user}
    else:
        resp = {"result": 401,
                "data": {"message": "user no login"}}
    return render_template('account.html',title='Account',r=resp,courts_booked=courts_booked,feedbacks_provided=feedbacks_provided)

@user.route('/login',methods=['GET','POST'])
def login():
    ### aaa@gmail.com
    ### 123
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        p = user.password
        if user and form.password.data == p:
            login_user(user)
            flash('You have been logged in.')
            return redirect(url_for('user.account'))
        else:
            flash('Login unsuccessful. Please check email and password.')
    return render_template('login.html',title='Login',form=form)

@user.route('/register',methods=['POST','GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data,password=form.password.data)
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



















