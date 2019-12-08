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

label2name = {0: 'airplane',
              1: 'automobile',
              2: 'bird',
              3: 'cat',
              4: 'deer',
              5: 'dog',
              6: 'frog',
              7: 'horse',
              8: 'ship',
              9: 'truck'}

with open('true_labels.csv', 'w') as f:
    count = 0
    for data in trainloader:
        images, labels = data
        int_label = int(labels[0])
        #images = np.reshape(images.numpy(), (3,32,32))

        #print(images.shape)
        test = np.zeros((32,32,3))
        #print(images[0][0])
        for i in range(0,32):
            for j in range(0,32):
                test[i][j] = [images[0][0][i][j], images[0][1][i][j],images[0][2][i][j]]

        test_img = np.uint8(255 * test)
        im = PIL.Image.fromarray(test_img)
        #im.save('./tester_andrea.png')

        #images = np.reshape(np.uint8(255 * images), (3,32,32))
        #print(images.shape)

        #im = PIL.Image.fromarray(images)

        im.save('images/image'+str(count)+'.jpeg')

        f.write('image'+str(count)+'.jpeg,'+str(int_label)+','+label2name[int_label]+'\n')

        #print(images.shape)
        count += 1
        if count % 100 == 0:
            print(count)
        if count >= 1000:
            break

