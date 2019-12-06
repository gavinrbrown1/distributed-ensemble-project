# Gavin Brown, grbrown@bu.edu # first pass at a CNN for my AI project on weight space symmetries 
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
from torch.autograd import Variable

import numpy as np
#from scipy.ndimage import imread 
from PIL import Image
import random
#from scipy.optimize import linear_sum_assignment
#import sys
import time
#import matplotlib.pyplot as plt
#plt.switch_backend('agg')

from CNN import Net
#from utils import *

#device = torch.device('cpu')
#datapath = '~/Desktop/cifar-10-images'

def load_network():
    """doesn't return anything"""
    net = Net()
    net.load_state_dict(torch.load('cnn_1_final.pt', map_location=torch.device('cpu')))
    net.eval()  # set in evaluation mode
    return net

def load_image(filename):
    """given filename, return 1x3x32x32 torch tensor"""
    image = Image.open(filename)
    image.load()
    image = np.asarray(image, dtype='float32')
    image = np.transpose(image, (2,0,1))
    image = np.reshape(image, (1,3,32,32))
    image = torch.from_numpy(image)
    return image

def classify(net, filename, delay_mean, error_probability):
    """
    Using pre-loaded network, find image and return prediction.
    filename: image name
    delay_mean: delay time is drawn from exponential distribution with this mean, in seconds.
    error_probability: w.p., output a random guess.
    """
    image = load_image(filename)
    prediction = torch.max(net(Variable(image))[-1].data, 1)

    # draw a sample from an exponential distribution
    if delay_mean != 0:
        wait_time = random.expovariate(1.0 / delay_mean)
        print('waiting', wait_time, 'sec')
        time.sleep(wait_time)

    # with specified probability, output a random guess
    if random.random() < error_probability:
        print('flipping')
        prediction = random.randrange(10)
        return prediction
    
    # otherwise, have to extract the value from the torch type
    return int(prediction.values[0])

net = load_network()
prediction = classify(net, 'images/image_0.jpeg', 1, 0.2)
print(prediction)

"""
# load the network
net = Net()
net.load_state_dict(torch.load('cnn_1_final.pt', map_location=device))
#net.to(device)
net.eval()

# load in an image
#image = imread('images/image_0.jpeg')
img = Image.open('images/image_0.jpeg')
img.load()
image = np.asarray( img, dtype="float32" )
print(type(image))
print(image.dtype)
print(image.shape)
image = np.transpose(image, (2,0,1))
image = np.reshape(image, (1,3,32,32))
image = torch.from_numpy(image)

# predict on it
prediction = torch.max(net(Variable(image))[-1].data, 1)
print('Predicted!')
print('type:', type(prediction))
#print('shape:', prediction.shape)
print('values:', prediction)
"""
