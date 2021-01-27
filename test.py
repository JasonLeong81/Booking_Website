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

    now = date_wanted.now()
    today = datetime(now.year,now.month,now.day,0,0)

    available = [] # [time,duration]
    for i in range(24):
        # print(today)
        available.append(today)
        today += timedelta(hours=1)
    # for i in available:
    #     print(i)

    for i in l[court]:
        if i[0].day == date_wanted.day:
            print(i)


court = '1'
Datetime = datetime(2021,1,27,1,1)
l = {
     '1':[[datetime(2021,1,27,1,1),datetime(2021,1,27,2,1)],[datetime(2021,1,27,3,1),datetime(2021,1,27,5,1)],[datetime(2021,1,28,3,1),datetime(2021,1,28,5,1)]],
     '2':[[datetime(2021,1,27,1,1),datetime(2021,1,27,3,1)],[datetime(2021,1,27,4,1),datetime(2021,1,27,5,1)]],
     '3': [[datetime(2021,1,27,1,1),datetime(2021,1,27,3,1)],[datetime(2021,1,27,5,1),datetime(2021,1,27,6,1)]]
}
check_availability(l,court,Datetime)
# now = datetime.utcnow()
# for i in range(10):
#     now += timedelta(hours=2)
#     print(now.time())