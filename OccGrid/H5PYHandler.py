import h5py

#Function to read frames from H5PY datafile
#Functions reads 'numFrames' frames starting at startIdx
#Default 'numFrames' ==1
def getData_(filename, dataset, startIdx, numFrames=1):
    if (numFrames <= 0):
        numFrames = 1; # since we will be returning only 1 frame
    
    try:
        file = h5py.File(filename, 'r')   # 'r' means that hdf5 file is open in read-only mode
    except Exception as e:
        print("Problem in file reading. Error message: {}".format(e));
        return None;
        
    #ensure we are reading within valIdx bounds
    if (startIdx >= file[dataset].shape[2] or startIdx + numFrames > file[dataset].shape[2]):
        print 'Index out of bounds when reading file {}. Max size is {}'.format(filename, file[dataset].shape[2]);
        file.close();
        return None
            
    #shape of data is (100, 100, n_frames)
    #maybe we need to transpose to be able to read and plot
    data = file[dataset][:, :, startIdx : startIdx + numFrames];
    file.close();
    return data#.transpose(2, 0, 1)

def getData(filename, startIdx, num=1):
    GT = None
    LS = None
    ret = True
    GT = getData_(filename, 'ground_truth', startIdx, num);
    LS = getData_(filename, 'occupancy', startIdx, num);
    if GT is None or LS is None:
        ret = False
    return (ret, GT, LS)
    