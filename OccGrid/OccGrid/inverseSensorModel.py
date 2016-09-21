import numpy as np

def normalize(a):
    d = a[0,0] + a[0,1]
    a /= d
    return a

#function to update state probabilities (prior) of the cell with observation z of laser scan.
#State Transition model A
def updateState(prior, A, z, log_odd):
    prior_trans = prior.dot(A)
    prior_trans = normalize(prior_trans)
    log_odd = log_odd + np.log(p_occ[z]) - np.log(1 - p_occ[z]) + np.log(1 - prior_trans[0, 1]) - np.log(prior_trans[0, 1])
    prior[0, 0] = 1 - (1 / (1 + np.exp(log_odd)))
    prior[0, 1] = 1 - prior[0, 0]
    print prior
    return (log_odd, prior)

obs = ['hit', 'miss', 'hit', 'hit', 'nobs', 'nobs', 'nobs', 'nobs', 'nobs', 'nobs', 'nobs', 'nobs']

A = np.zeros((2,2))
A[0, 0] = 0.3
A[0, 1] = 0.7
A[1, 0] = 0.4
A[1, 1] = 0.6

prior = np.zeros((1,2))
prior[0,0] = 0.3
prior[0,1] = 0.7

#Dictionary of Inverse Sensor Model
p_occ = {}
p_occ['hit'] = 0.999
p_occ['miss'] = 0.001
p_occ['nobs']  = 0.4

log_odd = 0;
for z in obs:
    log_odd, prior = step(z, log_odd, prior, A)

prior.dot(A)
prior
prior.shape
prior[0,1]

