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
    c_idx, labels, stats, centroids = cv2.connectedComponentsWithStats(local_map, CONN)
    for comp in range(1, c_idx):
        stat = stats[comp]
        #Center of bounding box seems like a better point to place obstacle
        cx = stat[0] + (stat[2]/2)
        cy = stat[1] + (stat[3]/2)
        #cx = centroid[0]
        #cy = centroid[1]
        
        if stat[4] > 2:           
            local_map = drawObstacle(local_map, (cx, cy), OBSTACLE_RADIUS, 255)
            saveImagePNG(local_map, 'local_map.png');
    
    #intersect local map with global map
    temp_global = np.zeros_like(global_map)
    temp_global[(global_map == 255) & (local_map == 255) ] = 255
    #temp_global = global_map + local_map
    saveImagePNG(local_map, 'mm_local_map.png');
    saveImagePNG(global_map, 'mm_global_map.png');
    saveImagePNG(temp_global, 'mm_add_map.png');
    global_map = np.zeros_like(global_map)
    
    state_prob = np.full((HEIGHT, WIDTH), 0.3);
    #redraw obstacles in global map...This is the final estimated state
    c_idx, labels, stats, centroids = cv2.connectedComponentsWithStats(temp_global, CONN)
    for comp in range(1, c_idx):
        stat = stats[comp]
        #Center of bounding box seems like a better point to place obstacle
        #cx = stat[0] + (stat[2]/2)
        #cy = stat[1] + (stat[3]/2)
        centroid = centroids[comp]
        cx = centroid[0]
        cy = centroid[1]
        
        if stat[4] > 2:           
            global_map = drawObstacle(global_map, (cx, cy), OBSTACLE_RADIUS, 255)
            state_prob = drawObstacle(state_prob, (cx, cy), OBSTACLE_RADIUS, 0.7)
            saveImagePNG(global_map, 'global_map.png');
            
    return (global_map, state_prob)

def getNewCenter(l_x, l_y, g_x, g_y):
    newX = 0
    newY = 0
    d = 6 - (np.sqrt((l_x-g_x)**2 + (l_y-g_y)**2))
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
        newX = g_x + d * math.cos(theta)
        newY = g_y + d * math.sin(theta)
        print l_x, l_y, g_x, g_y, newX, newY
    return (newX, newY)

def predictState(global_map, local_map, state_prob):
    c_l, labels_l, stats_l, centroids_l = cv2.connectedComponentsWithStats(local_map, 4)
    c_g, labels_g, stats_g, centroids_g = cv2.connectedComponentsWithStats(global_map, 4)
    print "Predicting"
    #clean global map
    print "centroids"
    print centroids_g
    print centroids_l
    global_map = np.zeros_like(global_map)    
    
    #get distance matrix between all centroids
    dist = cdist(centroids_l, centroids_g, 'sqeuclidean')
    #find shortes distance between the local and global obstacle positions
    print c_l    
    for p in range(1, c_l):        
        if stats_l[p][4] > 2:  
            print min(dist[p])
            if min(dist[p]) < 15: # if newest center is lesser than 9 pixels 
                # adjust center to 6 pixels in direction
                best_g = np.argmin(dist[p])
                (cx, cy) = getNewCenter(centroids_l[p][0], centroids_l[p][1], centroids_g[best_g][0], centroids_g[best_g][1])
             
                # add to global map
            else: # must be a new blob
                (cx, cy) = (centroids_l[p][0], centroids_l[p][1])
                
            global_map = drawObstacle(global_map, (cx, cy), OBSTACLE_RADIUS, 255)
            #state_prob = drawObstacle(state_prob, (cx, cy), OBSTACLE_RADIUS, 0.7)
    
    #there are obstacles in global map that also need to be added
    '''for p in range(1, c_g):
        if min(dist[:, p]) > 15 and min(dist[:, p]) < 30: #this obstacles was probably not added by anyone
            (cx, cy) = (centroids_g[p][0], centroids_g[p][1])
            global_map = drawObstacle(global_map, (cx, cy), OBSTACLE_RADIUS, 255)
            #state_prob = drawObstacle(state_prob, (cx, cy), OBSTACLE_RADIUS, 0.7)'''
        
                
    return (global_map, state_prob)