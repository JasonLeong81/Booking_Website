from datetime import datetime, timedelta

# print(datetime.now())
# x = datetime(2020, 5, 17,23,1)
# print(x)
# x = datetime(2018, 6, 1)
# print(x.strftime("%B")) # https://www.w3schools.com/python/python_datetime.asp
# print(datetime.utcnow())
# DateTime.UtcNow tells you the date and time as it would be in Coordinated Universal Time, which is also called the Greenwich Mean Time time zone - basically like it would be if you were in London England, but not during the summer. DateTime.Now gives the date and time as it would appear to someone in your current locale.


# today = datetime.utcnow()
# print('Year',today.year)
# print('Month',today.month)
# print('Day',today.day)
# print('Hour',today.hour)
# print('Min',today.minute)

def check_availability(l,court,date_wanted):
    # give the available time of a court based on schedule l

    # now = datetime.now()
    # tomorrow = datetime(now.year,now.month,now.day+1)
    # d = tomorrow - now

    now = date_wanted

    available = []

    booked = []
    for i in l[court]:
        if i[0].day == now.day:
            # print(i)
            booked.append(i)
    booked = sorted(booked)

    for i in range(len(booked)-1):
        # print(booked[i][1])
        # print(booked[i+1][0])
        if booked[i][1]<booked[i+1][0]:
            # print(booked[i][1],booked[i+1][0],'is available.')
            available.append([booked[i][1],booked[i+1][0]])
    else:
        # print(booked[-1][1], 'onwards is available.')
        for i in range(24):
            if now.day != available[0][0].day: # exclude next day
                break
            if -int(now.hour) + int(booked[0][0].hour) == 1: # first half done, now 2nd half # will only execute once
                available.append([now,now+timedelta(hours=1)])
                now = booked[-1][1]
            else:
                available.append([now,now+timedelta(hours=1)])
                now += timedelta(hours=1)
    # print('Available:')
    # for i in sorted(available):
    #     print(i[0].hour,i[1].hour)
    return (sorted(available),booked)

court = '1'
Datetime = datetime(2021,1,27,0,0)
l = {
     '1':[[datetime(2021,1,27,1,1),datetime(2021,1,27,2,1)],
          [datetime(2021,1,27,3,1),datetime(2021,1,27,5,1)],
        [datetime(2021,1,27,6,1),datetime(2021,1,27,7,1)],
          [datetime(2021,1,28,3,1),datetime(2021,1,28,5,1)]],
     '2':[[datetime(2021,1,27,1,1),datetime(2021,1,27,3,1)],[datetime(2021,1,27,4,1),datetime(2021,1,27,5,1)]],
     '3': [[datetime(2021,1,27,1,1),datetime(2021,1,27,3,1)],[datetime(2021,1,27,5,1),datetime(2021,1,27,6,1)]]
}
free,not_free = check_availability(l,court,Datetime)
# for i in free:
#     print(f'Available from {i[0].hour} to {i[1].hour}')
# print()
# for i in not_free:
#     print(f'Booked from {i[0].hour} to {i[1].hour}')

def notification(title,message,icon=None):
    # Plyer is a Python library for accessing features of your hardware / platforms.
    # pythonw <filename.py> to make it run in the background
    # relax icon ico
    from plyer import notification
    notification.notify(
        title=title,
        message=message,
        app_icon = icon,
        timeout = 10 # seconds
    )
title = 'Rest'
message = 'Rest your eyes for 20 seconds.'
icon = 'coffee.ico'
# import time
# if __name__=='__main__':
#     while True:
#         notification(title, message,icon)
#         time.sleep(1200) # 1200 seconds = 20 minutes
# pythonw test.py


# print(bin(123)) # divide two and write from bottom up the remainders


### Bcrypt ######################################3
# from bcrypt import *
# password = b'super'
# s = gensalt()
# hashed = hashpw(password, s)
# if checkpw(password,hashed):
#     print('Yes')
# else:
#     print('Nope')
# print(bytes(password))

### Send email ####################
from datetime import datetime
# print(dir(datetime.today()))
a = datetime.today().time()
# print(dir(a))
# print(a.hour,a.minute)
b = datetime.utcnow()
# print(b.date(),b.time())
# print(b)
# print(datetime.strftime(b, '%H:%M'))

# from web import db
# from web.models import Messages
# for i in Messages.query.all():
#     db.session.delete(i)
#     db.session.commit()
from datetime import date
# print(date.today().strftime('%Y %m %d'))
# aaa=[[1,date.today()], [2,date.today() + timedelta(days=1)], [3,date.today() - timedelta(days=1)]]
# aaa = sorted(aaa, key=lambda x: x[-1])
# # aaa = sorted(aaa)
# for i in aaa:
#     print(i)

def change(INPUT):
    d = {'Breakfast':1,'Lunch':2,'Tea-Time':3,'Dinner':4,'Supper':5}
    return d[INPUT]
# print(change('Breakfast'))



print(date.today())





















