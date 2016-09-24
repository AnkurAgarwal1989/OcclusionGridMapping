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
    p_occ[Observation.HIT] = 0.9999
    p_occ[Observation.MISS] = 0.0001
    p_occ[Observation.NO_OBS]  = 0.15
    
    
    #variable to hold log_odds
    log_odds = 0;

    def __init__(self):
        #initialize a cell with a high probability of being empty
        self.state_curr = State.EMPTY
        self.prior[0,0] = 0.7   #occlusion
        self.prior[0,1] = 0.3   #empty
        
        #Dynamic Environment
        self.A[0, 0] = 0.7
        self.A[0, 1] = 0.3
        self.A[1, 0] = 0.2
        self.A[1, 1] = 0.8
        
        '''self.A[0, 0] = 1
        self.A[0, 1] = 0
        self.A[1, 0] = 0
        self.A[1, 1] = 1'''
    #set cell prior to occlusion probability after state map correction
    def setPrior(self, p_occ):
        self.prior[0, 0] = p_occ
        self.prior[0, 1] = 1 - p_occ
        self.log_odds = np.log(p_occ) - np.log(1 - p_occ)
        
    def getPrior(self):
        return self.prior[0, 0]
 
    #function to update state probabilities (prior) of the cell with observation z of laser scan.
    def updateCellState(self, z):
        
        prior_trans = self.prior.dot(self.A)
        prior_trans = normalize_1d(prior_trans)
        self.log_odds = np.log(self.p_occ[z]) - np.log(1 - self.p_occ[z]) + np.log(1 - prior_trans[0, 0]) - np.log(prior_trans[0, 0])
        self.posterior[0, 0] = 1 - (1 / (1 + np.exp(self.log_odds)))
        self.posterior[0, 1] = 1 - self.posterior[0, 0]
        
        #some counting maybe???
        
        self.prior = self.posterior.copy()
        '''if z == Observation.HIT:
            self.prior[0, 0] = 0.8
            self.prior[0, 1] = 1 - 0.8
        
        elif z == Observation.MISS:
            self.prior[0, 0] = 0.2
            self.prior[0, 1] = 1 - 0.2
        elif z == Observation.NO_OBS:
            print "WTF"'''
    
    def printStateMatrix(self):
        print self.Q_curr;    
    
    '''def getState(self):
        if (self.prior[0, 0] > 0.5):
            return State.OCC
        return State.EMPTY'''
        
    def __repr__(self):
        return self.getState()
