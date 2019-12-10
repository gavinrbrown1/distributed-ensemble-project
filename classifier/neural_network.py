# Gavin Brown, grbrown@bu.edu 
# CS 655 Final Project
# Functions to classify images, possibly with delay and/or error

import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
from torch.autograd import Variable

import numpy as np
from PIL import Image
import random
import time

from CNN import Net

def load_network():
    """load and return the pre-trained network for prediction"""
    net = Net()
    net.load_state_dict(torch.load('cnn_1_final.pt', map_location=torch.device('cpu')))
    #net.eval()  # set in evaluation mode, as opposed to training
    return net

def load_image(filename):
    """given filename, return 1x3x32x32 torch tensor"""
    normal =  transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))

    image = Image.open(filename)
    image.load()
    image = np.asarray(image, dtype='float32')
    image = np.transpose(image, (2,0,1))
    image = image / 255
    image = torch.from_numpy(image)
    image = normal.__call__(image)
    image = image.resize_((1,3,32,32))
    return image

def classify(net, filename, fixed_delay, exp_delay_mean, error_probability):
    """
    Using pre-loaded network, find image and return prediction.
    filename: image name
    fixed_delay: always delay this much, in seconds
    delay_mean: delay time is drawn from exponential distribution with this mean, in seconds.
    error_probability: w.p., output a random guess.
    """
    image = load_image(filename)
    prediction = torch.max(net(Variable(image))[-1].data, 1)

    # model slower connection or longer time to classify
    time.sleep(fixed_delay)

    # draw a wait-time sample from an exponential distribution
    if exp_delay_mean != 0:
        wait_time = random.expovariate(1.0 / exp_delay_mean)
        time.sleep(wait_time)

    # with specified probability, output a random guess
    if random.random() < error_probability:
        prediction = random.randrange(10)
        return prediction
    
    # otherwise, have to extract the value from the torch type
    return int(prediction.indices[0])

