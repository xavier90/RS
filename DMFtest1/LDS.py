from numpy import *
import PrepareUserLatentFactor
from pykalman import KalmanFilter

# user latent factors for all time window
X = PrepareUserLatentFactor.getUserLatentFactor(5)

A = random.rand(5, 5)

X1hat = dot(X[0], A)

kf = KalmanFilter(transition_matrices=X1hat, observation_matrices=X[1])
measurements = asarray([[1, 0], [0, 0], [0, 1]])
kf = kf.em(measurements, n_iter=5)

