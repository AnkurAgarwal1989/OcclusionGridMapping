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

def estimateState(fileName, idx, debug):
    HEIGHT = 100
    WIDTH = 100
    T_STEPS = 20
    Global_State_Map = np.full((HEIGHT, WIDTH), 255, dtype = np.uint8);
    State_Prob = np.full((HEIGHT, WIDTH), 0.3); #All cells are assumed empty initially
    #State_Map = getStateMap(State_Map, State_Prob)
    
    Cell_Grid = [[Cell() for w in range(WIDTH)] for h in range(HEIGHT)]
    
    #read and save ground truth form database
    
    #Gnd_Truth = getData(fileName, 'ground_truth', idx);
    #savelmagePNG(Gnd_Truth[:, :, 0], 'GT_' + str(idx) + '.png');
    Gnd_Truth = getData(fileName, 'ground_truth', idx - T_STEPS + 1, T_STEPS);
    
    #read laser scan data form database
    Laser_Scans = getData(fileName, 'occupancy', idx - T_STEPS + 1, T_STEPS);
    startTime = time.time();
    for t in range( 0, T_STEPS):
        State_Map = np.zeros((HEIGHT, WIDTH), dtype = np.uint8);
        State_Prob = np.full((HEIGHT, WIDTH), 0.3);
        for y in range( HEIGHT):
            for x in range( WIDTH):
                obs = Laser_Scans[y, x, t]
                Cell_Grid[y][x].setPrior(State_Prob[y][x])
                if obs > -1:
                    Cell_Grid[y][x].updateCellState(OBS_MAP[obs])
                    State_Prob[y][x] = Cell_Grid[y][x].getPrior()
        #print State_Prob
                    
        State_Map = getStateMap(State_Map, State_Prob)
        #saveImagePNG(State_Prob*255, str(t + idx)+'_prob_1.png');
        #saveImagePNG(State_Map, str(t + idx)+ 'local_map.png');
        
        #saveImagePNG(Global_State_Map, str(t + idx)+'before_global_map.png');
        Global_State_Map, State_Prob = predictState(Global_State_Map, State_Map, State_Prob)
        #saveImagePNG(State_Prob*255, str(t + idx) +'_prob_2.png');
        #saveImagePNG(Global_State_Map, str(t + idx)+'after_global_map.png');

        '''if debug:
            saveImagePNG(Gnd_Truth[:, :, t], str(t + idx)+'_GT.png');
            #saveImagePNG(State_Map, 'est_map_'+str(t + idx)+'.png');
            compareWithGroundTruth(Gnd_Truth[:, :, t], Global_State_Map, str(t + idx) + '_diff.png')
            saveImagePNG(Laser_Scans[:, :, t], str(t + idx)+ '_scan.png');'''
    print "Total time taken %s seconds" % ((time.time() - startTime));
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

