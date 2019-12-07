# Program:     classifier_main.py
# Author:      Andrea Burns, Gavin Brown, Iden Kalemaj
# Description: Implementation of a classifier through socket application programmming. 


from socket import *
import sys
import time
from thread import *
import threading 


# function to receive message from socket
def recv_try(connectionSocket, numBytes):
    data = ""
    try:
      data = connectionSocket.recv(numBytes)
    except:
      connectionSocket.close()
      
    return data

def clientHandler(connectionSocket, serverPort, imgcounter):

      # read ID
      data = recv_try(connectionSocket, 4096)
          
      if data.startswith('ID'):          
	  tmp = data.split()
          image_id = int(tmp[1])
          print "Image ID was received"
          connectionSocket.sendall("GOT ID")
      else:
          connectionSocket.close()
      
      # read image
      image = recv_try(connectionSocket, 49600000)
      if image != "":
	  print "Received image of size: %s" % len(image)

      # store image
      basename = "image%s.png"
      myfile = open(basename % imgcounter, 'wb')
      myfile.write(image)
      myfile.close()
      
      # call classification function
      classf = 0
      
      # implement delay and corruption
      time.sleep(0)
      
      # send classification to manager
      if classf > -1:  
          connectionSocket.sendall("CLASS %s" % classf)
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
        print("Waiting for manager...")
        
        # Accept the client request and create a new socket dedicated to the client
        connectionSocket, addr = serverSocket.accept()
        print("A manager has joined!")
        imgcounter +=1
        # Start a new thread for client that just joined
        start_new_thread(clientHandler, (connectionSocket, serverPort, imgcounter))
    
    serverSocket.close()
