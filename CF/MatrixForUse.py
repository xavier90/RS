from numpy import *


def matrixDic(path = '/Users/yaojianwang/Documents/CF/ml-100k'):
    #load movie data
    movies = {}
    for line in open(path + '/u.item'):
        (id, title) = line.split('|')[0:2]
        movies[id] = title

    #load data
    prefs = {}
    for line in open(path + '/u.data'):
        (userId, itemId, rating, timeStamp) = line.split('\t')
        prefs.setdefault(userId,{})
        prefs[userId][itemId] = float(rating)

    #if user did not rate the movie, then set the rating into zero
    for i in prefs:
        for j in movies:
            prefs[i].setdefault(j, 0)

    #make a matrix with userId in row and moveTitle in column
    #if user does not vote the movie, the value should be ?

    matrixForUse = matrix([[prefs[i][j] for j in movies] for i in prefs])
    return matrixForUse