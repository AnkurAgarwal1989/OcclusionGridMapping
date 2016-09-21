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

# Dictionary to hold observation matrices. for ease of usage
B_z = {observation : np.zeros( (len(States), len(States)) ) for observation in Observations}
#Noiseless setting...This can be updated for noisy sensors
B_z[Observation.HIT][0, 0] = 1;
B_z[Observation.MISS][1, 1] = 1;

#used for updates in a dynamic world HMM
B_z[Observation.NO_OBS][0, 0] = 0;
B_z[Observation.NO_OBS][0, 1] = 1;
B_z[Observation.NO_OBS][1, 0] = 1;
B_z[Observation.NO_OBS][1,1] = 0;

#class to hold data for the cell.
class Cell:
    ###current state info
    #Name of current state
    state_curr = None
    #Cell state matrix, holds probability
    Q_curr = np.empty( (1, len(States)) )
    
    ###next state info
    #Name of next state
    state_next = None
    #Cell state matrix, holds probability
    Q_next = np.empty( (1, len(States)) )

    #transition matrix. Initially is zero
    A = np.zeros( (len(States), len(States)) );
    ##[ p(occ|occ)      p(free|occ)
    ##  p(occ|free)     p(free|free)]
    ##

    def __init__(self):
        self.state_curr = State.OCC
        self.Q_curr[0, 0] = 1  #init all states to occupied
        #Static Environment
        self.A[0,0] = 0.6
        self.A[0,1] = 0.4
        self.A[1,1] = 0.8
        self.A[1,0] = 0.2

    def set_A(self, A_next):
        print "Setting A"
        self.A = A_next.copy()
            
    def get_A(self):
        print "Getting A"
        return self.A

    #Function to estimate and update A
    #we maintain a dicitonary of values for each cell, update those and recalculate A at every time step 
    def update_A(self):
        print "Updating A"
        #set_A(self.A)

    
    #Perform a belief update on the cell given an Observation()
    def step(self, obs):
        #Qt+1 = Qt * A * B(h)
        #p1 = self.Q_curr.dot( self.A)
        #p2 = p1.dot(B_z[obs] )
        self.Q_next = self.Q_curr.dot( self.A ).dot( B_z[obs] )
        #self.Q_next = p2.copy();
        norm = self.Q_next[0, 0] + self.Q_next[0, 1];
        self.Q_next /= max(norm, epsilon);       
        self.Q_curr = self.Q_next.copy()

    def normalize(self):
        print "Normalizing"

    
    def printStateMatrix(self):
        print self.Q_curr;    
    
    def getState(self):
        if (self.Q_curr[0, 0] > 0.5):
            return State.OCC
        return State.EMPTY

    def __repr__(self):
        return self.getState()
