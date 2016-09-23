import os
import sys, getopt
import time
from updateBelief import *
from updateBelief import Cell
from updateBelief import Observation
from updateBelief import State

from predictState import *
from H5PYHandler import *
from utility import *

OBS_MAP = {0: Observation.NO_OBS,
127: Observation.MISS,
255: Observation.HIT}

STATE_MAP = {State.EMPTY: 0,
State.OCC: 255}

def usage():
    print "usage"
    print "\t -h —help : prints this usage information"
    print "\t -f —filename : REQUIRED. Path to H5PY file. If file exists in same location, only name is sufficient"
    print "\t -i —index : REQUIRED. Index of frame to be estimated. Should be >= 20"
    print "\t -d —debug: OPTIONAL. Flag to save estimated state map for each time step. default = False"
    return;
    
#function to generate state map from state probability
def getStateMap(state_map, state_prob):
    state_map[state_prob > 0.5] = 255
    state_map[state_prob <= 0.5] = 0
    return state_map

def estimateState(fileName, idx, debug):
    HEIGHT = 100
    WIDTH = 100
    T_STEPS = 20
    State_Map = np.zeros((HEIGHT, WIDTH), dtype = np.uint8);
    State_Prob = np.full((HEIGHT, WIDTH), 1); #All cells are assumed empty initially
    State_Map = getStateMap(State_Map, State_Prob)
    saveImagePNG(State_Map, "init.png");
    Cell_Grid = [[Cell() for w in range(WIDTH)] for h in range(HEIGHT)]
    
    #read and save ground truth form database
    
    #Gnd_Truth = getData(fileName, 'ground_truth', idx);
    #savelmagePNG(Gnd_Truth[:, :, 0], 'GT_' + str(idx) + '.png');
    Gnd_Truth = getData(fileName, 'ground_truth', idx - T_STEPS + 1, T_STEPS);
    
    #read laser scan data form database
    Laser_Scans = getData(fileName, 'occupancy', idx - T_STEPS + 1, T_STEPS);
    
    for t in range( 0, T_STEPS):
        for y in range( HEIGHT):
            for x in range( WIDTH):
                obs = Laser_Scans [y, x, t]
                Cell_Grid[y][x].setPrior(State_Prob[y][x])
                if obs >0:
                    Cell_Grid[y][x].updateCellState(OBS_MAP[obs])
                    State_Prob[y][x] = Cell_Grid[y][x].getPrior()
                    
        State_Map = getStateMap(State_Map, State_Prob)
        saveImagePNG(State_Prob*255, 'prob_1'+str(t + idx)+'.png');
        saveImagePNG(State_Map, 'temp_est_map'+str(t + idx)+ '.png');
        State_Map, State_Prob = predictState(State_Map, State_Prob)
        saveImagePNG(State_Prob*255, 'prob_2' +str(t + idx) +'.png');
    
        if debug:
            saveImagePNG(Gnd_Truth[:, :, t], 'GT'+str(t + idx)+'.png');
            saveImagePNG(State_Map, 'est_map_'+str(t + idx)+'.png');
            compareWithGroundTruth(Gnd_Truth[:, :, t], State_Map, 'diff'+str(t + idx)+'.png')
            saveImagePNG(Laser_Scans[:, :, t], 'scan_' + str(t + idx)+ '.png');
            
    #error = compareWithGroundTruth(Gnd_Truth[:, :, t], State_Map)
    return error

#Entry function
def main(argv):

    startTime = time.time();
    fileName = None;
    idx = 0;
    saveDebugImages = False;
    
    try:
        opts, args = getopt.getopt(argv, 'hf:i:d', ["help","filename = ", "index = "]);
        if not opts:
            print "No options supplied"
            usage();
            sys.exit();
    except getopt.GetoptError:
        usage();
        sys.exit(2);
        
    for opt, arg in opts:
        if opt in ("-h", "-—help"):
            usage();
            sys.exit();
    
    for opt, arg in opts:
        if opt in ("-f", "--filename"):
            fileName = arg;
        elif opt in ("-i", "--index"):
            idx = int(arg);
            if idx <20:
                print "The index needs to be >= 20."
                usage();
                sys.exit();
        elif opt == "-d":
            saveDebugImages = True;
    
    if fileName is None or idx == 0:
        print "Required arguments missing"
        usage();
        sys.exit();
    
    estimateState(fileName, idx, saveDebugImages)
    print "Total time taken %s minutes" % ((time.time() - startTime)/60);
    
if __name__ == "__main__":
    main(sys.argv[1:])

