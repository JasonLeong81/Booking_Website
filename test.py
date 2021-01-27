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

