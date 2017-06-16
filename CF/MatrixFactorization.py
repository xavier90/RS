from numpy import *

def costFuc(a, b):
    #calculate euclidean distance between a and b
    # diff = sum(asarray(a-b)**2)
    diff = 0
    for i in range(shape(a)[0]):
        for j in range(shape(a)[1]):
            if a.item((i, j)) > 0:
                diff += (a.item((i, j)) - b.item((i, j))) ** 2

    return sqrt(diff)

#use Multiplicative update rules
def factorizeMUR(v, k = 10, iter = 500):
    n = shape(v)[0]
    m = shape(v)[1]

    #initialize the weight and feature matrices with random values
    w = matrix([[random.random() for i in range(k)] for i in range(n)])
    h = matrix([[random.random() for i in range(m)] for i in range(k)])

    #perform operation a maximum of iter times
    for i in range(iter):
        wh = w*h

        #calculate the current difference
        cost = costFuc(v, wh)
        if i % 10 == 0: print cost

        #terminate if the matrix has been fully factorized
        if cost < 0.0001: break

        #update feature matrix
        hn = w.T * v
        hd = w.T * w * h
        h = matrix(array(h) * array(hn) / array(hd))

        #update weight matrix
        wn = v * h.T
        wd = w * h * h.T
        w = matrix(array(w) * array(wn) / array(wd))

    return w, h


# m = MatrixForUse.matrixDic()
# w, h = factorizeMUR(m)
# print w
# print h
#
# print w*h

# f = open('E:/cs/CF/ml-100k/result.txt','w')
# for i in range(0, shape(m)[0]):
#     for j in range(0, shape(m)[1]):
#         f.write(str(m.item((i,j))))
#     f.write('\n')
# f.close()

w = matrix([[5, 3, 0, 1], [4, 0, 0, 1], [1, 1, 0, 5], [2, 1, 5, 4]])
w, h = factorizeMUR(w, 4,500)
# print w
# print h
print around(w*h)