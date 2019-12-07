import random
import socket, select
import sys
from time import gmtime, strftime
from random import randint

# list of image names  used in the experiment
images = ["apple-touch-icon-144x144-precomposed.png"]
# list of corresponding id, indicating network parameters used 
# for each image in the experiment
ids = [1]

HOST = '198.248.248.133'

# Port number of server is specified as command line argument
if len(sys.argv) < 2:
    print "Please specify port number of server as command line argument."
PORT = int(sys.argv[1])


for i in range(len(images)):
    
    # establish connection with manager		
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    sock.connect(server_address)
    
    # read in image
    myfile = open(images[i], 'rb')
    bytes = myfile.read()
    size = len(bytes)
    
    # send image size to server
    sock.sendall("SIZE %s\n" % size)
    
    answer = ""
    try:
      answer = sock.recv(4096)
      print 'answer = %s' % answer
    except:
      sock.close()
    
    # send image ID and image to server
    if answer.startswith('GOT SIZE'):
      
      # send image ID
      print 'Sending ID...'
      sock.sendall('ID %s' % ids[i])
      answer = ""
      try:
	answer = sock.recv(4096)
        print 'anser = %s' % answer
      except:
	sock.close()

      # send image
      if answer.startswith('GOT ID'):
      	print 'Sending image...'
      	sock.sendall(bytes)
    
      	# check server reply
      	answer = ""
      	try:
            answer = sock.recv(4096)
            print 'answer = %s' % answer
      	except:
            sock.close()
    
      	if answer.startswith('Image is of class'):
            sock.sendall("Closing connection\n")
            sock.close()
		
    myfile.close()
