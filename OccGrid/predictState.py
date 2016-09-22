import cv2
import numpy as np

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
    b, thresh = cv2.threshold(state_map, 127, 255, cv2.THRESH_BINARY)
    connectivity =4
    
    c_idx, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, connectivity)
    #for each centroid (not background), create an obstacle
    
    for comp in range(1, c_idx):
        stat = stats[comp]
        centroid = centroids[comp]
        #do this only if area of obstacle is > 4
        if stat[4] >4:
            cx = stat[0] + (stat[2]/2)
            cy = stat[1] + (stat[3]/2)
            cx = centroid[0]
            cy = centroid[1]
            obs_prob = state_prob[centroid[1], centroid [0]]
            
            state_map = drawObstacle(state_map, (cx, cy), OBSTACLE_RADIUS, 255)
            state_prob = drawObstacle(state_prob, (cx, cy), OBSTACLE_RADIUS, obs_prob)
    return (state_map, state_prob)
