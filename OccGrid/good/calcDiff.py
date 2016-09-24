#set of utitlity functions to print/ save output images and errors

from numpy import linalg as LA

#function to calculate and save error metric and difference between ground truth and estimated states
#returns the error metric and saves difference image as a png
#Pixels map:
# Ground truth == estimate: 0
# Ground truth =/= estimate: 255


def saveDiff(gnd_truth, estimate):
  diff_image = np.zeros_like(gnd_truth);
  diff_image[gnd_truth == estimate] = 0
  diff_image[gnd_truth != estimate] = 255
  saveImage(diff_image, "diff_image");
  
  error = LA.norm(diff_image)
  error = error ** 2;
  return error
