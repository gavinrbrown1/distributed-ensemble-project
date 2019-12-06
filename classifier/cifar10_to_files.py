# Gavin Brown, grbrown@bu.edu
# CS 655 Final Project
# Distributed Ensembling of Image Classifiers

# load in the CIFAR-10 data the ``standard'' way, then make it images

import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
from torch.autograd import Variable

import numpy as np
import PIL

datapath = '~/Desktop/cifar-10-images'

#device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
device = torch.device('cpu')
#criterion = nn.NLLLoss()

#transform_train = transforms.Compose([
#    transforms.RandomCrop(32, padding=4),
#    transforms.RandomHorizontalFlip(),
#    transforms.ToTensor(),
#    transforms.Normalize((0.4914,0.4822,0.4465),(0.2023,0.1994,0.2010))])
#
transform_test = transforms.Compose([
    transforms.ToTensor()])#,
    #transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))])

trainset = torchvision.datasets.CIFAR10(root=datapath,
                                        train=True,
                                        download=True, 
                                        transform=transform_test)
trainloader = torch.utils.data.DataLoader(trainset,
                                            batch_size=1,
                                            shuffle=True)

testset = torchvision.datasets.CIFAR10(root=datapath,
                                        train=False,
                                        download=True,
                                        transform=transform_test)
testloader = torch.utils.data.DataLoader(testset,
                                            batch_size=1000,
                                            shuffle=True)

count = 0
for data in trainloader:
    images, labels = data
    images = np.reshape(images.numpy(), (3,32,32))

    scaled = np.uint8(255 * images)
    scaled = np.transpose(scaled, (1,2,0))
    #print('shape:', scaled.shape)
    #print(type(scaled))
    #print(scaled.dtype)
    #print(np.max(scaled, axis=(0,1,2)))
    #print(np.min(scaled, axis=(0,1,2)))
    #print()

    im = PIL.Image.fromarray(scaled, mode='RGB')
    #print(im.size)

    im.save('images/image_'+str(count)+'.jpeg')
    #print(images.shape)
    count += 1
    if count % 100 == 0:
        print(count)
    if count >= 1000:
        break

