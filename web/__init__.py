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


