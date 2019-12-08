# delete me later

import sys

from neural_network import load_network, classify

with open('../true_labels.csv') as f:
    truth = [line.split(',') for line in f.read().splitlines()]

net = load_network()
N = 10
correct = 0

for i in range(N):
    print('Image     :', i)
    prediction = classify(net, '../images/image'+str(i)+'.jpeg', 0, 0)
    print("Predicted :", prediction)
    print('Actual    :', truth[i][1], end='')
    if str(prediction)==truth[i][1]:
        correct += 1
        print('   Correct!')
    else:
        print()
    print('--------------------------------')

print('--------------------------------')
print('Accuracy: ', 100*correct/N)
print('--------------------------------')
