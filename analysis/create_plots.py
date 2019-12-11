# CS 655 Final Project
# Iden Kalemaj, Andrea Burns, Gavin Brown

# Script to read in results text files and produce plots

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')

def read_in_csv(filename):
    """read in the results of one experiment, saved in the CSV"""
    with open(filename, 'r') as f:
        results = [line.split(',') for line in f.read().splitlines()]
    for i in range(len(results)):
        results[i][0] = int(results[i][0][13:-4])  # this part depends on how we've saved the image names
        results[i][1] = int(results[i][1])
        results[i][2] = float(results[i][2])
    return results

def get_true_labels():
    """read in the true results CSV"""
    with open('true_labels.csv', 'r') as f:
        raw = [line.split(',') for line in f.read().splitlines()]
    labels = []
    for line in raw:
        labels.append(int(line[1]))
    return labels

def accuracy(results, labels):
    """for single experiment, calculate the fraction of images we correctly classified"""
    total = len(results)
    correct = 0
    for result in results:
        if result[1] == labels[result[0]]:
            correct += 1
    return correct / total

def average_time(results):
    """for single experiment, calculate the average time it took"""
    times = [result[2] for result in results]
    return sum(times) / len(results)

####
# what other functions do we need?
# accuracy given results, average time given results
# then averages over different sets of results

labels = get_true_labels()
print(labels[:10])

## a sample piece of code to plot with 
if False:
    starting_experiment = 1

    cache_size = [10, 25, 50]
    avg_times_uniform = [0.1, 0.1, 0.2]
    avg_times_power = [0.05, 0.75, 0.1]
    plt.plot(cache_size, avg_times_uniform, label='Uniform')
    plt.plot(cache_size, avg_times_power, label='Power Law')
    plt.xlabel('Cache Size')
    plt.ylabel('Avg. Communication Time (s)')
    plt.title('Communication Time and Cache Size')
    plt.legend()
    plt.savefig('comm_time_vs_cache_size.png')

# accuracy and error probability
if True:
    starting_experiment = 0
    num_exp = 6
    num_runs = 10
    total_acc = num_exp*[0]
    probs = [0,1,2,3,4,5]
    for exp in range(num_exp):
        for run in range(num_runs):
            filename = "../results/results_experiment"+str(starting_experiment+exp)+'_run'+str(run)+'.csv'
            results = read_in_csv(filename)
            acc =
            








































