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
    password = db.Column(db.String(200),nullable=False)
    Gender = db.Column(db.Integer,nullable=True) # 0 is male and 1 is female
    # Profile_picture = db.Column(db.,nullable=True)

    feedback = db.relationship('Feedback',backref='owner',lazy='subquery') # Feedback model # backref allows us to do Feedback.query.all()[0].owner.(attributes of owner who created the feedback) lazy (select,joined,dynamic,subquery) # uselist = True means we can have more than one child
    court_booking = db.relationship('Booking',backref='owner',lazy='subquery')
    messages = db.relationship('Messages',backref='owner',lazy='subquery')
    grocery = db.relationship('Grocery',backref='owner',lazy='subquery')
    recipes = db.relationship('Recipes',backref='owner',lazy='subquery')
    logged_in = db.Column(db.String(10), nullable=True)
    admin = db.Column(db.String(10), nullable=True)
    shopping_info = db.relationship('Shopping',backref='owner',lazy='subquery')
    Friend_From = db.relationship('Friends',backref='From',lazy='subquery', foreign_keys='Friends.From_id')
    Friend_To = db.relationship('Friends', backref='To', lazy='subquery', foreign_keys='Friends.To_id')
    Hair_Cut_Appointments = db.relationship('Booking_Hair_Cut',backref='owner',lazy='subquery')


class Feedback(db.Model,UserMixin): # figure out a thred like in reddit where user and admin can continuously talk about a topic
    id = db.Column(db.Integer,primary_key=True)
    feedback = db.Column(db.String(200),nullable=False)
    response_feedback = db.Column(db.String(500),nullable=True)
    Feedback_Status = db.Column(db.Integer,nullable=False) # 0 means not replied and 1 means an admin has replied
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False) # user is the User table

class Booking(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime,nullable=False) # datetime.date
    end_time = db.Column(db.DateTime,nullable=False)
    date = db.Column(db.Date,nullable=False)
    court = db.Column(db.Integer,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete="CASCADE"),nullable=False) # user is the User table

class Promotion(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(30),nullable=False)
    Content = db.Column(db.String(100),nullable=False)
    Dates = db.Column(db.DateTime,nullable=False)

class Messages(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    messages = db.Column(db.String(100),nullable=False)
    dates = db.Column(db.DateTime,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)

class Grocery(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100),nullable=False)
    Type = db.Column(db.String(10),nullable=True)
    Type_id = db.Column(db.Integer,nullable=True)
    Date = db.Column(db.DateTime,nullable=False) # same as datetime in python
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete="CASCADE"),nullable=False)

class Recipes(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100),nullable=False)
    Category = db.Column(db.String(100),nullable=False)
    Ingredients = db.Column(db.String(100),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete="CASCADE"),nullable=False)

class Shopping(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Item_Name = db.Column(db.String(100),nullable=False)
    Date = db.Column(db.DateTime,nullable=False) # default to datetime.today()
    Description = db.Column(db.String(500),nullable=False)
    Edited_by = db.Column(db.Integer, nullable=False) # username of who edited it # be careful if user is deleted (basically user not exist)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete="CASCADE"),nullable=False)

class Friends(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.DateTime,nullable=False) # default to datetime.today()
    From_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete="CASCADE"),nullable=False) # if any one of these (From_id and To_id) are deleted, the entire row will be deleted.
    To_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    Status = db.Column(db.Integer, nullable=False) # 0 -> Pending, 1 -> Accepted, 2 -> Rejected
    Friend_of_id = db.Column(db.Integer,nullable=False) # friend of id of someone in user table # if not a friend yet, then this value is 0
    Priviledged = db.Column(db.Integer,nullable=False) # if someone is priviledged, then the From_id (in this table) can edit the To_id's shopping list # Priviledged 0 is just friends and 1 means priviledged

    # From = db.relationship('User', foreign_keys=[From_id])
    # To = db.relationship('User', foreign_keys=[To_id])
    # Friend_of = db.relationship('User', foreign_keys=[Friend_of_id])

class Booking_Hair_Cut(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.DateTime,nullable=False) # datetime.date
    Service = db.Column(db.String(100),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False) # user is the User table






# admin = Admin(app)
# admin.add_view(ModelView(Feedback,db.session))


# UserMixin class provides the implementation of this properties. Its the reason you can call for example is_authenticated to check if login credentials provide is correct
# or not instead of having to write a method to do that yourself.


# you've first created the database without this date column in the model Item.
# session['x'] = xxx, session.pop('x',None)




