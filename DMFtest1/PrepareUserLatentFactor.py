from numpy import *
import datetime
import NMFGradientDescent
from sklearn.decomposition import NMF as NMFsimple
from sklearn.decomposition import non_negative_factorization as NMFcomplex
from sklearn.metrics import mean_squared_error as ms_error
from sklearn.metrics import mean_absolute_error as ma_error
# from sklearn.metrics import median_absolute_error as meda_error
import matplotlib.pyplot as plt

users0 = {}
users1 = {}
users2 = {}
users3 = {}
users4 = {}
users5 = {}


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


def matrixDic(timeWindowId, wholeUsers = True, overlap = True, path = 'ml-100k'):
    #load movie data
    movies = {}
    for line in open(path + '/u.item'):
        (id, title) = line.split('|')[0:2]
        movies[id] = title

    #load data
    prefs = {}
    users = {} #dictionary to filter user


    #1997/9/1 -1998/3/1
    #set time interval
    time_interval = []
    if timeWindowId == 0:
        time_interval = [datetime.datetime(1997, 9, 1), datetime.datetime(1997, 9, 15)]
    elif timeWindowId == 1:
        if overlap:
            start = datetime.datetime(1997, 9, 1)
        else:
            start = datetime.datetime(1997, 9, 15)
        time_interval = [start, datetime.datetime(1997, 10, 1)]
    elif timeWindowId == 2:
        if overlap:
            start = datetime.datetime(1997, 9, 1)
        else:
            start = datetime.datetime(1997, 10, 1)
        time_interval = [start, datetime.datetime(1997, 10, 15)]
    elif timeWindowId == 3:
        if overlap:
            start = datetime.datetime(1997, 9, 1)
        else:
            start = datetime.datetime(1997, 10, 15)
        time_interval = [start, datetime.datetime(1997, 11, 1)]
    elif timeWindowId == 4:
        if overlap:
            start = datetime.datetime(1997, 9, 1)
        else:
            start = datetime.datetime(1997, 11, 1)
        time_interval = [start, datetime.datetime(1997, 11, 15)]
    elif timeWindowId == 5:
        if overlap:
            start = datetime.datetime(1997, 9, 1)
        else:
            start = datetime.datetime(1997, 11, 15)
        time_interval = [start, datetime.datetime(1997, 12, 1)]
    elif timeWindowId == 6:
        if overlap:
            start = datetime.datetime(1997, 9, 1)
        else:
            start = datetime.datetime(1997, 12, 1)
        time_interval = [start, datetime.datetime(1997, 12, 15)]
    elif timeWindowId == 7:
        if overlap:
            start = datetime.datetime(1997, 9, 1)
        else:
            start = datetime.datetime(1997, 12, 15)
        time_interval = [start, datetime.datetime(1998, 1, 1)]
    elif timeWindowId == 8:
        if overlap:
            start = datetime.datetime(1997, 9, 1)
        else:
            start = datetime.datetime(1998, 1, 1)
        time_interval = [start, datetime.datetime(1998, 1, 15)]
    elif timeWindowId == 9:
        if overlap:
            start = datetime.datetime(1997, 9, 1)
        else:
            start = datetime.datetime(1998, 1, 15)
        time_interval = [start, datetime.datetime(1998, 2, 1)]
    elif timeWindowId == 10:
        if overlap:
            start = datetime.datetime(1997, 9, 1)
        else:
            start = datetime.datetime(1998, 2, 1)
        time_interval = [start, datetime.datetime(1998, 2, 15)]
    elif timeWindowId == 11:
        if overlap:
            start = datetime.datetime(1997, 9, 1)
        else:
            start = datetime.datetime(1998, 2, 15)
        time_interval = [start, datetime.datetime(1998, 3, 1)]



    for line in open(path + '/u.data'):
        (userId, itemId, rating, timeStamp) = line.split('\t')
        time = datetime.datetime.fromtimestamp(int(timeStamp))

        #create rating matrix
        prefs.setdefault(userId,{})
        if time >= time_interval[0] and time <= time_interval[1]:
            prefs[userId][itemId] = float(rating)
        else:
            prefs[userId][itemId] = 0.0

        #create user matrix
        users.setdefault(userId,[])
        users[userId].append(time)


    #time range of rating is from 1997.9.1 -1998.5.1, so we only have 8 months
    #get 11 users exists in all of following time window

    users0 = filterForUser(datetime.datetime(1997, 9, 1), datetime.datetime(1997, 10, 1), users)
    users1 = filterForUser(datetime.datetime(1997, 10, 1), datetime.datetime(1997, 11, 1), users0)
    users2 = filterForUser(datetime.datetime(1997, 11, 1), datetime.datetime(1997, 12, 1), users1)
    users3 = filterForUser(datetime.datetime(1997, 12, 1), datetime.datetime(1998, 1, 1), users2)
    users4 = filterForUser(datetime.datetime(1998, 1, 1), datetime.datetime(1998, 2, 1), users3)
    users5 = filterForUser(datetime.datetime(1998, 2, 1), datetime.datetime(1998, 3, 1), users4)
    # users6 = filterForUser(datetime.datetime(1997, 9, 1), datetime.datetime(1997, 10, 1), users)
    # users7 = filterForUser(datetime.datetime(1997, 10, 1), datetime.datetime(1997, 11, 1), users0)
    # users8 = filterForUser(datetime.datetime(1997, 11, 1), datetime.datetime(1997, 12, 1), users1)
    # users9 = filterForUser(datetime.datetime(1997, 12, 1), datetime.datetime(1998, 1, 1), users2)
    # users10 = filterForUser(datetime.datetime(1998, 1, 1), datetime.datetime(1998, 2, 1), users3)
    # users11 = filterForUser(datetime.datetime(1998, 2, 1), datetime.datetime(1998, 3, 1), users4)

    # cnt  = 0
    # for i in users:
    #     cnt += 1
    #     if cnt == 413:
    #         print i
    #         break
    # sum = 0
    # for id in users:
    #     sum += len(users[id])
    # print 1.0*sum/11

    tmp = {}
    if wholeUsers:
        targetMatrix = users
    else:
        targetMatrix = users5



    for id in targetMatrix:
        tmp[id] = prefs[id]
    prefs = tmp


    #if user did not rate the movie, then set the rating into zero
    for i in prefs:
        for j in movies:
            prefs[i].setdefault(j, 0)


    matrixForUse = matrix([[prefs[i][j] for j in movies] for i in prefs])
    return matrixForUse


# function used to calculate latent factor, True for whole user, False for 11 users
def getUserLatentFactor(K = 5, wholeUsers = True, overlap = True):

    # get user matrix for each time window
    matrices = []
    for i in range(6):
        matrices.append(matrixDic(i, wholeUsers, overlap))


    # calculate user latent fadtor for each time window
    errors = []
    # storeX = []
    X = []

    matrix_for_use = array(matrices[0])
    model = NMFsimple(n_components=K, init='random', random_state=0)
    # X.append(model.fit_transform(matrix_for_use))
    X.append(model.fit_transform(matrix_for_use)[412])
    C = model.components_


    #250.462450954

    for i in range(1, 6):
        matrix_for_use = array(matrices[i])

        # fix item latent factor C, make user latent factor X to burden all the changes during different time window
        tmp_X, C, times = NMFcomplex(matrix_for_use, X[i-1], C, K, 'custom', False)
        # X.append(tmp_X)
        X.append(tmp_X[412])
        errors.append(ma_error(X[i-1], X[i]))


    #print errow array
    return errors


    #return latent factor array
    # return X
#
# errors1 = getUserLatentFactor(2, wholeUsers=True, overlap=True)
# errors2 = getUserLatentFactor(5, wholeUsers=True, overlap=True)
# errors3 = getUserLatentFactor(10, wholeUsers=True, overlap=True)
# errors4 = getUserLatentFactor(20, wholeUsers=True, overlap=True)
# errors5 = getUserLatentFactor(100, wholeUsers=True, overlap=True)
# plt.plot(errors1, marker='o', color = 'red', label = 'k=2')
# plt.plot(errors2, marker='o', color = 'green', label = 'k=5')
# plt.plot(errors3, marker='o', color = 'blue', label = 'k=10')
# plt.plot(errors4, marker='o', color = 'orange', label = 'k=20')
# plt.plot(errors5, marker='o', color = 'black', label = 'k=100')
# plt.ylabel('error')
# plt.title('max user 650, overlap, mean_absolute_error')
# plt.legend()
# plt.show()

