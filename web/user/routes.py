from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from web.user.forms import RegistrationForm, LoginForm, UpdateEmailForm, UpdatePasswordForm, UpdateUsernameForm
from web.models import User, Feedback, Booking, Messages, Grocery, Recipes
from flask_login import login_required, logout_user, login_user, current_user
from bcrypt import *
from web import mail, Message, db, main
from datetime import datetime
from web.admin.routes import admin

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


    return render_template('account.html',title='Account',r=resp,courts_booked=courts_booked,feedbacks_provided=feedbacks_provided,form=form,form1=form1,form2=form2)

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




