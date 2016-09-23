import cv2
import numpy as np
from utility import *

OBSTACLE_RADIUS = 6

#function to draw a circle (obstacle) on state map and state probability
#State map is unit8, but state prob is float
def drawObstacle(img, (x, y), r, value):
    cv2.circle(img, (int(x), int(y)), r, (value), -1)
    return img

# function to add obstcles to the global state
# First a state is predicted on basis of the posterior
# then the posterior is corrected to account for the added obstcle area
def predictState(state_map, state_prob):
    CONN = 8
    c_idx, labels, stats, centroids = cv2.connectedComponentsWithStats(state_map, CONN)
    
    #cleanup   
    #saveImagePNG(state_prob*255, 'prob_before_circle.png');
    state_prob_new = state_prob.copy()
    state_prob_new[state_prob_new > 0.5] = 0.3;    
    state_map[state_map == 1] = 0;   
    
    #for each centroid (not background), create an obstacle
    
    #print "probmax" + str(np.amax(state_prob))
    
    #first component is the background..ignore that
    for comp in range(1, c_idx):
        stat = stats[comp]
        centroid = centroids[comp]
        #do this only if area of obstacle is > 4
    
        #Center of bounding box seems like a better point to place obstacle
        #cx = stat[0] + (stat[2]/2)
        #cy = stat[1] + (stat[3]/2)
        cx = centroid[0]
        cy = centroid[1]
        #Pick the probability of the centroid. This becomes prior for all pixels belonging to the obstacle now
        #print centroid        
        '''obs_prob = max(state_prob[np.ceil(centroid[1]) ][np.ceil(centroid[0]) ], 
                       state_prob[np.ceil(centroid[1]) ][np.floor(centroid[0]) ],
                       state_prob[np.floor(centroid[1]) ][np.ceil(centroid[0]) ],
                       state_prob[np.floor(centroid[1]) ][np.floor(centroid[0]) ]);#indexed [y][x]'''
                     
        obs_prob = np.amax(state_prob[stat[2]:stat[2] + stat[4], stat[1]:stat[1] + stat[3]])
        
        if obs_prob < 0.5:
            print state_prob[stat[1]:stat[1] + stat[3], stat[2]:stat[2] + stat[4]]
            print str(obs_prob) + " here"
        state_map = drawObstacle(state_map, (cx, cy), OBSTACLE_RADIUS, 255)
        state_prob_new = drawObstacle(state_prob_new, (cx, cy), OBSTACLE_RADIUS, 0.8)
        
        saveImagePNG(state_prob*255, 'prob_after_circle.png');
            
    return (state_map, state_prob_new)
