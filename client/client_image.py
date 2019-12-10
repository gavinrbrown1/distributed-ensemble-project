import random
import socket, select
import sys
from time import time, gmtime, strftime
import random
import csv

def sample_index(n, method, seed):
    """returns a length-k list, sampled with replacement from images according to method"""
    random.seed(seed)
    if method == "uniform":
        # just sample uniformly
        return random.sample(range(1000), k=n)
    elif method == "power":
        # according to a randomly-chosen power law distribution
        weights = list(range(1000))
        random.shuffle(weights)
        weights = [1/(1+w) for w in weights] # add one to each, because python starts with zero
        return random.sample(range(1000), weights=weights, k=n)
    else:
        print('ERROR! Incorrect method name specific')
        return None


# read in information about all the experiments
image_ids = []
sampling_methods = []
with open('experiments.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    experiment_counter = 0
    for row in csv_reader:
        if experiment_counter > 0:
            image_id = row[0]+"."+row[1]+"."+"0"
            image_ids.append(image_id)
            sampling_methods.append(row[3])
        experiment_counter += 1



total_runs = 2
images_per_run = 10

# iterate over experiments
for experiment_number in range(experiment_counter):
    
    # set up experiment
    base_id = image_ids[experiment_number]
    sampling_method = sampling_methods[experiment_number]
    
    # iterate over runs for each experiment 
    for run_number in range(total_runs):
        
        # list of image names  used in the experiment
        image_sequence = sample_index(images_per_run, sampling_method, 655)
        images = [("images/image" + str(x) + ".jpeg") for x in image_sequence] 
    
        # set up lists to store predictions returned by the manager, and  communication times
        predicted_labels = []
        communication_times = []
    
        # list of corresponding id, indicating network parameters used
        # for each image in the experiment
        ids = len(image_sequence)*base_id
    
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
            start = time.time()
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
    	            end = time.time()
    	            predicted_labels.append(str(answer))
    	            communication_times.append(str(end-start))
    	        except:
    	            sock.close()
    	    
    	        if answer[:17] == 'Image is of class':
    	            sock.sendall(("Closing connection").encode())
    	            sock.close()
    	
            myfile.close()
    
        # after we've gone through all the images, write out csv with the results
        filename = '../results/results_experiment'+str(experiment_number)+'_run'+str(run_number)+'.csv'
        with open(filename, 'w') as f:
    	    for i in range(len(images)):
    	        f.write(images[i]+','+predicted_labels[i]+','+communication_times[i]+'\n')
