# Gavin Brown, grbrown@bu.edu
# CS640 Class Project

# Assorted functions I use throughout my code

import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
from torch.autograd import Variable

import numpy as np
from scipy.optimize import linear_sum_assignment
import sys
import time
import matplotlib.pyplot as plt
plt.switch_backend('agg')

from CNN import Net

datapath = '.'

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
criterion = nn.NLLLoss()

transform_train = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.4914,0.4822,0.4465),(0.2023,0.1994,0.2010))])

transform_test = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))])

trainset = torchvision.datasets.CIFAR10(root=datapath,
                                        train=True,
                                        download=True,
                                        transform=transform_train)
trainloader = torch.utils.data.DataLoader(trainset,
                                            batch_size=128,
                                            shuffle=True)

testset = torchvision.datasets.CIFAR10(root=datapath,
                                        train=False,
                                        download=True,
                                        transform=transform_test)
testloader = torch.utils.data.DataLoader(testset,
                                            batch_size=1000,
                                            shuffle=True)

def calculate_accuracy(net, loader):
    correct = 0
    total = 0

    for data in loader:
        images, labels = data
        images, labels = images.to(device), labels.to(device)
        activations = net(Variable(images))
        outputs = activations[-1]
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    return 100 * correct / total

def best_permutation_activations(act1, act2, layer):
    out1, out2 = act1[layer], act2[layer]
    if layer in range(6): # convolutional activations, flatten to 2d matrix
        side = out1.size()[1]
        C = np.zeros((side,side))
        for i in range(side):
            for j in range(i,side):
                prod = torch.mul(out1[:,i,:,:],out2[:,j,:,:])
                total = torch.sum(prod, (0,1,2))
                C[i,j], C[j,i] = -total, -total
    else:
        costs = torch.mul(torch.matmul(torch.t(out1),out2),-1)
        C = costs.cpu().detach().numpy()
        C = C.copy()
    row_ind, col_ind = linear_sum_assignment(C)
    return col_ind

def best_permutation_euclidean(state1, state2, l):
    names = [['conv1.weight','conv1.bias'],
            ['conv2.weight','conv2.bias'],
            ['conv3.weight','conv3.bias'],
            ['conv4.weight','conv4.bias'],
            ['conv5.weight','conv5.bias'],
            ['conv6.weight','conv6.bias'],
            ['linear1.weight', 'linear1.bias'],
            ['linear2.weight', 'linear2.bias'],
            ['linear3.weight', 'linear3.bias']
            ]  
    side = state1[names[l][1]].size()[0]
    C = np.zeros((side,side))
    for i in range(side):
        for j in range(i,side):
            total = 0
            if l in range(5):   # convolutions
                t1, t2 = state1[names[l][0]][i,:,:,:],state2[names[l][0]][j,:,:,:]
                total += torch.dist(t1,t2).item()**2
                t1, t2 =state1[names[l+1][0]][:,i,:,:],state2[names[l+1][0]][:,j,:,:]
                total += torch.dist(t1,t2).item()**2
            elif l == 5:
                t1, t2 = state1[names[l][0]][i,:,:,:],state2[names[l][0]][j,:,:,:]
                total += torch.dist(t1,t2).item()**2
                t1, t2 =state1[names[l+1][0]],state2[names[l+1][0]]
                t1, t2 = t1.reshape((1024,256,4,4)), t2.reshape((1024,256,4,4))
                t1, t2 = t1[:,i,:,:], t2[:,j,:,:]
                total += torch.dist(t1,t2).item()**2
            else: # linear layer 
                t1, t2 = state1[names[l][0]][i,:],state2[names[l][0]][j,:]
                total += torch.dist(t1,t2).item()**2
                t1, t2 = state1[names[l+1][0]][:,i],state2[names[l+1][0]][:,j]
                total += torch.dist(t1,t2).item()**2
            # now add bias
            t1, t2 = state1[names[l][1]][i], state2[names[l][1]][j]
            total += torch.dist(t1,t2).item()**2
            C[i,j], C[j,i] = np.sqrt(total), np.sqrt(total)
    row_ind, col_ind = linear_sum_assignment(C)
    predicted_total = 0
    for i in range(side):
        predicted_total += C[row_ind[i],col_ind[i]]**2
    return col_ind, predicted_total
    
def euclidean_distance(state1, state2=0):
    vec1 = nn.utils.parameters_to_vector(state1.values())
    if state2 == 0:
        return torch.norm(vec1).item()
    else:
        vec2 = nn.utils.parameters_to_vector(state2.values())
        return torch.dist(vec1,vec2).item()

def test_loss_ensemble(net1, net2, alpha):
    total_loss = 0.0
    for i, data in enumerate(testloader, 0):
        inputs, labels = data
        inputs, labels = inputs.to(device), labels.to(device)
        inputs, labels = Variable(inputs), Variable(labels)

        # need to convert to probabilities, not log-prob
        acts1, acts2 = net1(inputs), net2(inputs)
        outputs1 = torch.exp(acts1[-1])
        outputs2 = torch.exp(acts2[-1])
        outputs = torch.log(torch.add(torch.mul(outputs1,alpha),
                                    torch.mul(outputs2,1-alpha)))

        loss = criterion(outputs, labels)
        total_loss += loss.item()
    return total_loss / len(testloader)

def test_loss_interpolate(net1, net2, alpha):
    total_loss = 0.0
    weights1 = net1.state_dict()
    weights2 = net2.state_dict()
    new_state = {}
    for name in weights1:
        new_state[name] = torch.add(torch.mul(weights1[name],alpha),
                                    torch.mul(weights2[name],1-alpha))

    new_net = Net()
    new_net.to(device)
    new_net.load_state_dict(new_state)
    new_net.eval()

    for i, data in enumerate(testloader, 0):
        inputs, labels = data
        inputs, labels = inputs.to(device), labels.to(device)
        inputs, labels = Variable(inputs), Variable(labels)

        outputs = new_net(inputs)[-1]
        loss = criterion(outputs, labels)
        total_loss += loss.item()
    return total_loss / len(testloader),euclidean_distance(new_net.state_dict())

def permute_hidden_layer(state, l, index):
    # permute the convolutions 
    if l in range(6):
        name = 'conv'+str(l+1)+'.weight'
        state[name] = torch.index_select(state[name],0,index)
        name = 'conv'+str(l+1)+'.bias'
        state[name] = torch.index_select(state[name],0,index)
        if l == 5:
            old_index = torch.LongTensor(range(4096))
            old_index = old_index.reshape((256, 4, 4))
            idx = index.cpu()
            old_index = torch.index_select(old_index, 0, idx)
            new_index = old_index.reshape(4096)
            name = 'linear1.weight'
            new_index = new_index.to(device)
            state[name] = torch.index_select(state[name],1,new_index)
        else:
            name = 'conv'+str(l+2)+'.weight'
            state[name] = torch.index_select(state[name],1,index)
    else:
        name = 'linear'+str(l-5)+'.weight'
        state[name] = torch.index_select(state[name],0,index)
        name = 'linear'+str(l-5)+'.bias'
        state[name] = torch.index_select(state[name],0,index)
        name = 'linear'+str(l-4)+'.weight'
        state[name] = torch.index_select(state[name],1,index)
    return state

