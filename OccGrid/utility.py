#set of utitlity functions to print/ save output images and errors

from numpy import linalg as LA
import cv2

#function to calculate and save error metric and difference between ground truth and estimated states
#returns the error metric and saves difference image as a png
#Pixels map:
# Ground truth == estimate: 0
# Ground truth =/= estimate: 255
def compareWithGroundTruth(state_GT, state_est):
  diff_image = np.zeros_like(state_GT);
  diff_image[state_GT == state_est] = 0
  diff_image[state_GT != state_est] = 255
  saveImagePNG(diff_image, "diff_image.png");
  
  error = LA.norm(diff_image)
  error = error ** 2;
  return error


##Function to display the grid map as image
#params: single frame,a 2d image
def saveImagePNG(img, fileName = "temp.png"):
    if (img is not None):
      cv2.imwrite(img, fileName)

