# Gavin Brown, grbrown@bu.edu # first pass at a CNN for my AI project on weight space symmetries 
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
from torch.autograd import Variable

import numpy as np
#from scipy.ndimage import imread 
from PIL import Image
#from scipy.optimize import linear_sum_assignment
#import sys
#import time
#import matplotlib.pyplot as plt
#plt.switch_backend('agg')

from CNN import Net
#from utils import *

device = torch.device('cpu')
datapath = '~/Desktop/cifar-10-images'

def load_network(filename):
    pass

def load_image(filename):
    pass

def classify(model, image):
    pass

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
