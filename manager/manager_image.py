# Program:     manager_image.py
# Author:      Andrea Burns, Gavin Brown, Iden Kalemaj
# Description: Implementation of a manager through socket application programmming. 
# Command line inputs: manager port number


from socket import *
import sys
import time
from thread import *
import threading 
from manager_classifier_communication import callClassifiers 

# Decide on number of classifiers used
numClass = 1

# function to receive message from socket
def recv_try(connectionSocket, numBytes):
    data = ""
    try:
      data = connectionSocket.recv(numBytes)
    except:
      connectionSocket.close()
      
    return data


def clientHandler(connectionSocket, serverPort, imgcounter):

      # read sentence with image size
      data = recv_try(connectionSocket, 4096)
          
      if data.startswith('SIZE'):          
	  tmp = data.split()
          size = int(tmp[1])
          print "Image size was received"
          connectionSocket.sendall("GOT SIZE")
      else:
          connectionSocket.close()
      
      # read ID
      data = recv_try(connectionSocket, 4096)

      if data.startswith('ID'):
	  tmp = data.split()
          image_id = int(tmp[1])
          print('ID was received')
	  connectionSocket.sendall("GOT ID")
      else:
          connectionSocket.close()
      
      # read image
      data = recv_try(connectionSocket, 49600000)
      if data != "":
	  print "Received image of size: %s" % len(data)
  	
      if len(data) != size:
	  print "Size of image received does not match size advertised"
          print "Terminating connection"
	  connectionSocket.close()

      # store image
      basename = "image%s.png"
      myfile = open(basename % imgcounter, 'wb')
      myfile.write(data)
      myfile.close()
      
      # send image to classifiers and receive classification
      response = ""
      response = callClassifiers(numClass, data, image_id)
      
      if response != "":  
          connectionSocket.sendall("Image is of class %s" % response)
      else:
          connectionSocket.sendall("Image classification failed")
      
      
      # read sentence closing connection
      data = recv_try(connectionSocket, 4096)
          
      if data.startswith('Closing'):
          connectionSocket.close()
      else:
          connectionSocket.close()
          


if __name__=='__main__':

    # Port number of server is specified as command line argument
    if len(sys.argv) < 2: 
        print "Please specify port number of server as command line argument."
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
        print("A new client has joined!")
        imgcounter +=1
        # Start a new thread for client that just joined
        start_new_thread(clientHandler, (connectionSocket, serverPort, imgcounter))
    
    serverSocket.close()
