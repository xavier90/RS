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


def matrixDic(timeWindowId, Id, overlap = True, path = 'ml-100k'):
    #load movie data
    movies = {}
    for line in open(path + '/u.item'):
        (id, title) = line.split('|')[0:2]
        movies[id] = title

    #load data
    prefs = {}
    users = {} #dictionary to filter user

    #set time interval
    time_interval = []
    if timeWindowId == 0:
        time_interval = [datetime.datetime(1997, 9, 1), datetime.datetime(1997, 10, 1)]
    elif timeWindowId == 1:
        if overlap:
            start = datetime.datetime(1997, 9, 1)
        else:
            start = datetime.datetime(1997, 10, 1)
        time_interval = [start, datetime.datetime(1997, 11, 1)]
    elif timeWindowId == 2:
        if overlap:
            start = datetime.datetime(1997, 9, 1)
        else:
            start = datetime.datetime(1997, 11, 1)
        time_interval = [start, datetime.datetime(1997, 12, 1)]
    elif timeWindowId == 3:
        if overlap:
            start = datetime.datetime(1997, 9, 1)
        else:
            start = datetime.datetime(1997, 12, 1)
        time_interval = [start, datetime.datetime(1998, 1, 1)]
    elif timeWindowId == 4:
        if overlap:
            start = datetime.datetime(1997, 9, 1)
        else:
            start = datetime.datetime(1998, 1, 1)
        time_interval = [start, datetime.datetime(1998, 2, 1)]
    elif timeWindowId == 5:
        if overlap:
            start = datetime.datetime(1997, 9, 1)
        else:
            start = datetime.datetime(1998, 2, 1)
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


    #only keep 922 users
    tmp = {}
    tmp = prefs[Id]
    prefs = tmp
    print prefs

    #if user did not rate the movie, then set the rating into zero
    for movie in movies:
        prefs.setdefault(movie, 0)

    matrixForUse = matrix([prefs[i] for i in prefs])
    print count_nonzero(matrixForUse)
    return matrixForUse

#
# # function used to calculate latent factor, True for whole user, False for 11 users
# def getUserLatentFactor(K = 5, wholeUsers = True, overlap = True):
#
#     # get user matrix for each time window
#     matrices = []
#     for i in range(6):
#         matrices.append(matrixDic(i, wholeUsers, overlap))
#
#
#     # calculate user latent fadtor for each time window
#     errors = []
#     # storeX = []
#     X = []
#
#     matrix_for_use = array(matrices[0])
#     model = NMFsimple(n_components=K, init='random', random_state=0)
#     X.append(model.fit_transform(matrix_for_use))
#     C = model.components_
#
#
#     #250.462450954
#
#     for i in range(1, 6):
#         matrix_for_use = array(matrices[i])
#
#         # fix item latent factor C, make user latent factor X to burden all the changes during different time window
#         tmp_X, C, times = NMFcomplex(matrix_for_use, X[i-1], C, K, 'custom', False)
#         X.append(tmp_X)
#         errors.append(ma_error(X[i-1], X[i]))
#
#
#     # result of error for whole users between two time window is following
#     #[0.65273390415311039, 1.3207501956476182, 1.3720867499619522, 0.91827877221896337, 0.87801555325471625]
#
#     # result of error for 11 users between two time window is following
#     #[0.52588900833510677, 0.01619487118296753, 0.0028863264666930876, 0.0010539344593993851, 0.0022620676048250073]
#
#     #print errow array
#     return errors
#
#
#     #return latent factor array
#     # return X
#
# errors1 = getUserLatentFactor(2, wholeUsers=False, overlap=True)
# errors2 = getUserLatentFactor(5, wholeUsers=False, overlap=True)
# errors3 = getUserLatentFactor(10, wholeUsers=False, overlap=True)
# # errors4 = getUserLatentFactor(20, wholeUsers=False, overlap=False)
# # errors5 = getUserLatentFactor(100, wholeUsers=False, overlap=False)
# plt.plot(errors1, marker='o', color = 'red', label = 'k=2')
# plt.plot(errors2, marker='o', color = 'green', label = 'k=5')
# plt.plot(errors3, marker='o', color = 'blue', label = 'k=10')
# # plt.plot(errors4, marker='o', color = 'orange', label = 'k=20')
# # plt.plot(errors5, marker='o', color = 'black', label = 'k=100')
# plt.ylabel('error')
# plt.title('11 users, overlap, mean_absolute_error')
# plt.legend()
# plt.show()

matrix = matrixDic(0, Id='860')
