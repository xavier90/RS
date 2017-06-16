from math import sqrt

#make dataset into a dictionary
def prefsDic(path = '/Users/yaojianwang/Documents/CF/ml-100k'):
    #Get movie titles
    movies = {}
    for line in open(path + '/u.item'):
        (id, title) = line.split('|')[0:2]
        movies[id] = title

    #Load data
    prefs = {}
    for line in open(path + '/u.data'):
        (userId, itemId, rating, timeStamp) = line.split('\t')
        prefs.setdefault(userId, {})
        prefs[userId][movies[itemId]] = float(rating)
    return prefs


#calculate user-based pearson correlation coefficient
def pearsonCC(prefs, p1, p2):
    #Get the list of mutually rated items
    mutual = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            mutual[item] = 1

    #the number of elements of mutually rated items
    n = len(mutual)

    #if there are no ratings in common, return 0
    if n == 0: return 0

    #add up all the preferences
    sum1 = sum([prefs[p1][it] for it in mutual])
    sum2 = sum([prefs[p2][it] for it in mutual])


    #add up the squares
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in mutual])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in mutual])

    #sum up the products
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in mutual])

    #calculate pearson score
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1,2)/n) * (sum2Sq - pow(sum2,2)/n))
    if den == 0: return 0

    return num/den


#return the best matches for person from the prefs dictionary
def topMatches(prefs, person, n = 10, similarity = pearsonCC):
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]

    #sort the list so the highest sores appear at the top
    scores.sort()
    scores.reverse()
    return scores[0:n]

print topMatches(prefsDic(), '1')
