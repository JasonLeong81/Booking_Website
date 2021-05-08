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





# print(date(1,1,1))



import pandas as pd
# print(pd.Timestamp.today().date())


class Item():
    def __init__(self,owner,d=datetime.today()):
        self.owner = owner
        self.d = d

item = Item('jason')
# print(item.d,item.owner)

# LIST = [1,2,3]*10
# print(len(LIST))

# ddd = '123/123'
# temp = ddd.split('/')
# print(temp[0],temp[1])



# Date = datetime.today()
# d = Date.strftime('%Y-%m-%dT%H:%M')
# print(d)

# today = datetime(datetime.today().year, datetime.today().month, datetime.today().day, 0, 0, 0)
# tomorrow = today + timedelta(hours=24)
# print(today)
# print(tomorrow)

from bcrypt import *

# hashed = hashpw(bytes('jason', encoding='utf-8'), gensalt())
# print(hashed,type(hashed))
# hashed = hashed.decode("utf-8", "ignore")
# print(hashed,type(hashed))
# by = bytes(hashed, 'utf-8')
# print(by,type(by))
# print(checkpw(bytes('jason',encoding='utf-8'),by))

# input : list of occupied datetime
# output : list of available times for booking with a minimum of 15 minutes booking and 5 minute buffer
import random
import datetime
minutes = [0,15,30]
hours = list(range(0,24,1))
# print(minutes)
# print(hours)
occupied = []
for i in hours:
    for j in range(len(minutes)-1):
        occupied.append([datetime.datetime(1,1,1,i,minutes[j]),datetime.datetime(1,1,1,i,minutes[j+1])])
# print(occupied)
def available_time(occupied):
    buffer = 5 # dependent on your mood or energy
    mn_booking_time = 15 # dependent on services then this will be automatically changed
    start = datetime.datetime(1,1,1,0,0)
    end = datetime.datetime(1,1,1,23,59)

    available = []
    # for j in range(len(occupied)):
    #     print(occupied[j][0].hour,occupied[j][0].minute)
    #     print(occupied[j][1].hour, occupied[j][1].minute)
    #     print()

    for occupied_times in range(len(occupied)-1): # middle part
        # print(occupied[occupied_times])
        if int(occupied[occupied_times][1].hour) == int(occupied[occupied_times+1][0].hour): # if two contiguous elements are in the same hour
            if int(occupied[occupied_times][1].minute) < int(occupied[occupied_times+1][0].minute): # if i[0].minute < i[1].minute. If so, that means there is some free time in the middle
                if int(occupied[occupied_times+1][0].minute) - int(occupied[occupied_times][1].minute) >= mn_booking_time + buffer: # we want at least 15 minutes booking
                    # end_time = occupied[occupied_times][1] + timedelta(minutes=mn_booking_time) + timedelta(minutes=buffer) # maximisde booking frequency
                    available.append([occupied[occupied_times][1],occupied[occupied_times+1][0]]) # maximise bookint time
        elif int(occupied[occupied_times][1].hour) < int(occupied[occupied_times+1][0].hour): # if previous hour is less than next hour
            if (60 - int(occupied[occupied_times][1].minute)) + int(occupied[occupied_times+1][0].minute) >= mn_booking_time + buffer: # straight away check for available time
                # end_time = occupied[occupied_times][1] + timedelta(minutes=mn_booking_time) + timedelta(minutes=buffer) # maximisde booking frequency
                available.append([occupied[occupied_times][1],occupied[occupied_times+1][0]]) # maximise booking time

    # beginning and ending part (remember to do checking as well )
    earliest_booking = occupied[0]
    latest_booking = occupied[-1]
    # print(earliest_booking,latest_booking)
    opening_hour = 0
    closing_hour = 24
    tomorrow = datetime.datetime(datetime.datetime.today().year,datetime.datetime.today().month,int(datetime.datetime.today().day)+1,0,0)
    if int(latest_booking[1].hour) == closing_hour-1:
        if (60 - int(latest_booking[1].minute)) >= mn_booking_time + buffer: # check if its more than buffer and required booking time
            available.append([latest_booking[1], tomorrow])  # check two things: hour and minute
    elif int(latest_booking[1].hour) < 23:
        available.append([latest_booking[1], tomorrow])  # check two things: hour and minute

    if int(earliest_booking[0].hour) == opening_hour: # check if opening hour and the earliest booking.hour is the same
        if int(abs(0 - int(earliest_booking[0].minute))) >= mn_booking_time + buffer: # check if between the opening hour and the start of earliest appointment is more than buffer + required booking time
            available.insert(0,[earliest_booking[0],datetime.datetime(datetime.datetime.today().year,datetime.datetime.today().month,datetime.datetime.today().day,0,0)]) # check two things: hour and minute
    elif opening_hour < int(earliest_booking[0].hour):
        available.insert(0, [earliest_booking[0],datetime.datetime(datetime.datetime.today().year, datetime.datetime.today().month,datetime.datetime.today().day, 0,0)])  # check two things: hour and minute

    # print('Available Times are')
    # for i in available:
    #     print(f'{i[0].hour}:{i[0].minute} to {i[1].hour}:{i[1].minute}')
    #
    # print('Occupied Times are')
    # for i in occupied:
    #     print(f'{i[0].hour}:{i[0].minute} to {i[1].hour}:{i[1].minute}')
    occupied += available
    occupied.sort() # when this is done, pass this in to this function itself and the output would be the time that are not shown to customer and owner can decide what to do about it
    # print(available)

    return available
available_time(occupied)



# result = datetime.datetime(1,1,1,1,0)+timedelta(minutes=15) + timedelta(minutes=5)
# print(result)

# don = [[datetime.datetime(2021,1,1,1,1)]]
# don += [[datetime.datetime(2020,1,1,1,3)]]
# don.extend([[datetime.datetime(2020,1,1,1,3)]])
# print(don)
# don.sort()
# print(don)


import os
dir_path = os.path.dirname(os.path.realpath(__file__)) # __file__ means current file
# print(os.path.realpath(__file__))
# print(__file__)
for root, dirs, files in os.walk(dir_path):
    # print('root',root)
    # print('dirs',dirs)
    for file in files:
        if file.endswith('t.py'):
            print(root + '/' + str(file))





