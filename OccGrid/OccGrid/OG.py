import numpy as np

# Class to hold different types of observations
class Observation:
    NO_OBS = "no_obs"   #0
    MISS = "miss"       #127
    HIT = "hit"         #255
    
class State:
    EMPTY = "empty"     #0
    OCC = "occupied"    #255

States = [State.OCC, State.EMPTY];
Observations = [Observation.HIT, Observation.MISS, Observation.NO_OBS]
epsilon = 0.00001

def normalize_1d(a):
    d = a[0,0] + a[0,1]
    a /= max(d, epsilon)
    return a

#class to hold data for the cell.
class Cell:
    ###current state info
    #Cell state matrix, holds probability
    prior = np.zeros( (1,len(States)) )
    
    ###next state info
    #Cell state matrix, holds probability
    posterior = np.empty( (1, len(States)) )

    #transition matrix. Initially is zero
    A = np.zeros( (len(States), len(States)) );
    ##[ p(occ|occ)      p(free|occ)
    ##  p(occ|free)     p(free|free)]
    ##
    
    #Dictionary of Inverse Sensor Model
    p_occ = {}
    p_occ['hit'] = 0.999
    p_occ['miss'] = 0.001
    p_occ['nobs']  = 0.4
    
    #variable to hold log_odds
    log_odds = 0;

    def __init__(self):
        #initialize a cell with a high probability of being empty
        self.state_curr = State.EMPTY
        self.prior[0,0] = 0.3   #occlusion
        self.prior[0,1] = 0.7   #empty
        
        #Dynamic Environment
        A[0, 0] = 0.3
        A[0, 1] = 0.7
        A[1, 0] = 0.4
        A[1, 1] = 0.6
 
    #function to update state probabilities (prior) of the cell with observation z of laser scan.
    def updateState(self, z):
        prior_trans = self.prior.dot(self.A)
        prior_trans = normalize_1d(prior_trans)
        self.log_odd = self.log_odd + np.log(self.p_occ[z]) - np.log(1 - self.p_occ[z]) + np.log(1 - prior_trans[0, 1]) - np.log(prior_trans[0, 1])
        self.posterior[0, 0] = 1 - (1 / (1 + np.exp(log_odd)))
        self.posterior[0, 1] = 1 - self.posterior[0, 0]
        
        #some counting maybe???
        
        prior = posterior.copy()
    
    def printStateMatrix(self):
        print self.Q_curr;    
    
    def getState(self):
        if (self.prior[0, 0] > 0.5):
            return State.OCC
        return State.EMPTY
        
    def __repr__(self):
        return self.getState()
