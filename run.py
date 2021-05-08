from web import app, db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

if __name__=='__main__':
    app.run(debug=True) # comment this out when migrating
    # migrate = Migrate(app, db)
    # manager = Manager(app)
    # manager.add_command('db', MigrateCommand)
    # manager.run()

# strip
# 3781
# 378100YCJL
# pip install stripe

### Commands for flask migrate
# python run.py db init # just once
# python run.py db migrate
# python run.py db upgrade