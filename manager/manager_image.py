# Program:     manager_image.py
# Author:      Andrea Burns, Gavin Brown, Iden Kalemaj
# Description: Implementation of a manager through socket application programmming.
# Command line inputs: manager port number

#import cv2
from cache import *
from socket import *
import sys
import time
from _thread import *
import threading
from manager_classifier_communication import callClassifiers

# Decide on number of classifiers used
numClass = 4

def clearCache(path='./cache/'):
    #remove cache images
    currCache = [img for img in os.listdir(path)]
    for i in currCache:
        os.remove(path + i)    
    
    #remove cache decisions
    os.remove('./cache_decisions.txt')

    #remove pairwise distances
    os.remove('./pairwise_distances.txt')

    print('Clearing cache, time for a new experiment!')

# function to receive message from socket
def recv_try(connectionSocket, numBytes):
    data = ""
    try:
        data = connectionSocket.recv(numBytes).decode()
    except:
        connectionSocket.close()

    return data
    

def clientHandler(connectionSocket, serverPort, imgcounter):
    # read sentence with image size
    data = recv_try(connectionSocket, 4096)

    if data[0:4] == 'SIZE':
        tmp = data.split()
        size = int(tmp[1])
        print("Image size was received")
        connectionSocket.sendall(("GOT SIZE").encode())
    else:
        connectionSocket.close()
      
    # read ID
    data = recv_try(connectionSocket, 4096)
    image_id = ''

    if data[0:2] == 'ID':
        tmp = data.split()
        image_id = tmp[1]
        print('ID received from client: %s' % image_id)
        connectionSocket.sendall(("GOT ID").encode())
    else:
        connectionSocket.close()

    # read image
    data = ""
    try:
        data = connectionSocket.recv(49600000)
    except:
        connectionSocket.close()
    if data != "":
        print("Received image of size: %s" % len(data))

    if len(data) != size:
        print("Size of image received does not match size advertised")
        print("Terminating connection")
        connectionSocket.close()
        
    # store image
    basename = "image" + str(imgcounter) + ".png"
    myfile = open(basename, 'wb')
    myfile.write(data)
    myfile.close()

    # check cache before sending to classifiers
    tryCache = useCache(basename)
    if tryCache[0] == False:
        # send image to classifiers and receive classification
        response = callClassifiers(numClass, data, image_id)
        if response > -1:
            #img = Image.open(basename)
            #data = np.asarray(img, dtype='int32')
            updateCache(basename, data, response)
            connectionSocket.sendall(("Image is of class %s" % response).encode())
        else:
            connectionSocket.sendall(("Image classification failed").encode())
 
        fn = 'cache_stats_' + image_id + '.txt'
        #update cache hit stats
        with open(fn, 'a') as f:
            f.write(basename+',miss\n')

    else:
        #return cached decision
        print("Image was found in cache")
        connectionSocket.sendall(("Image is of class %s" % tryCache[1]).encode())
    
        fn = 'cache_stats_' + image_id + '.txt'
        #update cache hit stats
        with open(fn, 'a') as f:
            f.write(basename+',hit\n')

    #can now delete image from manager folder (not from cache)
    os.remove(basename)

    # read sentence closing connection
    data = recv_try(connectionSocket, 4096)

    if data.startswith('Closing'):
        connectionSocket.close()
    else:
        connectionSocket.close()




if __name__=='__main__':

    # Port number of server is specified as command line argument
    if len(sys.argv) < 2:
        print("Please specify port number of server as command line argument.")
    serverPort = int(sys.argv[1])

    # Create a server TCP pocket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    # Associate the port number with the server
    serverSocket.bind(('', serverPort))

    # serverSocket will be the welcoming socket
    serverSocket.listen(1)
    imgcounter = 0
    while True:
        print("Waiting for client...")

        # Accept the client request and create a new socket dedicated to the client
        connectionSocket, addr = serverSocket.accept()
        print("**A new client has joined!**")
        imgcounter +=1

        if imgcounter >= 99:
            #new experiment, start anew
            clearCache()
            imgcounter = 0

        # Start a new thread for client that just joined
        start_new_thread(clientHandler, (connectionSocket, serverPort, imgcounter))

    serverSocket.close()





