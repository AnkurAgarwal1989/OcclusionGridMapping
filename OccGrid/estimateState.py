import os
import sys, getopt
import time

import numpy as np

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
    print "\t -h help : prints this usage information"
    print "\t -f filename : REQUIRED. Path to H5PY file. If file exists in same location, only name is sufficient"
    print "\t -i index : REQUIRED. Index of frame to be estimated. Should be >= 20"
    print "\t -d debug: OPTIONAL. Flag to save estimated state map for each time step. default = False"
    return;
    
#function to generate state map from state probability
def getStateMap(state_map, state_prob):
    state_map[state_prob > 0.5] = 255
    #state_map[state_map == 0 and state_prob <= 0.5] = 0
    state_map[state_prob <= 0.5] = 0
    return state_map

def estimateState(fileName, idx, DEBUG):
    HEIGHT = 100
    WIDTH = 100
    T_STEPS = 20
    State_Map = np.full((HEIGHT, WIDTH), 0, dtype = np.uint8);
    Global_State_Map = np.zeros_like(State_Map)
    State_Prob = np.full((HEIGHT, WIDTH), 0.3); #All cells are assumed empty initially
    State_Map = getStateMap(State_Map, State_Prob)
    
    Cell_Grid = [[Cell() for w in range(WIDTH)] for h in range(HEIGHT)]
    
    begin_idx = idx - T_STEPS + 1
    goodData, Gnd_Truth, Laser_Scans = getData(fileName, begin_idx, T_STEPS);
    if not goodData:
        print "Error reading Data"
        return -1
        
    startTime = time.time();
    for t in range( 0, T_STEPS):
        saveImagePNG(State_Prob * 255, str(begin_idx + t) +'_prob_B_before.png');
        for y in range( HEIGHT):
            for x in range( WIDTH):
                obs = Laser_Scans[y, x, t]
                Cell_Grid[y][x].setPrior(State_Prob[y][x])
                if obs > 0:
                    Cell_Grid[y][x].updateCellState(OBS_MAP[obs])
                    State_Prob[y][x] = Cell_Grid[y][x].getPrior()
                    
        State_Map = getStateMap(State_Map, State_Prob)
        
        if DEBUG:
            saveImagePNG(Laser_Scans[:, :, t], str(begin_idx + t)+ '_scan.png');
            saveImagePNG(State_Prob*255, str(begin_idx + t)+'_prob_A.png');
            saveImagePNG(State_Map, str(begin_idx + t)+ '_local_map.png');
        
        Global_State_Map, State_Prob = predictState(Global_State_Map, State_Map, State_Prob)
        
        if DEBUG:
            saveImagePNG(State_Prob*255, str(begin_idx + t) +'_prob_B.png');
            saveImagePNG(Global_State_Map, str(begin_idx + t)+'_corrected_map.png');
            saveImagePNG(Gnd_Truth[:, :, t], str(begin_idx + t)+'_GT.png');
            compareWithGroundTruth(Gnd_Truth[:, :, t], Global_State_Map, str(begin_idx + t) + '_diff.png')
    
    print "Time taken %s seconds" % ((time.time() - startTime));
    diff_file_name = os.path.join(os.getcwd(), "diff.png") 
    print "Difference image saved as "+ diff_file_name
    print "Green areas are Ground Truth. Red is Estimate"
    error = compareWithGroundTruth(Gnd_Truth[:, :, t], Global_State_Map, diff_file_name)
    print "Squared pixel value error: " + str(error)
    return error

#Entry function
def main(argv):

    
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
        if opt in ("-h", "help"):
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
    
if __name__ == "__main__":
    main(sys.argv[1:])

