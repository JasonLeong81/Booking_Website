from web import app, db

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

if __name__=='__main__':
    Make_admins()
    app.run(debug=True)
