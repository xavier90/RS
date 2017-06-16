from numpy import *
import CF.MatrixForUse

def matrix_factorization(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
    Q = Q.T
    for step in xrange(steps):
        for i in xrange(shape(R)[0]):
            for j in xrange(shape(R)[1]):

                if R[i, j] > 0:
                    eij = R[i, j] - dot(P[i,:],Q[:,j])
                    for k in xrange(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        eR = dot(P,Q)
        e = 0
        for i in xrange(shape(R)[0]):
            for j in xrange(shape(R)[1]):
                if R[i, j] > 0:
                    e = e + pow(R[i, j] - dot(P[i,:],Q[:,j]), 2)
                    for k in xrange(K):
                        e = e + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))
        if e < 0.001:
            break
        if step % 5 == 0:
            print e
    return P, Q.T

# R = MatrixForUse.matrixDic()
# R = [[5, 3, 0, 1], [4, 0, 0, 1], [1, 1, 0, 5], [2, 1, 5, 4]]
#
# R = numpy.array(R)
#
# N = len(R)
# M = len(R[0])
# K = 2
#
# P = numpy.random.rand(N,K)
# Q = numpy.random.rand(M,K)
#
# nP, nQ = matrix_factorization(R, P, Q, K)
# nR = numpy.dot(nP, nQ.T)
# print R
# print numpy.around(nR)
