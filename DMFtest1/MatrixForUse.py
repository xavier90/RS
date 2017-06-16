from numpy import *
import datetime


def filterForUser(start, end, users):
    tmp = {}

    for user in users:
        delete = True
        for time in users[user]:
            if time > start and time < end:
                delete = False

        if not delete:
            tmp[user] = users[user]

    return tmp

def matrixDic(path = 'ml-100k'):
    #load movie data
    movies = {}
    for line in open(path + '/u.item'):
        (id, title) = line.split('|')[0:2]
        movies[id] = title

    #load data
    prefs = {}
    users = {} #dictionary to filter user

    for line in open(path + '/u.data'):
        (userId, itemId, rating, timeStamp) = line.split('\t')
        time = datetime.datetime.fromtimestamp(int(timeStamp))

        prefs.setdefault(userId,{})
        prefs[userId][itemId] = float(rating)

        users.setdefault(userId,[])
        users[userId].append(time)



    #time range of rating is from 1997.9.1 -1998.5.1, so we only have 8 months
    #get 922 users exists in all of following time window

    users1 = filterForUser(datetime.datetime(1997, 9, 1), datetime.datetime(1997, 10, 1), users)
    users2 = filterForUser(datetime.datetime(1997, 10, 1), datetime.datetime(1997, 11, 1), users)
    users3 = filterForUser(datetime.datetime(1997, 11, 1), datetime.datetime(1997, 12, 1), users)
    users4 = filterForUser(datetime.datetime(1997, 12, 1), datetime.datetime(1998, 1, 1), users)
    users5 = filterForUser(datetime.datetime(1998, 1, 1), datetime.datetime(1998, 2, 1), users)
    users6 = filterForUser(datetime.datetime(1998, 2, 1), datetime.datetime(1998, 3, 1), users)
    print len(users1), len(users2), len(users3), len(users4), len(users5), len(users6)

    #only keep 922 users
    # tmp = {}
    # for id in users6:
    #     tmp[id] = prefs[id]
    # prefs = tmp

    #if user did not rate the movie, then set the rating into zero
    for i in prefs:
        for j in movies:
            prefs[i].setdefault(j, 0)


    matrixForUse = matrix([[prefs[i][j] for j in movies] for i in prefs])
    return matrixForUse


matrixDic()