# Program:     manager_classifier_communication.py
# Author:      Andrea Burns, Gavin Brown, Iden Kalemaj
# Description: Implement communication between manager and classifiers.


import socket, select
import sys
import time
from collections import Counter

classifier_ip = ['172.17.1.10', '172.17.1.13', '172.17.1.12', '172.17.1.11']
classifier_port = int(sys.argv[1])
numClass = 4
timeout_var = 3

def recv_try(connectionSocket, numBytes):
    data = ""
    try:
        data = connectionSocket.recv(numBytes).decode()
    except:
        connectionSocket.close()

    return data

# numClass      : number of classifiers that the manager asks for classification
# image         : image to be classified, in string format
# image_id      : id of image, as communicated by client, that determines experimental parameters
#                 about delay and corruption in the communication between classifier and manager
def callClassifiers(numClass, image, image_id):
   
    answers = []
    sockets = []
    for i in range(numClass):
        sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        server_address = (classifier_ip[i], classifier_port)
        sockets[i].connect(server_address)
        sockets[i].settimeout(timeout_var)

    for i in range(numClass):
        # two classifiers experience delay
        if i == 0 | i == 1 | i == 2:
            sockets[i].sendall(('ID %s' % image_id).encode())
            print("ID sent to class: %s" % image_id)
        # two other classifiers experience no delay
        else:
            image_id = image_id[:2] + '0' + image_id[3:]
            sockets[i].sendall(('ID %s' % image_id).encode())

    for i in range(numClass):
        answer = recv_try(sockets[i], 4096)
        if answer[:6] == 'GOT ID':
            print('Sending image to classifier %s' % i)
            sockets[i].sendall(image)

    for i in range(numClass):
        # check server reply
        answer = recv_try(sockets[i], 4096)

        if answer[:5]== 'CLASS':
            tmp = answer.split()
            classf = int(tmp[1])
            answers.append(classf)
            sockets[i].sendall(("Closing connection").encode())
            sockets[i].close()
            print('answer = %s' % answer)
            print('Classification was successful')
        else:
            print('Timer for classifier %s expired' % i)
    """

    answers = []
    for i in range(numClass):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (classifier_ip[i], classifier_port)
        sock.connect(server_address)
        sock.settimeout(timeout_var)
        
        # two classifiers experience delay
        if i == 0 | i == 1 | i == 2:
            sock.sendall(('ID %s' % image_id).encode())
            print("ID sent to class: %s" % image_id)
        # two other classifiers experience no delay
        else:
            image_id = image_id[:2] + '0' + image_id[3:]
            sock.sendall(('ID %s' % image_id).encode())
        
        answer = recv_try(sock, 4096)
        if answer[:6] == 'GOT ID':
            print('Sending image to classifier %s' % i)
            sock.sendall(image)
  
            # check server reply
            answer = recv_try(sock, 4096)
  
            if answer[:5]== 'CLASS':
                tmp = answer.split()
                classf = int(tmp[1])
                answers.append(classf)
                sock.sendall(("Closing connection").encode())
                sock.close()
                print('answer = %s' % answer)
                print('Classification was successful')
            else:
                print('Timer for classifier %s expired' % i)
    """  
    if len(answers) >= 1:
        most_frequent = Counter(answers).most_common(1)[0][0]
    else:
        most_frequent = -1
  
    return most_frequent

