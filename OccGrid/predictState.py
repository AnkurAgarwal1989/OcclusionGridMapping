import cv2
import numpy as np
from utility import *
from scipy.spatial.distance import cdist
import math

OBSTACLE_RADIUS = 6

#function to draw a circle (obstacle) on state map and state probability
#State map is unit8, but state prob is float
def drawObstacle(img, (x, y), r, value):
    cv2.circle(img, (int(x), int(y)), r, (value), -1)
    return img

# function to add obstcles to the global state
# First a state is predicted on basis of the posterior
# Then we find the closest obstacle in the global map amd move that to a new position between the 2. 
# then the posterior is corrected to account for the added obstacle area
def predictState(global_map, local_map, state_prob):
    CONN = 8
    c_l, labels_l, stats_l, centroids_l = cv2.connectedComponentsWithStats(local_map, CONN)
    c_g, labels_g, stats_g, centroids_g = cv2.connectedComponentsWithStats(global_map, CONN)
    
    #clean global map
    # we will be drawing on this
    global_map = np.zeros_like(global_map) 
    
    #get distance matrix between all centroids
    dist = cdist(centroids_l, centroids_g, 'sqeuclidean')
    #find shortest distance between the local and global obstacle positions 
    
    tracked = []
    for p in range(1, c_l):
        #minimum size of component to be considered
        if stats_l[p][4] > 3: 
            best_g = np.argmin(dist[p])
            
            #find closest obstacle in global map within a certain range (heuristic)
            if min(dist[p]) < 25 and best_g > 0: 
                best_g = np.argmin(dist[p])
                tracked.append(best_g)
                
                #Find center of bounding box for the local map obstacle.
                l_x = stats_l[p][0] + (stats_l[p][2]/2)
                l_y = stats_l[p][1] + (stats_l[p][3]/2)
                
                cx = (l_x * 2  + centroids_g[best_g][0])/3
                cy = (l_y * 2  + centroids_g[best_g][1])/3
                
            else: # must be a new blob
                (cx, cy) = (centroids_l[p][0], centroids_l[p][1])
                
            state_prob[labels_l == p] = 0.3 #cut off all other spurious values
            global_map = drawObstacle(global_map, (cx, cy), OBSTACLE_RADIUS, 255)
            state_prob = drawObstacle(state_prob, (cx, cy), OBSTACLE_RADIUS + 1, 0.8)
            state_prob[labels_l == p] = state_prob[labels_l == p] * 0.9
            
        else:
            state_prob[labels_l == p] = state_prob[labels_l == p] * 0.9
        
    return (global_map, state_prob)