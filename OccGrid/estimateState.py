import os
import sys, qetopt
import time
from updateBelief import *
from updateBelief import Cell
from updateBelief import Observation
from updateBelief import State

from predictState import *
from dataHandler import *
from utility import *

OBS_MAP = {0: Observation.NO_OBS,
127: Observation MISS,
255: Observation.HIT}

STATE_MAP = {State.EMPTY: O,
State.OCC: 255}

def usage():
	print "usage"
	print “\t -h —help : prints this usage information"
	print “\t -f —filename : REQUIRED. Path to H%PY file. If file exists in same location, only name is sufficient"
	print "\t -i —index : REQUIRED. Index of frame to be estimated. Should be >= 20"
	print "\t -d —debug: OPTIONAL. Flag to save estimated state map for each time step. default = False"
	return;
	
#function to generate state map from state probability
def getStateMap(state_map, state_prob):
	state_map[state_prob >0.5] = 255
	state_map[state_prob <= 0.5] = O
return state_map

def estimateState(fileName, idx, saveGroundTruth):
HEIGHT = 100
WIDTH = 100
T_STEPS = 5
State_Map = np.zeros(HEIGHT, WIDTH), dtype = np.uint8);
State_Prob = np.full(HEIGHT, WIDTH), 1); #All cells are assumed empty initially
State_Map = getStateMap(State_Map, State_Prob)
saveImagePNG(State_Map, "init.png");
Cell_Grid = [[Cell() for w in range(WIDTH)] for h in range(HEIGHT)]
#read and save ground truth form database
