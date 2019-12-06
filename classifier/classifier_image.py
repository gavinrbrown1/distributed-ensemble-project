# Program:     server_2.py
# Author:      Iden Kalemaj, Gavin Brown
# Description: Implementation of a classifiying server through socket application programmming. 
# Command line Inputs: server port number


from socket import *
import sys
import time
from thread import *
import threading 
   
def clientHandler(connectionSocket, serverPort, imgcounter):

      # read sentence with image size
      data = ""
      try:
          data = connectionSocket.recv(4096)
      except:
          connectionSocket.close()
          
      if data.startswith('SIZE'):          
	  tmp = data.split()
          size = int(tmp[1])
          print "Image size was received"
          connectionSocket.sendall("GOT SIZE")
      else:
          connectionSocket.close()
      
      # read ID
      data = ""
      try:
	 data = connectionSocket.recv(4096)
      except:
	 connectionSocket.close()

      if data.startswith('ID'):
	   tmp = data.split()
           id = int(tmp[1])
           print('ID was received')
	   connectionSocket.sendall("GOT ID")
      
	
      # read image
      data = ""
      try:
	  data = connectionSocket.recv(49600000)
	  print "Received image of size: %s" % len(data)
      except:
          connectionSocket.close()
  	
      if len(data) != size:
	print "Size of image received does not match size advertised"
        print "Terminating connection"
	connectionSocket.close()

      # store image
      basename = "image%s.png"
      myfile = open(basename % imgcounter, 'wb')
      myfile.write(data)
      myfile.close()
      connectionSocket.sendall("GOT IMAGE")
      
      
      # read sentence closing connection
      data = ""
      try:
          data = connectionSocket.recv(4096)
      except:
          connectionSocket.close()
          
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
