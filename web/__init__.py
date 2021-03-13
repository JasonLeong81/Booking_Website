from flask import Flask
from web.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'user.login'
login_manager.init_app(app)
# print(db, 'dbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
mail = Mail(app)


from web.main.routes import main
app.register_blueprint(main)
from web.user.routes import user
app.register_blueprint(user)
from web.admin.routes import admin
app.register_blueprint(admin)

db.create_all()



def Make_admins():
    from web.models import User
    from bcrypt import hashpw, gensalt
    # admins = {email:username,password,admin}
    admins = {
        'jason@gmail.com': ['jason',1,'True'],
        'mum@gmail.com': ['mum', 1, ''],
        'dad@gmail.com': ['dad', 1, ''],
        'GB@gmail.com': ['GB', 1, ''],
        'piggy@gmail.com': ['piggy', 1, '']
    }
    for emails in admins:
        user = User.query.filter_by(email=emails).first()
        print(user)
        if not user:
            user = User(username=admins[emails][0], password=hashpw(bytes(str(admins[emails][1]), encoding='utf-8'), gensalt()),email=emails, admin=admins[emails][2])
            db.session.add(user)
        db.session.commit()
    print('Admins have been created!')
Make_admins()









def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    # print(db,'dbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')

    from web.main.routes import main
    app.register_blueprint(main)

    from web.user.routes import user
    app.register_blueprint(user)

    return app




# if __name__ =='__main__':
#     app = create_app()
#     app.run(debug=True)
# set FLASK_APP = web
# flask run


