# CS 655 Final Project
# Iden Kalemaj, Andrea Burns, Gavin Brown

# Script to read in results text files and produce plots

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')
import sys
import re

def read_in_csv(filename):
    """read in the results of one experiment, saved in the CSV"""
    out = []
    with open(filename, 'r') as f:
        results = [line.split(',') for line in f.read().splitlines()]

    # remove the non-numbers from the file name
    p = re.compile('\D') # \D matches all non-decimals, equivalent to [^0-9]
    results = [[int(p.sub('', result[0])), int(result[1]), float(result[2])] for result in results]

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

# Table results
if True:
    starting_experiment = 4
    num_runs = 3 
    times = np.zeros(num_runs)
    for run in range(num_runs):
        filename = "../results/results_experiment"+str(starting_experiment)+'_run'+str(run)+'.csv'
        results = read_in_csv(filename)
        times[run] = average_time(results)
    # report out average
    print('uniform, cache=30, average')
    print(np.mean(times))
    print()

    starting_experiment = 0
    num_runs = 3 
    times = np.zeros(num_runs)
    for run in range(num_runs):
        filename = "../results/results_experiment"+str(starting_experiment)+'_run'+str(run)+'.csv'
        results = read_in_csv(filename)
        times[run] = average_time(results)
    # report out average
    print('power, cache=30, average')
    print(np.mean(times))
    print()

    starting_experiment = 1
    num_runs = 3 
    times = np.zeros(num_runs)
    for run in range(num_runs):
        filename = "../results/results_cache15_experiment"+str(starting_experiment)+'_run'+str(run)+'.csv'
        results = read_in_csv(filename)
        times[run] = average_time(results)
    # report out average
    print('uniform, cache=15, average')
    print(np.mean(times))
    print()

    starting_experiment = 0
    num_runs = 3 
    times = np.zeros(num_runs)
    for run in range(num_runs):
        filename = "../results/results_cache15_experiment"+str(starting_experiment)+'_run'+str(run)+'.csv'
        results = read_in_csv(filename)
        times[run] = average_time(results)
    # report out average
    print('power, cache=15, average')
    print(np.mean(times))
    print()



# Plot 1
# accuracy and error probability
if False:
    starting_experiment = 4
    num_exp = 4
    num_runs = 3 
    accs = np.zeros((num_exp, num_runs))
    probs = [0.0, 0.1, 0.2, 0.3]
    for exp in range(num_exp):
        for run in range(num_runs):
            filename = "../results/results_experiment"+str(starting_experiment+exp)+'_run'+str(run)+'.csv'
            print(filename)
            results = read_in_csv(filename)
            accs[exp, run] = accuracy(results, labels)

    # plot as lines
    plt.plot(probs, np.mean(accs, axis=1), 'b--', label='Average')
    #plt.xlabel('Probability of Error')
    #plt.ylabel('Average Accuracy')
    #plt.title('Prediction Accuracy and Classifier Error')
    #plt.savefig('plot_1_single_line.png')

    # plot both points and lines
    for run in range(num_runs):
        plt.plot(probs, accs[:, run], 'bo')
    plt.xlabel('Probability of Error')
    plt.ylabel('Accuracy')
    plt.title('Prediction Accuracy and Classifier Error')
    plt.legend()
    plt.savefig('plot_1_final.png')
    plt.clf()

# Plot 2
# same as above, except random delay
if False:
    starting_experiment = 8
    num_exp = 4
    num_runs = 3 
    accs = np.zeros((num_exp, num_runs))
    probs = [0.1, 0.2, 0.3, 0.4]
    for exp in range(num_exp):
        for run in range(num_runs):
            filename = "../results/results_experiment"+str(starting_experiment+exp)+'_run'+str(run)+'.csv'
            results = read_in_csv(filename)
            accs[exp, run] = accuracy(results, labels)


    # plot individual points


# Plot 1
# accuracy and error probability
if False:
    starting_experiment = 4
    num_exp = 4
    num_runs = 3 
    accs = np.zeros((num_exp, num_runs))
    probs = [0.0, 0.1, 0.2, 0.3]
    for exp in range(num_exp):
        for run in range(num_runs):
            filename = "../results/results_experiment"+str(starting_experiment+exp)+'_run'+str(run)+'.csv'
            print(filename)
            results = read_in_csv(filename)
            accs[exp, run] = accuracy(results, labels)

    # plot as lines
    plt.plot(probs, np.mean(accs, axis=1), 'b--', label='Average')
    #plt.xlabel('Probability of Error')
    #plt.ylabel('Average Accuracy')
    #plt.title('Prediction Accuracy and Classifier Error')
    #plt.savefig('plot_1_single_line.png')

    # plot both points and lines
    for run in range(num_runs):
        plt.plot(probs, accs[:, run], 'bo')
    plt.xlabel('Probability of Error')
    plt.ylabel('Accuracy')
    plt.title('Prediction Accuracy and Classifier Error')
    plt.legend()
    plt.savefig('plot_1_final.png')
    plt.clf()

# Plot 2
# same as above, except random delay
if False:
    starting_experiment = 8
    num_exp = 4
    num_runs = 3 
    accs = np.zeros((num_exp, num_runs))
    probs = [0.1, 0.2, 0.3, 0.4]
    for exp in range(num_exp):
        for run in range(num_runs):
            filename = "../results/results_experiment"+str(starting_experiment+exp)+'_run'+str(run)+'.csv'
            results = read_in_csv(filename)
            accs[exp, run] = accuracy(results, labels)


    # plot individual points
    for run in range(num_runs):
        plt.plot(probs, accs[:, run], 'bo')
    #plt.savefig('plot_2_points.png')

    # plot lines and points
    plt.plot(probs, np.mean(accs, axis=1), 'b--', label='Average')
    plt.xlabel('Mean Random Delay')
    plt.ylabel('Accuracy')
    plt.title('Random Delay and Classifier Error')
    plt.legend()
    plt.savefig('plot_2_final.png')
    plt.clf()

# Plot 3
# same as above, except random delay and time 
if False:
    starting_experiment = 8
    num_exp = 4
    num_runs = 3 
    times = np.zeros((num_exp, num_runs))
    probs = [0.1, 0.2, 0.3, 0.4]
    for exp in range(num_exp):
        for run in range(num_runs):
            filename = "../results/results_experiment"+str(starting_experiment+exp)+'_run'+str(run)+'.csv'
            results = read_in_csv(filename)
            times[exp, run] = average_time(results)

    # plot individual points
    for run in range(num_runs):
        plt.plot(probs, times[:, run], 'bo')
    #plt.savefig('plot_2_points.png')

    # plot lines and points
    plt.plot(probs, np.mean(times, axis=1), 'b--', label='Average')
    plt.xlabel('Mean Random Delay')
    plt.ylabel('Avg. Comm. Time (s)')
    plt.title('Random Delay and Communication Time')
    plt.legend()
    plt.savefig('plot_3_final.png')
    plt.clf()

































