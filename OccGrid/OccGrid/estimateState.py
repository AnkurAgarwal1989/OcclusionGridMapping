import os
import sys, getopt
import time

def usage():
    print "usage"
    print "\t -h --help : prints this usage information"
    print "\t -f --filename : REQUIRED. Path to H5PY file. If file exists in same location, only name is sufficient"
    print "\t -i --index : REQUIRED. Index of frame to be estimated. Should be >= 20"
    print "\t -g --groundTruth: OPTIONAL. flag to save ground truth for ease of comparison. default = False"
    return;

def main(argv):
    startTime = time.time();
    fileName = None;
    idx = 0;
    saveGroundTruth = False;
    
    try:
        opts, args = getopt.getopt(argv, "hf:i:g",["help", "filename = ", "index = "]);
        if not opts:
            print 'No options supplied'
            usage();
            sys.exit();
    except getopt.GetoptError:
            usage();
            sys.exit(2);
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage();
            sys.exit();
    
    for opt, arg in opts:
        if opt in ("-f", "--filename"):
            fileName = arg;
        elif opt in ("-i", "--index"):
            idx = int(arg);
            if idx < 20:
              print "The index needs to be >= 20."
              usage();
              sys.exit();
        elif opt == '-g':
            saveGroundTruth = True;
    
    if fileName is None or idx == 0:
      print "Required arguments missing"
      usage();
      sys.exit();
    
    HEIGHT = 100
    WIDTH = 100
    
    if (saveGroundTruth):
      Gnd_Truth = getData(fileName, 'ground_truth', HEIGHT, WIDTH, idx, idx+1);
      saveImage(GT, True);
    
    Laser_Scans =  getData(fileName, 'laser_scan', HEIGHT, WIDTH, idx - 20, idx + 1);
    
    T = 20 #time steps
    State_Map = np.
    
    
    
    
    print "Total time taken %s minutes" % ((time.time() - startTime)/60);
    print "Return Value: " + str(success);
    
    if success:
        return(0);
    else:
        return(-1);

if __name__ == "__main__":
    main(sys.argv[1:])
