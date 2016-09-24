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
# then the posterior is corrected to account for the added obstcle area
def predictState2(global_map, local_map, state_prob):
    CONN = 8
    #for local_map...draw obstacles at every location
    temp_global = np.zeros_like(global_map)
    c_idx, labels, stats, centroids = cv2.connectedComponentsWithStats(local_map, CONN)
    for comp in range(1, c_idx):
        stat = stats[comp]
        centroid = centroids[comp]
        #Center of bounding box seems like a better point to place obstacle
        cx = stat[0] + (stat[2]/2)
        cy = stat[1] + (stat[3]/2)
        #cx = centroid[0]
        #cy = centroid[1]
        
        if stat[4] > 3:           
            temp_global = drawObstacle(temp_global, (cx, cy), OBSTACLE_RADIUS, 255)
            state_prob = drawObstacle(state_prob, (cx, cy), OBSTACLE_RADIUS, 0.7)
            
        else:
            state_prob[labels == comp] = 0.7
        saveImagePNG(temp_global, 'temp_global_map.png');
    #saveImagePNG(global_map, 'mm_global_map.png');
    #saveImagePNG(temp_global, 'mm_add_map.png');
    #global_map = np.zeros_like(global_map)
            
    return (temp_global, state_prob)

def getNewCenter(l_x, l_y, g_x, g_y):
    newX = 0
    newY = 0
    dd = 6
    d = ((np.sqrt((l_x-g_x)**2 + (l_y-g_y)**2)) - dd)
    print "dist", d
    if (g_x == l_x and g_y == l_y):
        return (g_x, g_y)
    if (g_x == l_x):
        if (l_y > g_y):
            #move down
            newY = g_y + d
            newX = g_x
        elif (l_y < g_y):
            #move down
            newY = g_y - d
            newX = g_x
            
    elif (g_y == l_y):
        if (l_x > g_x):
            #move down
            newY = g_y
            newX = g_x + d
        elif (l_x < g_x):
            #move down
            newY = g_y
            newX = g_x - d
    else:
        theta = math.atan( (l_y - g_y) / (l_x - g_x) )
        newX = g_x - (d * math.cos(theta))
        newY = g_y - (d * math.sin(theta))
    #print l_x, l_y, g_x, g_y, newX, newY
    return (newX, newY)

def predictState(global_map, local_map, state_prob):
    CONN = 8
    c_l, labels_l, stats_l, centroids_l = cv2.connectedComponentsWithStats(local_map, CONN)
    c_g, labels_g, stats_g, centroids_g = cv2.connectedComponentsWithStats(global_map, CONN)
    
    #clean global map
    global_map = np.zeros_like(global_map) 
    
    #get distance matrix between all centroids
    dist = cdist(centroids_l, centroids_g, 'sqeuclidean')
    #find shortes distance between the local and global obstacle positions 
    tracked = []
    for p in range(1, c_l):      
        if stats_l[p][4] > 3: 
            #print 'c_l_cen' , centroids_l[p][0], centroids_l[p][1]
            #print 'min_dist', min(dist[p])
            best_g = np.argmin(dist[p])
            #print 'best_fit', best_g
            if min(dist[p]) < 25 and best_g > 0: # if newest center is lesser than 9 pixels 
                # adjust center to 6 pixels in direction
                best_g = np.argmin(dist[p])
                tracked.append(best_g)
                
                #Find center of bounding box for the local map obstacle.
                l_x = stats_l[p][0] + (stats_l[p][2]/2)
                l_y = stats_l[p][1] + (stats_l[p][3]/2)
                #(cx, cy) = getNewCenter(l_x, l_y, centroids_g[best_g][0], centroids_g[best_g][1])
                cx = (l_x*2  + centroids_g[best_g][0])/3
                cy = (l_y*2  + centroids_g[best_g][1])/3
                
                #cx = centroids_l[p][0]
                #cy = centroids_l[p][1]
                
                #(cx, cy) = getNewCenter(centroids_l[p][0], centroids_l[p][1], centroids_g[best_g][0], centroids_g[best_g][1])
             
                # add to global map
            else: # must be a new blob
                (cx, cy) = (centroids_l[p][0], centroids_l[p][1])
            #state_prob[labels_l == p] = 0.3 #cut off all other spurious values
            global_map = drawObstacle(global_map, (cx, cy), OBSTACLE_RADIUS, 255)
            state_prob = drawObstacle(state_prob, (cx, cy), OBSTACLE_RADIUS , 0.8)
            state_prob[labels_l == p] = state_prob[labels_l == p] * 0.9
        else:
            #global_map[labels_l == p] = 255
            #state_prob[labels_l == p] = 0.7
            state_prob[labels_l == p] = state_prob[labels_l == p] * 0.9
    
    #there are obstacles in global map that also need to be added
    '''for p in range(1, c_g):
        if p not in tracked:
            (cx, cy) = (centroids_g[p][0], centroids_g[p][1])
            global_map = drawObstacle(global_map, (cx, cy), OBSTACLE_RADIUS, 255)
        #state_prob = drawObstacle(state_prob, (cx, cy), OBSTACLE_RADIUS, 0.7)
        #state_prob[labels_l == p] = 0.7'''
        
        
    return (global_map, state_prob)