import random
import socket, select
from time import gmtime, strftime
from random import randint



def recv_all(connectionSocket):
    message = ""
    while True:
      try:
        p = connectionSocket.recv(1).decode()
        message += p
        if p == "\n":
          break
      except:
        break
    return(message)


images = ["apple-touch-icon-144x144-precomposed.png"]



HOST = '198.248.248.133'
PORT = 8889


for image in images:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    sock.connect(server_address)
    
    myfile = open(image, 'rb')
    bytes = myfile.read()
    #bytes += "\n"
    print "Size of image to be delivered is %s" %len(bytes)
    size = len(bytes)
    
    # send image size to server
    sock.sendall("SIZE %s\n" % size)
    
    answer = ""
    try:
      answer = recv_all(sock)
      print 'answer = %s' % answer
    except:
      sock.close()
    
    # send image to server
    if answer.startswith('GOT SIZE'):
      print 'Sending image...'
      sock.sendall(bytes)
    
      # check what server sent
      answer = ""
      try:
         answer = sock.recv(4096)
         print 'answer = %s' % answer
      except:
         sock.close()
    
      if answer.startswith('GOT IMAGE'):
          sock.sendall("Closing connection\n")
          sock.close()
          print 'Image successfully sent to server'
    
    myfile.close()
