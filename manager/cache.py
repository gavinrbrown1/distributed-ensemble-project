#cache control code on manager
#file structure on manager is as follows
#manager.py
#cache.py
#cache_decisions.txt
#cache/
#-----cifar10 images
import numpy as np
import os
from os import listdir
from os.path import isfile, join
from PIL import Image

#intended flow: manager calls useCache when img arrives from client
#it either returns true and the decision, or it returns false
#in the case of false, manager sends img to classifiers and upon receipt
#manager calls updateCache

#threshold for cache decision
thresh = 0.9

#computes the Zero-Normalized Cross-Correlation Coefficient
#(ZNCC) between two images to determine if there 
#is a match in the cache; similarity metric ranges [0,1]
#p0, p1 np arrays
def ZNCC(p0,p1):
    #p0 = p0.astype(np.float)
    #p1 = p1.astype(np.float)
    #p0, p1 are two images in the form of np arrays
    zncc = 0

    #n pixels to average over
    rows = len(p0)
    columns = len(p0[0]) 
    n = rows * columns

    #mean image values
    mu0 = np.mean(p0)
    mu1 = np.mean(p1)

    #stds
    s0 = np.std(p0)
    s1 = np.std(p1)

    for i in range(0, rows):
        for j in range(0, columns):
            zncc += (p0[i][j]-mu0)*(p1[i][j]-mu1)/(s0*s1)

    #take mean again bc 3 values for RGB
    return np.mean(zncc)/n

#compute L2 distance between images
#takes in image names, not np arrays yet
def l2(p0, p1):
    img0 = Image.open(p0)
    #img.load()
    np0 = np.asarray(img0, dtype="int32" )

    img1 = Image.open('./cache/' + p1)
    np1 = np.asarray(img1, dtype="int32" )
    return np.linalg.norm(np1-np0)

#computes pairwise distances
def minPairwiseDist(cachepath='./cache/', distances = './pairwise_distances.txt'): 
    currPairwise  = [f for f in listdir('./') if isfile(join('./', f))]
    currCache  = [f for f in listdir(cachepath) if isfile(join(cachepath, f))]
    currMinDist = 100000000
    currMinPair = []

    if distances in currPairwise:
        #distances have already been computed
        #file is in the form image name 1, image name 2, distance per line
        with open(distances, 'r') as f:
            lines = f.readlines()
            for pair in lines:
                [im1, im2, dist] = pair.strip().split(',') 
                if dist < currMinDist:
                    currMinDist = dist
                    currMinPair = [im1, im2]
    else:
        #the first time this will be called is when the cache reaches capacity
        pairwiseDistances = [] 
        #list of [im1, im2, dist] entries
        #need to compute distances between imgs in cache for the first time
        for i in range(0, len(currCache)):
            for j in range(0, len(currCache)):
                if (i != j) and (currCache[j] not in [el[0] for el in pairwiseDistances]):
                    ll2 = l2(currCache[i], currCache[j])
                    #compute distance and add to list
                    pairwiseDistances.append([currCache[i], currCache[j], ll2])
                    if ll2 < currMinDist:
                        currMinDist = ll2
                        currMinPair = [currCache[i], currCache[j]]
        #write all pairwise distances to file
        with open(distances, 'w') as f:
            for entry in pairwiseDistances:
                f.write(entry[0] + ',' + entry[1] + ',' + str(entry[2]) + '\n')
    #return the pair of images with minimal distance to each other
    return currMinPair
                    

#removes pair of images that are closest to each other in cache
#and removes the values in the decisions and distances txt file
def kickOutCache(distances='./pairwise_distances.txt', mypath='./cache/'):
    currCache  = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    #have to remove the two images from the cache
    pairToRemove = minPairwiseDist()
    os.remove(mypath + pairToRemove[0])
    os.remove(mypath + pairToRemove[1])

    keepers = []
    #have to remove all pairwise distances that include either image in distances file
    with open(distances, 'r') as f:
        entries = f.readlines()
        for pairwise in entries:
            pairwise = pairwise.strip().split(',')
            if (pairwise[0] not in pairToRemove) and (pairwise[1] not in pairToRemove):
                keepers.append(pairwise)
    
    #now overwrite existing file with remaining distances
    with open(distances, 'w') as f:
        for kept in keepers:
            f.write(kept[0] + ',' + kept[1] + ',' + kept[2] + '\n')

#compute distance of new cache image p0 against all existing cache files
#add these pair to pairwise distance txt file
#p0 is the image file name, not numpy
def addNewPairwise(p0, cachePath='./cache/', pairwisePath='./pairwise_distances.txt'):
    newEntries = []

    cache = [f for f in listdir(cachePath) if isfile(join(cachePath, f))]
    for img in cache:
       newEntries.append([p0,img,l2(p0,img)])

    with open(pairwisePath, 'a') as f:
        for newE in newEntries:
            f.write(newE[0] + ',' + newE[1] + ',' + str(newE[2]) + '\n')

#return already classified value of image from saved text file
#cache_decisions.txt
#set up like fname, decision per row
def decision(fname, cache='./cache_decisions.txt'):
    with open(cache, 'r') as f:
        lines = f.readlines()
        for entry in lines:
            [imgName, decision] = entry.strip().split(',')
            if imgName == fname:
                return decision
    return "COULDNT LOCATE ENTRY IN CACHE!! ERROR!!"

#updates cache, adding new image to 
#and new decision to txt file
def updateCache(fname, pNew, dNew, mypath='./cache/'):
    #get num of images in current cache folder
    currCache  = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    cacheSize = len(currCache) 
    if cacheSize < 100:
        #in addition to adding this to the cache
        #we need to add its pairwise distance to the known distances
        addNewPairwise(fname)
        #print(type(pNew))
        #im = Image.fromarray(pNew, mode="RGB")
        with open(mypath + fname, 'wb') as f:
            f.write(pNew)
        
        with open('cache_decisions.txt', 'a') as f:
            f.write(fname + "," + str(dNew) + '\n')

    #but don't need to remove anything from set yet, since under 100
    else:
       #kickout closest pair of images
       #pre-emptively "backing off", but linear backoff
       kickOutCache()

       #now there's space, try again
       updateCache(fname, pNew, dNew, mypath='./cache/')

#pNew here is filename     
def useCache(pNew, mypath='./cache/'):
    #create cache folder if it doesn't yet exist
    if not os.path.exists(mypath):
        os.makedirs(mypath)

    #get names of images in current cache folder
    currCache  = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    for f in currCache:
        cacheImg = Image.open(mypath + f)
        cacheData = np.asarray(cacheImg, dtype="int32")

        newImg = Image.open(pNew)
        newData = np.asarray(newImg, dtype="int32")
        zncc = ZNCC(newData, cacheData) #cv2.imread(f, mode='RGB'))
        print('ZNCC = ' + str(zncc))
        if zncc > thresh:
            #spit out cached class
            #chooses first match in cache for efficiency
            return [True, decision(f)]
        #else, continue checking other cache samples

    #if we exit the for loop w/o return, no cache sample matches 
    #manager passes to classifiers
    #also need to update cache now with new sample, manager has to call update fn
    return [False, None]



