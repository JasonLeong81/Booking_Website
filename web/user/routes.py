from flask import Blueprint, render_template, flash, redirect, url_for, request, session, abort
from web.user.forms import RegistrationForm, LoginForm, UpdateEmailForm, UpdatePasswordForm, UpdateUsernameForm, ShoppingListForm, MakePriviledged
from web.models import User, Feedback, Booking, Messages, Grocery, Recipes, Shopping, Friends, Booking_Hair_Cut
from flask_login import login_required, logout_user, login_user, current_user
from bcrypt import *
from web import mail, Message, db, main, app
from datetime import datetime
from web.admin.routes import admin
import os

user = Blueprint('user',__name__)


@user.route('/account',methods=['GET','POST'])
@login_required
def account():
    # db.session.query(User).filter(User.username == 'Jason').update({User.username: 'Jasoni'}) # updating rows in database
    # db.session.commit()
    # hashed = hashpw(bytes(form.password.data, encoding='utf-8'), gensalt())
    # if user and checkpw(bytes(form.password.data, encoding='utf-8'), p):
    try:
        if session['id']:
            print(session['id'])
    except:
        print('no session id')
    courts_booked = Booking.query.filter_by(user_id=current_user.id)
    feedbacks_provided = Feedback.query.filter_by(user_id=current_user.id)
    if current_user.is_authenticated:
        resp = {"result": 200,
                "data": current_user}
    else:
        resp = {"result": 401,
                "data": {"message": "user no login"}}
    ### Profile picture ###


    if request.method == 'POST':
        if 'Change_Profile_Picture' in request.form:
            if request.form['Change_Profile_Picture'] == 'Confirm':
                profile_picture = request.files['Profile_Picture']
                # print(dir(profile_picture))
                file_name,file_extension = os.path.splitext(profile_picture.filename)
                # print('file_name: ',file_name)
                # print('file_extension: ',file_extension)
                # print('app.root_path: ',app.root_path)
                picture_filename_in_database = os.path.join(app.root_path,'static\pictures\profile_pictures',str(current_user.id)+f'{file_extension}')
                # print('picture_filename_in_database: ',picture_filename_in_database)
                profile_picture.save(picture_filename_in_database)
                flash('Profile Picture has been updated.')
                return redirect(url_for('user.account'))

    # pp = os.path.join(app.root_path, 'static\pictures\profile_pictures', str(current_user.id)+'.png')
    profile_picture = False
    # checking whether current user has a profile picture, if not then we will use male.png as default
    for root, dirs, files in os.walk('web/static/pictures/profile_pictures'):
        # print('root',root)
        # print('dirs',dirs)
        for file in files:
            if file.endswith(f'{current_user.id}.png'):
                print(root + '/' + str(file))
                pp = url_for('static', filename='pictures/profile_pictures/' + str(current_user.id) + '.png')
                profile_picture = True
    if profile_picture == False:
        pp = url_for('static', filename='pictures/male.png')
    print(pp,1111111111111111111111111111,profile_picture)



    ### Make/Remove Priviledged ###
    form3 = MakePriviledged()
    if request.method == 'POST':
        if form3.validate_on_submit():
            # what we get back from hidden tag in html form is the username of the user whose current_user wants to make priviledged
            # so we query that id in the friends table with status = 1 (this means they are friends) and toggle Priviledged from 0 to 1. Note here that the From_id and To_id can be any of these two users because of how the accepting of friend request works in this code base

            if form3.submit_grant.data == True and form3.submit_remove.data == False:
                try:
                    user_to_be_made_priviledged_username = form3.Good_Friend_username.data.strip()
                    user_exist = User.query.filter_by(username=user_to_be_made_priviledged_username).first()
                    if user_exist == None:
                        flash(f'User {user_to_be_made_priviledged_username} does not exist.')
                        raise ValueError # so that else would not run
                    user_to_be_made_priviledged_id = User.query.filter_by(username=user_to_be_made_priviledged_username).first().id
                    two_user_are_friends = Friends.query.filter_by(To_id=int(user_to_be_made_priviledged_id), Status=1,From_id=current_user.id).first()
                    if two_user_are_friends == None: # see if they are friends
                        flash(f'You and {user_to_be_made_priviledged_username} are not friends so {user_to_be_made_priviledged_username} will not be able to edit your shopping list.')
                        raise ValueError  # just for fun
                except Exception as m:
                    print(m,1)
                    pass
                else:
                    db.session.query(Friends).filter(Friends.From_id == int(user_to_be_made_priviledged_id) ,Friends.Status==1,Friends.To_id==current_user.id).update({Friends.Priviledged: 1})  # toggling Friend's table Priviledged from 0 to 1 by making sure that they are friends
                    db.session.commit()
                    flash(f'Your friend {user_to_be_made_priviledged_username} can now edit your shopping list!')
            elif form3.submit_remove.data == True and form3.submit_grant.data == False:
                try:
                    user_to_be_made_priviledged_username = form3.Good_Friend_username.data.strip()
                    user_exist = User.query.filter_by(username=user_to_be_made_priviledged_username).first()
                    if user_exist == None:
                        flash(f'User {user_to_be_made_priviledged_username} does not exist.')
                        raise ValueError # so that else would not run
                    user_to_be_made_priviledged_id = User.query.filter_by(username=user_to_be_made_priviledged_username).first().id
                    two_user_are_friends = Friends.query.filter_by(To_id=int(user_to_be_made_priviledged_id), Status=1,From_id=current_user.id).first()
                    if two_user_are_friends == None: # see if they are friends # we can choose to check any columns not just From_id
                        flash(f'You and {user_to_be_made_priviledged_username} are not friends so {user_to_be_made_priviledged_username} will not be able to edit your shopping list.')
                        raise ValueError # just for fun
                except Exception as m:
                    # flash(f'You and {user_to_be_made_priviledged_username} are not friends so {user_to_be_made_priviledged_username} will not be able to edit your shopping list.')
                    print(m,2)
                    # pass
                else:
                    db.session.query(Friends).filter(Friends.From_id == int(user_to_be_made_priviledged_id) ,Friends.Status==1,Friends.To_id==current_user.id).update({Friends.Priviledged: 0})  # toggling Friend's table Priviledged from 0 to 1 by making sure that they are friends
                    db.session.commit()
                    flash(f'Your friend {user_to_be_made_priviledged_username} can no longer edit your shopping list!')
            return redirect(url_for('user.account'))


    ### Remove friends ###
    if request.method == 'POST':
        if 'remove_friend' in request.form:
            if request.form['remove_friend'] == 'Remove':
                mine,friend = int(str(request.form['Friends_id']).split('/')[0]),int(str(request.form['Friends_id']).split('/')[1])
                db.session.delete(Friends.query.filter_by(id=mine).first())
                db.session.delete(Friends.query.filter_by(id=friend).first()) # remove the other one
                db.session.commit()
                flash('Removed a friend.')

    ### see friends ###
    f = []
    myfriends = Friends.query.filter_by(Friend_of_id=current_user.id,Status=1) # get all users whose value of Friend_of_id is me with status 1 from Friend's table # friends of id is relative to from_id

    try:
        for MyFriends in myfriends:
            the_other_one = Friends.query.filter_by(Friend_of_id=MyFriends.From_id,Status=1).first().id
            f.append([User.query.filter_by(id=MyFriends.From_id).first(),str(MyFriends.id) + '/' + str(the_other_one)]) # [User_object,Friends_id for mine and friend in one strig]
    except:
        pass

    ### see friend_request ###
    Friend_Request_temp = Friends.query.filter_by(To_id=current_user.id,Status=0)
    Friend_Request = []
    for i in Friend_Request_temp:
        user_id = i.From_id # Friend's table id
        User_who_added_you = User.query.filter_by(id=user_id).first()
        try:
            Friend_Request.append([User_who_added_you.username,i.Date,i.id]) # [User,date,id of adder in Friends table]
        except:
            pass
    if request.method == 'POST':
        if 'accept_friend_request' in request.form:
            if request.form['accept_friend_request'] == 'Accept':
                id_in_FriendsTable = int(request.form['id_in_FriendsTable'])
                db.session.query(Friends).filter(Friends.id == id_in_FriendsTable).update({Friends.Status: 1,Friends.Friend_of_id:current_user.id}) # toggling Friend's table Status from 0 to 1
                db.session.commit()
                ### Once accepted, we insert a row into Friend's table but with Friend_of_id being the person whose current_user accepted as friend, from_id and to_id will be swapped, and the date would be datetime.today() ###
                # this is optional, since we can always tell users to add each other if they wanna be friends #
                person_whose_currentuser_accepted = Friends.query.filter_by(id=int(request.form['id_in_FriendsTable'])).first().From_id # person who sent current_user the friend request
                success_friend_request_response = db.session.query(Friends).filter(Friends.To_id==current_user.id, Friends.From_id==User.query.filter_by(id=person_whose_currentuser_accepted).first().id).update({Friends.Status: 1,Friends.Friend_of_id:current_user.id})
                add_friend = Friends(Date=datetime.today(), From=current_user, To=User.query.filter_by(id=person_whose_currentuser_accepted).first(), Status=0,Priviledged=0,Friend_of_id=0) # counter adding and accepting
                success_friend_request_response = db.session.query(Friends).filter(Friends.From_id==current_user.id, Friends.To_id==User.query.filter_by(id=person_whose_currentuser_accepted).first().id).update({Friends.Status: 1,Friends.Friend_of_id:User.query.filter_by(id=person_whose_currentuser_accepted).first().id})
                db.session.add(add_friend)
                db.session.commit()
                # print('Done'*100)
                ## end of optional code ###
                flash('Accepted friend request.')

        if 'decline_friend_request' in request.form:
            if request.form['decline_friend_request'] == 'Decline':
                # db.session.query(Friends).filter(Friends.id == int(request.form['id_in_FriendsTable'])).update({Friends.Status: 2,Friends.Friend_of_id:current_user.id})  # toggling Friend's table Status from 0 to 2
                friend_request_to_be_deleted = Friends.query.filter_by(id=int(request.form['id_in_FriendsTable'])).first()
                db.session.delete(friend_request_to_be_deleted) # deleting a friend request that has been rejected
                db.session.commit()
                flash('Declined friend request.')
        return redirect(url_for('user.account'))



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


    return render_template('account.html',title='Account',r=resp,courts_booked=courts_booked,feedbacks_provided=feedbacks_provided,form=form,form1=form1,form2=form2,fr=Friend_Request,myFriends=f,form3=form3,pp=pp)

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
        p = bytes(p, 'utf-8')
        if user and checkpw(bytes(form.password.data,encoding='utf-8'),p):
            login_user(user)
            db.session.query(User).filter(User.id == current_user.id).update({User.logged_in: 'True'})
            db.session.commit()
            # msg = Message('Hello', sender='leongjason822@gmail.com', recipients=['leongjason3781@gmail.com'])
            # msg.body = f'{current_user.username} has logged in with email {current_user.email}.'
            # mail.send(msg)
            flash('You have been logged in.')
            if current_user.admin == 'True':
                return redirect(url_for('admin.admin_Account'))
            else:
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
        hashed = hashed.decode("utf-8", "ignore") # decode this into string for postgres
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
    db.session.query(User).filter(User.id == current_user.id).update({User.logged_in: 'False'})
    db.session.commit()
    logout_user()
    return redirect(url_for('user.login'))
    # return redirect(url_for(main.home)) # why can't this work?

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
    # print("ans:",ans)
    return render_template('random_functions.html',error=error,results=results,default1=default1,default2=default2,today=str(datetime.today().date()))


def change(INPUT):
    d = {'Breakfast':1,'Lunch':2,'Tea-Time':3,'Dinner':4,'Supper':5}
    return d[INPUT]

@user.route('/grocery',methods=['POST','GET'])
@login_required
def grocery():
    global friend_grocery, friend
    friend_grocery = None
    friend = None

    counter = 0
    if request.method == 'POST':
        # if request.form['add'] == 'Add':
        if 'add' in request.form:
            temp = request.form['date'].split('-')
            d_grocery = datetime(int(temp[0]),int(temp[1]),int(temp[2]))
            # print(d_grocery,type(d_grocery))
            newGrocery = Grocery(Name=request.form['food'],Type=request.form['meal'],Type_id =change(str(request.form['meal'])),Date=d_grocery,owner=current_user)
            db.session.add(newGrocery)
            db.session.commit()
            flash('One meal has been created.')
            counter += 1

        if 'delete' in request.form:
            if request.form['submit'] == 'Delete':
                myGrocery_delete = Grocery.query.filter_by(id=int(request.form['delete'])).first()
                db.session.delete(myGrocery_delete)
                db.session.commit()
                flash('One meal has been deleted.')
                counter += 1
            else:
                old_name = Grocery.query.filter_by(id=int(request.form['delete'])).first().Name
                session['old_name'] = old_name
                session['id'] = int(request.form['delete'])
                return redirect(url_for('user.update_grocery'))
        if counter == 1:
            counter = 0
            return redirect(url_for('user.grocery')) # counter must be 1 to execute this line

    if request.method == 'POST':
        if 'Add to My Meals' in request.form:
            item_to_copy_id = request.form.getlist('copy')
            print(item_to_copy_id)
            for copy in item_to_copy_id:
                item_to_copy_ = Grocery.query.filter_by(id=int(copy)).first()
                add_item_to_my_meal = Grocery(Name=item_to_copy_.Name,Type=item_to_copy_.Type,Type_id =item_to_copy_.Type_id ,Date=item_to_copy_.Date,owner=current_user)
                db.session.add(add_item_to_my_meal)
                db.session.commit()

        if 'search' in request.form:
            if request.form['username']:
                if len(request.form['username']) > 0:
                    search = request.form['username'].strip()
                    friend = User.query.filter_by(username=search).first()
                    if not friend:
                        flash('Could not find your friend. Please make sure his/her name is entered correctly.')
                    else:
                        friend_grocery = Grocery.query.filter_by(user_id=friend.id)


    myGrocery = Grocery.query.filter_by(user_id=current_user.id)
    # for i in myGrocery:
    #     print(i,type(i))
    myGrocery = sorted(myGrocery,key=lambda x:(x.Date,x.Type_id))
    return render_template('Grocery.html',title='MyGrocery',my=myGrocery,friend=friend_grocery,friend_name=friend)

@user.route('/update_grocery',methods=['POST','GET'])
@login_required
def update_grocery():
    # strf(A) is to make it in english
    if request.method == 'POST':
        new_name = request.form['new_name'].strip()
        db.session.query(Grocery).filter(Grocery.id == session['id']).update({Grocery.Name: f'{new_name}'})  # updating rows in database
        db.session.commit()
        flash('One meal has been updated.')
        session.pop('old_name',None)
        session.pop('id', None)
        return redirect(url_for('user.grocery'))
    return render_template('Update_Grocery.html',title='UpdateGrocery',old_name=session['old_name'])


@user.route('/recipes',methods=['POST','GET'])
@login_required
def recipes():
    global user_recipes
    user_recipes = db.session.query(Recipes.Category).filter_by(user_id=current_user.id)
    myrecipes = [] # [ ['category name',[object1,object2,...,objectn]] ]
    # Global variables are special. If you try to assign to a variable a = value inside of a function, it creates a new local variable inside the function, even if there is a global variable with the same name.To instead access the global variable, add a global statement inside the function
    if request.method == 'POST':
        if 'create' in request.form:
            new_recipe = Recipes(Name=request.form['Name'].strip(),Category=request.form['Category'].strip(),Ingredients=request.form['Ingredients'].strip(),owner=current_user)
            db.session.add(new_recipe)
            db.session.commit()
            return redirect(url_for('user.recipes'))

        if 'delete' in request.form:
            delete_recipe = Recipes.query.filter_by(id=int(request.form['delete-update-recipe'])).first()
            db.session.delete(delete_recipe)
            db.session.commit()
            return redirect(url_for('user.recipes'))

        if 'update' in request.form:
            session['update_recipe_id'] = int(request.form['delete-update-recipe'])
            return redirect(url_for('user.update_recipes'))

        if 'see' in request.form:
            user_recipes = Recipes.query.filter_by(user_id=current_user.id)  ### getting all recipes of current_user
            if request.form['Category1'] == 'All':

                for i in db.session.query(Recipes.Category).filter_by(user_id=current_user.id).distinct(): ### getting all distinct categories of current user
                    # print(i[0])
                    myrecipes.append( [i[0]] )
                for j in range(len(myrecipes)):
                    myrecipes[j].append(user_recipes.filter_by(Category=myrecipes[j][0]))

                # myrecipes = sorted(myrecipes, key=lambda x: (x[1].Name))

            else:
                if Recipes.query.filter_by(user_id=current_user.id):
                    if Recipes.query.filter_by(user_id=current_user.id).filter_by(Category=request.form['Category1']).first():
                        myrecipes.append([request.form['Category1'],Recipes.query.filter_by(user_id=current_user.id,Category=request.form['Category1'])])

    options = user_recipes.distinct() # selecing distinct values in Category column of table Recipes
    return render_template("recipes.html",title='MyRecipes',myrecipes=myrecipes,options=options)

@user.route('/update_recipes',methods=['POST','GET'])
@login_required
def update_recipes():
    if request.method == 'POST':
        if 'update' in request.form:
            db.session.query(Recipes).filter(Recipes.id == session['update_recipe_id']).update({Recipes.Name: request.form['update_Name'].strip(),Recipes.Ingredients:request.form['update_Ingredient'].strip(),Recipes.Category:request.form['update_Category'].strip()})
            db.session.commit()
            session.pop('update_recipe_id',None)
            return redirect(url_for('user.recipes'))
    recipe_to_update = Recipes.query.filter_by(id=session['update_recipe_id']).first()
    return render_template('Update_recipe.html', title='UpdateRecipe', recipe_to_update=recipe_to_update)





import stripe
stripe.api_key = app.config['STRIPE_SECRET_KEY']
@user.route('/payment',methods=['POST','GET'])
@login_required
def payment():
    ### this way everytime we refresh the payment.html page, we have a payment that is failed
    ### everytime we reload the page, we create a session
    # session = stripe.checkout.Session.create(
    #     payment_method_types=['card'],
    #     line_items = [{
    #         'price':'price_1IUZP9GCE7nPsl2DJjIrwwTf',
    #         'quantity':1
    #     }],
    #     mode='payment',
    #     success_url=url_for('user.account',_external=True) + '?session_id={CHECKOUT_SESSION_ID}',
    #     cancel_url=url_for('user.payment',_external=True)
    # )
    # return render_template('payment.html',title='payment',checkout_session_id=session['id'],checkout_public_key=app.config['STRIPE_PUBLIC_KEY'])
    return render_template('payment.html',title='payment')

@user.route('/ajax_payment',methods=['POST','GET'])
@login_required
def ajax_payment():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items = [{
            'price':'price_1IUZP9GCE7nPsl2DJjIrwwTf',
            'quantity':1
        }],
        mode='payment',
        success_url=url_for('user.account',_external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('user.payment',_external=True)
    )
    # print(session['id'])
    return {
        'checkout_session_id': session['id'],
        'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
    }

# @app.route('/stripe_webhook', methods=['POST'])
# def stripe_webhook():
#     print('WEBHOOK CALLED')
#     if request.content_length > 1024 * 1024:
#         print('REQUEST TOO BIG')
#         abort(400)
#     payload = request.get_data()
#     sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
#     endpoint_secret = 'YOUR_ENDPOINT_SECRET'
#     event = None
#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, endpoint_secret
#         )
#     except ValueError as e:
#         # Invalid payload
#         print('INVALID PAYLOAD')
#         return {}, 400
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         print('INVALID SIGNATURE')
#         return {}, 400
#     # Handle the checkout.session.completed event
#     if event['type'] == 'checkout.session.completed':
#         session = event['data']['object']
#         print(session)
#         line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
#         print(line_items['data'][0]['description'])
#     return {}




@user.route('/shopping_list',methods=['POST','GET'])
@login_required
def shopping_list():
    Shopping_List_wanted = []
    name_friend_shoppinglist = ''

    form = ShoppingListForm()
    items = Shopping.query.filter_by(user_id=current_user.id) # get all items that have user_id the same as current user's id
    if request.method == 'POST':
        if form.validate_on_submit():
            Item_Name = form.Item.data.strip()
            Date = datetime.today()
            Description = form.Description.data.strip()
            add_new_shopping_item = Shopping(Item_Name=Item_Name,Date=Date,Description=Description,owner=current_user,Edited_by=current_user.username)
            db.session.add(add_new_shopping_item)
            db.session.commit()
            return redirect(url_for('user.shopping_list'))
        if 'shopping_item_delete' in request.form:# if name in request.form
            if request.form.get('shopping_item_delete') == "Delete": # if name == value
                delete_one_shopping_item = Shopping.query.filter_by(id=int(request.form.get('id_shopping_item_delete'))).first()
                db.session.delete(delete_one_shopping_item)
                db.session.commit()
                flash('One item has been deleted.')
                return redirect(url_for('user.shopping_list'))
        if 'shopping_item_update' in request.form:# if name in request.form
            if request.form.get('shopping_item_update') == "Update": # if name == value
                session['update_item_name'], session['update_item_description'] = Shopping.query.filter_by(id=int(request.form.get('id_shopping_item_update'))).first().Item_Name, Shopping.query.filter_by(id=int(request.form.get('id_shopping_item_update'))).first().Description
                session['id_shopping_item_update'] = int(request.form.get('id_shopping_item_update'))
                return redirect(url_for('user.update_shopping_item'))

        ### we want a search bar to show which shopping list we wanna see, default to our own self's ###
        # Pending: who edited and
        if 'See_Shopping_List_Of' in request.form:
            if request.form['See_Shopping_List_Of'] == 'See':
                Shopping_List_Of_username = request.form['Shopping_List_Of'].strip() # name of a user whose shopping list is what current_user wanna see
                if User.query.filter_by(username=Shopping_List_Of_username).first() == None:
                    flash(f'User "{Shopping_List_Of_username}" does not exist')
                elif Shopping_List_Of_username == current_user.username:
                    flash('Your shopping list has already been shown. ')
                elif Friends.query.filter_by(To_id=User.query.filter_by(username=Shopping_List_Of_username).first().id,From_id=current_user.id,Status=1).first() == None:
                    flash(f'You and {Shopping_List_Of_username} are not friends yet.')
                elif Friends.query.filter_by(To_id=User.query.filter_by(username=Shopping_List_Of_username).first().id,From_id=current_user.id,Status=1).first().Priviledged == 0: # From_id and To_id here is the opposite as when we made them as friends. If A grants permission to B, we will look for the request that A sent in friend's table and change that priviledge to 1 but the other request will still be 0
                    # print('Executed',1)
                    # print(Friends.query.filter_by(To_id=User.query.filter_by(username=Shopping_List_Of_username).first().id,From_id=current_user.id,Status=1).first().Priviledged)
                    # print(Friends.query.filter_by(From_id=User.query.filter_by(username=Shopping_List_Of_username).first().id,To_id=current_user.id,Status=1).first().Priviledged)
                    flash(f'"{Shopping_List_Of_username}" has not granted you the priviledge to edit his/her shopping list.')
                else:
                    # print('executed',2)
                    name_friend_shoppinglist = Shopping_List_Of_username
                    Shopping_List_Of_id = User.query.filter_by(username=str(Shopping_List_Of_username)).first().id
                    Shopping_List_wanted = Shopping.query.filter_by(user_id=int(Shopping_List_Of_id))


    return render_template('Shopping_List.html',title='MyShoppingList',form=form,items=items,Shopping_List_wanted=Shopping_List_wanted,shopper=name_friend_shoppinglist)

@user.route('/update_shopping_item',methods=['POST','GET'])
@login_required
def update_shopping_item():
    if request.method == 'POST':
        db.session.query(Shopping).filter(Shopping.id == session['id_shopping_item_update']).update({Shopping.Item_Name: request.form.get('new_Item_Name').strip(),Shopping.Date:datetime.today(),Shopping.Description:request.form.get('new_Item_Description').strip(),Shopping.Edited_by:current_user.username}) # updating rows in database
        db.session.commit()
        flash('One item has been update.')
        session.pop('update_item_name', None)
        session.pop('update_item_description', None)
        session.pop('id_shopping_item_update', None)
        return redirect(url_for('user.shopping_list'))
    return render_template('update_shopping_item.html',title='UpdateShoppingItem',Old_Item_Name=session['update_item_name'],Old_Item_Description=session['update_item_description'])

@user.route('/hair_cut',methods=['POST','GET'])
@login_required
def HairCut():
    if request.method == "POST":
        if 'Book_Hair_Cut_appointment' in request.form:
            if request.form['Book_Hair_Cut_appointment'] == 'Book':
                service, Date_raw = str(request.form['Service'].strip()),request.form['Date']
                Date = datetime(int(Date_raw[0:4]),int(Date_raw[5:7]),int(Date_raw[8:10]),int(Date_raw[11:13]),int(Date_raw[14:]))
                # print(service,11111111111111111111111111,type(service))
                # print(Date,1111111111111111111111111,type(Date)) # 2021-05-04T16:55 is in the form of a string
                Appointment = Booking_Hair_Cut(Date=Date,Service=service,owner=current_user)
                db.session.add(Appointment)
                db.session.commit()
                flash('Your hair cut appointment has been booked.')
                return redirect(url_for('user.HairCut'))

        if "update" in request.form: # update appointment
            if request.form['update'] == 'Update':
                booking_hair_cut_appointment_id = int(request.form['booking_hair_cut_appointment_id'])
                session['booking_hair_cut_appointment_id'] = booking_hair_cut_appointment_id
                return redirect(url_for('user.Update_Hair_Cut_Appointment'))

        if "cancel" in request.form: # cancel appointment
            if request.form['cancel'] == 'Cancel':
                booking_hair_cut_appointment_id = int(request.form['booking_hair_cut_appointment_id'])
                booking_hair_cut_appointment_ToBeDeleted = Booking_Hair_Cut.query.filter_by(id=booking_hair_cut_appointment_id).first()
                db.session.delete(booking_hair_cut_appointment_ToBeDeleted)
                db.session.commit()
                flash('Your hair cut appointment has been cancelled.')
                return redirect(url_for('user.HairCut'))

    appointments = Booking_Hair_Cut.query.filter_by(user_id=current_user.id)
    default_booking_date_temp = datetime.today()
    default_booking_date = default_booking_date_temp.strftime('%Y-%m-%dT%H:%M')

    if appointments.first() == None:
        return render_template('Hair_Cut.html', title='Hair_Cut',default_booking_date=str(default_booking_date))
    else:
        return render_template('Hair_Cut.html',title='Hair_Cut',appointments=appointments,default_booking_date=str(default_booking_date))

@user.route('/updated_hair_cut_appointment',methods=['POST','GET'])
@login_required
def Update_Hair_Cut_Appointment():
    if request.method == 'POST':
        if "Update_Hair_Cut_appointment" in request.form:
            if request.form['Update_Hair_Cut_appointment'] == 'Update':
                service, Date_raw = str(request.form['Service'].strip()),request.form['Date']
                Date = datetime(int(Date_raw[0:4]),int(Date_raw[5:7]),int(Date_raw[8:10]),int(Date_raw[11:13]),int(Date_raw[14:]))
                db.session.query(Booking_Hair_Cut).filter(Booking_Hair_Cut.id == session['booking_hair_cut_appointment_id']).update({Booking_Hair_Cut.Date:Date,Booking_Hair_Cut.Service: service})
                db.session.commit()
                flash('Your hair cut appointment has been updated.')
                session.pop('booking_hair_cut_appointment_id',None)
                return redirect(url_for('user.HairCut'))
    default_booking_date_temp = datetime.today()
    default_booking_date = default_booking_date_temp.strftime('%Y-%m-%dT%H:%M')
    return render_template('Update_HairCutAppoinment.html', title='Update_Hair_Cut_Appoinment',default_booking_date=default_booking_date)
