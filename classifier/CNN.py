# Gavin Brown, grbrown@bu.edu
# CS655 Final Project
# Architecture taken from CS640 Final Project, that has citations

# Define the architecture we use for experiments

import torch
import torch.nn as nn

class Net(nn.Module):
    def __init__(self):
        super(Net,self).__init__()
        
        self.ReLU = nn.ReLU(inplace=True)
        self.MaxPool = nn.MaxPool2d(kernel_size=2,stride=2)

        self.dropout005 = nn.Dropout2d(p=0.05)
        self.dropout01 = nn.Dropout(p=0.01)

        self.conv1 = nn.Conv2d(in_channels=3,out_channels=32,kernel_size=3,padding=1)
        self.conv2 = nn.Conv2d(in_channels=32,out_channels=64,kernel_size=3,padding=1)
        self.conv3 = nn.Conv2d(in_channels=64,out_channels=128,kernel_size=3,padding=1)
        self.conv4 = nn.Conv2d(in_channels=128,out_channels=128,kernel_size=3,padding=1)
        self.conv5 = nn.Conv2d(in_channels=128,out_channels=256,kernel_size=3,padding=1)
        self.conv6 = nn.Conv2d(in_channels=256,out_channels=256,kernel_size=3,padding=1)

        self.linear1 = nn.Linear(4096,1024)
        self.linear2 = nn.Linear(1024,512)
        self.linear3 = nn.Linear(512,10)

        self.logsoftmax = nn.LogSoftmax(1)

    def forward(self, x):
        # report out all numbers
        x0 = self.conv1(x)
        x0 = self.ReLU(x0)

        x1 = self.conv2(x0)
        x1 = self.ReLU(x1)
        
        x2 = self.MaxPool(x1)
        x2 = self.conv3(x2)
        x2 = self.ReLU(x2)
        
        x3 = self.conv4(x2)
        x3 = self.ReLU(x3)
        
        x4 = self.MaxPool(x3)
        x4 = self.dropout005(x4)
        x4 = self.conv5(x4)
        x4 = self.ReLU(x4)

        x5 = self.conv6(x4)
        x5 = self.ReLU(x5)

        x6 = self.MaxPool(x5)
        #xfull = x6
        x6 = x6.view(x6.size(0), -1)    # done with convolutions, flatten
        #xflat = x6
        x6 = self.dropout01(x6)
        x6 = self.linear1(x6)
        x6 = self.ReLU(x6)

        x7 = self.linear2(x6)
        x7 = self.ReLU(x7)

        x8 = self.dropout01(x7)
        x8 = self.linear3(x8)
        
        x9 = self.logsoftmax(x8)
        
        # CS 640 cares about activations, so they get exposed on the forward pass.
        # x9 is the prediction.
        return (x0, x1, x2, x3, x4, x5, x6, x7, x8, x9)

