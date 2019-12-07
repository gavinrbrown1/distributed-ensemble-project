# Program:     manager_classifier_communication.py
# Author:      Andrea Burns, Gavin Brown, Iden Kalemaj
# Description: Implement communication between manager and classifiers.  


import socket, select
import sys
import time
from collections import Counter

classifier_ip = ['172.17.1.10']
classifier_port = int(sys.argv[1])
numClass = 1


def recv_try(connectionSocket, numBytes):
    data = ""
    try:
      data = connectionSocket.recv(numBytes)
    except:
      connectionSocket.close()
      
    return data


# numClass	: number of classifiers that the manager asks for classification
# image		: image to be classified, in string format
# image_id	: id of image, as communicated by client, that determines experimental parameters
#		  about delay and corruption in the communication between classifier and manager			
def callClassifiers(numClass, image, image_id):
      answers = []
      for i in range(numClass):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (classifier_ip[i], classifier_port)
        sock.connect(server_address)
        
        sock.sendall('ID %s' % image_id)
        answer = recv_try(sock, 4096)
        if answer.startswith('GOT ID'):
            print 'Sending image to classifier %s' % i
      	    sock.sendall(image)
    
            # check server reply
            answer = recv_try(sock, 4096)
            print 'answer = %s' % answer
        
      	    if answer.startswith('CLASS'):
                tmp = answer.split()
                classf = int(tmp[1])
                answers.append(classf)
                sock.sendall("Closing connection")
                sock.close()
                print 'Classification was successful'
         
      most_frequent = Counter(answers).most_common(1)[0][0]
      return most_frequent
