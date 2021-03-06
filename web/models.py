from web import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
# from flask_admin.contrib.sqla import ModelView
# from flask_admin import Admin


@login_manager.user_loader
def load_user(user_id):
    # returns a user object from sqlalchemy by searching based on id provided
    # for current user etc
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    # profile_picture = db.Column(db.Integer)
    username = db.Column(db.String(30), unique=True, nullable=False)  # string of max 20 len
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100),nullable=False)
    feedback = db.relationship('Feedback',backref='owner',lazy='subquery') # Feedback model # backref allows us to do Feedback.query.all()[0].owner.(attributes of owner who created the feedback) lazy (select,joined,dynamic,subquery) # uselist = True means we can have more than one child
    court_booking = db.relationship('Booking',backref='owner',lazy='subquery')
    messages = db.relationship('Messages',backref='owner',lazy='subquery')
    grocery = db.relationship('Grocery',backref='owner',lazy='subquery')
    recipes = db.relationship('Recipes',backref='owner',lazy='subquery')
    logged_in = db.Column(db.String(10), nullable=True)
    admin = db.Column(db.String(10), nullable=True)

class Feedback(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    feedback = db.Column(db.String(100),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False) # user is the User table

class Booking(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime,nullable=False)
    end_time = db.Column(db.DateTime,nullable=False)
    date = db.Column(db.Date,nullable=False)
    court = db.Column(db.Integer,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False) # user is the User table

class Promotion(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(30),nullable=False)
    Content = db.Column(db.String(100),nullable=False)
    Dates = db.Column(db.DateTime,nullable=False)

class Messages(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    messages = db.Column(db.String(100),nullable=False)
    dates = db.Column(db.DateTime,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

class Grocery(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100),nullable=False)
    Type = db.Column(db.String(10),nullable=True)
    Type_id = db.Column(db.Integer,nullable=True)
    Date = db.Column(db.DateTime,nullable=False) # same as datetime in python
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

class Recipes(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100),nullable=False)
    Category = db.Column(db.String(100),nullable=False)
    Ingredients = db.Column(db.String(100),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)




# admin = Admin(app)
# admin.add_view(ModelView(Feedback,db.session))


# UserMixin class provides the implementation of this properties. Its the reason you can call for example is_authenticated to check if login credentials provide is correct
# or not instead of having to write a method to do that yourself.


# you've first created the database without this date column in the model Item.
# session['x'] = xxx, session.pop('x',None)




