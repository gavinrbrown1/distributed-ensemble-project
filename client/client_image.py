import random
import socket, select
import sys
from time import gmtime, strftime
import random

def sample_index(k, method, seed):
    """returns a length-k list, sampled with replacement from images according to method"""
    random.seed(seed)
    if method == "uniform":
        # just sample uniformly
        return random.choices(range(1000), k=k)
    elif method == "power":
        # according to a randomly-chosen power law distribution
        weights = list(range(1000))
        random.shuffle(weights)
        weights = [1/(1+w) for w in weights] # add one to each, because python starts with zero
        return random.choices(range(1000), weights=weights, k=k)
    else:
        print('ERROR! Incorrect method name specific')
        return None

# list of image names  used in the experiment
image_sequence = sample_index(100, 'power', 655)
#image_sequence = [8, 9, 10, 11]
images = [("images/image" + str(x) + ".jpeg") for x in image_sequence] 

# list of corresponding id, indicating network parameters used
# for each image in the experiment
ids = 4*['0.0.0']

HOST = '198.248.248.133'

# Port number of server is specified as command line argument
if len(sys.argv) < 2:
    print("Please specify port number of server as command line argument.")
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
    sock.sendall(("SIZE %s\n" % size).encode())

    answer = ""
    try:
        answer = sock.recv(4096).decode()
        print('answer = %s' % answer)
    except:
        sock.close()
    
    # send image ID
    print('Sending ID...')
    sock.sendall(('ID %s' % ids[i]).encode())
    answer = ""
    try:
        answer = sock.recv(4096).decode()
        print('answer = %s' % answer)
    except:
        sock.close()
  
    # send image
    if answer[:6] == 'GOT ID':
        print('Sending image...')
        sock.sendall(bytes)
        # check server reply
        answer = ""
        try:
          answer = sock.recv(4096).decode()
          print('answer = %s' % answer)
        except:
          sock.close()
        
        if answer[:17] == 'Image is of class':
          sock.sendall(("Closing connection").encode())
          sock.close()
    myfile.close()
