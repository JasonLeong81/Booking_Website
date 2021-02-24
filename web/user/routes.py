from flask import Blueprint, render_template, flash, redirect, url_for, request
from web.user.forms import RegistrationForm, LoginForm, UpdateEmailForm, UpdatePasswordForm, UpdateUsernameForm
from web.models import User, Feedback, Booking, Messages
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
    number_of_users = User.query.all()
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
    else:
        if form.current_email.data:
            flash('This is not your email. Please try again.')
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
        elif User.query.filter_by(username=new_username).first():
            flash('This username has been taken. Please try a differnt one.')
        else:
            db.session.query(User).filter(User.email == current_user.email).update({User.username:new_username })
            db.session.commit()
            flash('Your username has been updated.')
    else: # if username format is wrong, then this will be executed (for future use)
        if form2.current_username.data:
            flash('This is not your username. Please try again.')
    form2.current_username.data = ''
    form2.new_username.data = ''


    return render_template('account.html',title='Account',r=resp,courts_booked=courts_booked,feedbacks_provided=feedbacks_provided,form=form,form1=form1,form2=form2,number_of_users=len(number_of_users))

@user.route('/login',methods=['GET','POST'])
def login():
    # aaa.1
    #
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip()).first()
        if not user:
            flash('This email is not registered in our servers.')
            return render_template('login.html', title='Login', form=form)
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
        if form.email.data:
            flash('Invalid Email.')
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
    return render_template('home.html',title='Home')

@user.route('/messages')
@login_required
def messages():
    m = Messages.query.filter_by(user_id=current_user.id)
    return render_template('Messages.html',title='Messages',m=m)

@user.route('/delete_messages',methods=['POST','GET'])
@login_required
def delete_message():
    message_to_delete = Messages.query.filter_by(id=request.form['id_message']).first()
    db.session.delete(message_to_delete)
    db.session.commit()
    return redirect(url_for('user.messages'))

##################### Random Functions ########################################
@user.route('/covid',methods=['POST','GET'])
def covid():
    error = []
    results = []
    default1 = []
    default2 = []
    e = ''

    from bs4 import BeautifulSoup
    import requests
    from datetime import date, timedelta, datetime

    date_test = []
    today = datetime.today()
    for i in range(10):
        date_test.append(today - timedelta(days=1))

    def clean_1(l):
        # clean commas and brackets
        for i in range(1, len(l)):
            for j in range(len(l[i][1])):
                # print(l[i][1][j])
                if l[i][1][j] == '(':
                    l[i][1] = l[i][1][:j].strip()
                    break
        for i in range(1, len(l)):
            for j in range(len(l[i][1])):
                if l[i][1][j] == ',':
                    l[i][1] = l[i][1][:j] + l[i][1][j + 1:]
                    break

            l[i][1] = int(l[i][1])
        return l
        # for i in l:
        #     print(i[1],type(i[1]))

    # clean_1([['NEGERI', 'BILANGAN KES BAHARU *( )', 'BILANGAN KES KUMULATIF'], ['SABAH', '260 (1)', '34,083'], ['SELANGOR', '692 (2)', '23,623'], ['W.P. KUALA LUMPUR', '197 (3)', '9,623'], ['NEGERI SEMBILAN', '174', '6,858'], ['JOHOR', '77 (2)', '2,912'], ['PULAU PINANG', '37', '2,900'], ['KEDAH', '4', '2,869'], ['PERAK', '65', '2,775'], ['W.P. LABUAN', '19', '1,495'], ['SARAWAK', '1', '1,085'], ['PAHANG ', '6', '861'], ['MELAKA', '140', '691'], ['KELANTAN', '1', '483'], ['TERENGGANU', '4', '285'], ['W.P. PUTRAJAYA', '6', '228'], ['PERLIS', '0', '45'], ['JUMLAH KESELURUHAN', '1,683 (8)', '90,816']]
    # )

    def detail(link):
        import csv
        # url = "https://kpkesihatan.com/"
        # source = requests.get(url).text
        # soup = BeautifulSoup(source, 'lxml')
        # print(soup.prettify())
        url = link
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')
        # n = soup.find_all('figure',class_='wp-block-table')
        try:
            n = soup.findAll('figure', class_='wp-block-table')[1]
        except:
            # print('Sorry there was an error, please go to the link above.')
            error.append('Sorry there was an error, please go to the link above.')
            return
        # print(url)

        # for i in n:
        #     print(i)
        # print(n.table.tbody)
        # return

        temp = []
        # for j in n[1:]:
        for j in n.table.tbody:
            try:
                tr = j.find_all('td')
                # print(tr)
                # return
            except:
                pass
                # print('j', tr)
            else:
                # for h in tr:
                #     tds = h.find_all('td')
                # temp.append([tds[0].text,tds[1].text,tds[2].text])
                temp.append([tr[0].text, tr[1].text, tr[2].text])
        try:
            l = len(temp[0][1])
        except:
            # print(temp)
            # print('Sorry there was an error, please go to the link above.')
            error.append('Sorry there was an error, please go to the link above.')
            return
        for i in range(l):
            if temp[0][1][i] == '*':
                temp[0][1] = temp[0][1][:i + 1] + '( )'
                break
        # for i in temp:
        #     print(i)
        return temp

    def Filter(INPUT, Sort=None):
        if date(int(INPUT[0:4]), int(INPUT[5:7]), int(INPUT[8:])) > date.today():
            # print(f'This date is in the future! Please enter any date before {date.today()}')
            e = f'This date is in the future! Please enter any date before {date.today()}'
            error.append(e)
            return
        url = "https://kpkesihatan.com/"
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')
        strings = soup.find_all('time', class_='entry-date')

        # target = f"Kenyataan Akhbar KPK {day_of_month} Disember 2020 – Situasi Semasa Jangkitan Penyakit Coronavirus 2019 (COVID-19) di Malaysia"
        state = 'all'

        ### duplicate times
        duplicates = []
        term = ''
        for i in range(0, len(strings)):
            if strings[i].text == term:  # if date is equals to previous date
                duplicates.append(
                    [strings[i]['datetime'][:10], i])  # add duplicate dates with their order according to the website
            else:
                term = strings[i].text
            # print(strings[i]['datetime'][:10]) # list of dates
            # print(strings[i],i)
        # print(duplicates) # duplicate dates
        # print(INPUT)

        correct_link_id = ''
        for i in duplicates:
            if INPUT == i[0]:
                # print(INPUT,i[1])
                correct_link_id = i[1]  # taking the latest date
        if correct_link_id == '':  # input is not one of duplicates
            for i in range(len(strings)):
                # print(strings[i]['datetime'][:10],INPUT)
                if strings[i]['datetime'][:10] == INPUT:
                    correct_link_id = i

        # e = f'If there is an error, please go to the link: {url}\n'
        # default1.append(e) # this has been replaced by javascript

        # print(f'If there is an error, please go to the link: {url}')
        # print(url)
        # print()
        if len(INPUT) == 10:
            if correct_link_id == '' and date(int(INPUT[0:4]), int(INPUT[5:7]), int(
                    INPUT[8:])) != date.today():  # date is too long ago, information not in website
                # print(date(int(INPUT[0:4]),int(INPUT[5:7]),int(INPUT[8:])), date.today())
                # print(INPUT,'might be too long ago and may not be available anymore. Please go to the link above for more information.')
                e = f'{INPUT} might be too long ago and may not be available anymore. Please go to the link above for more information.'
                error.append(e)
                return
        ### end of duplicate times

        for i in range(0, len(strings)):
            # print(i)
            if strings[i].has_attr('datetime') and strings[i]['datetime'][:10].strip() == INPUT and i == correct_link_id:
                # print(INPUT)
                parent_link = strings[i].find_parent('a')['href']  # finding first parent
                # print(parent_link,'pl')
            # print(INPUT,i['datetime'][:10].strip())
            else:
                # print(strings[i])
                continue
            # continue
            # return
            if parent_link:
                if not Sort:
                    t = detail(parent_link)
                    # for i in t:
                    #     if state.upper() == "ALL":
                    #         print(i)
                    #     if state.upper() == i[0]:
                    #         print(i)
                    #         break
                    return t
                else:
                    t = detail(parent_link)
                    if t:
                        # print(t)
                        t = clean_1(t)
                        if Sort.upper() == 'A':
                            for i in range(1, len(t) - 2):
                                for j in range(1, len(t) - 2):
                                    if t[j][1] > t[j + 1][1]:
                                        t[j + 1], t[j] = t[j], t[j + 1]
                        else:
                            for i in range(1, len(t) - 2):
                                for j in range(1, len(t) - 2):
                                    if t[j][1] < t[j + 1][1]:
                                        t[j + 1], t[j] = t[j], t[j + 1]
                        # for i in t:
                        #     if state.upper() == "ALL":
                        #         print(i)
                        #     if state.upper() == i[0]:
                        #         print(i)
                        #         break
                        return t
        foo = f'{date.today().year}-{date.today().month}-{date.today().day}'
        foo = date.today().strftime('%Y-%m-%d')
        if foo == INPUT:
            # print('Unavailable, please try again at around 6:00 pm to 8:00 pm.')
            error.append('Unavailable, please try again at around 6:00 pm to 8:00 pm.')
            return 'Unavailable, please try again at around 6:00 pm to 7:00 pm.'
        else:
            print('foo:',foo,INPUT)
            error.append('Sorry there was an error, please go to the link above.')
            return 'Sorry here was an error, plese go to the link above.'

    # print()
    # print('\nFor results today, you do not need to enter the date. Simply skip by pressing enter. For results on other days, please specify the date in the form yyyy-mm-dd.')
    # print()
    default1.append('For results today, just click the "Find" button. For past results, please specify the desired date in the form yyyy-mm-dd.')

    # ans = input('Enter date: ')
    ans = ''
    if request.method == 'POST':
        ans = request.form.get('date').strip()
    # print('AAAAAAAAAAAAAAAAAA:',ans)
    # return render_template('random_functions.html',error=error,results=results,default=default)

    base = date.today()
    date_list = [base - timedelta(days=x) for x in range(10)]

    def check_input(d):
        if type(d) == date:
            if len(str(d)) == 8:  # yyyy-m-d
                return str(f'{d.year}-0{d.month}-0{d.day}')
            else:  # yyyy-mm-dd
                return str(f'{d.year}-{d.month}-{d.day}')
        if len(d) == 0:
            return str(f'{date.today()}')
        temp = d.split('-')
        return str(f'{temp[0]}-{temp[1]}-{temp[2]}')

    e = f'Date entered: {check_input(ans)}'
    default2.append(e)

    t = Filter(check_input(ans), 'd')
    if t:
        for i in t[1:]:
            try:
                results.append(f'{i[0]} : {i[1]}')
            except:
                break
    else:
        error.append('Sorry, no results have been found :(')
    # print(results)
    print("ans:",ans)
    return render_template('random_functions.html',error=error,results=results,default1=default1,default2=default2,today=str(datetime.today().date()))












