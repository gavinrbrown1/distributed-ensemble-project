# distributed-ensemble-project

## Introduction

Hello! 
This is the Github repository for the CS 655 final project of Andrea Burns, Gavin Brown, and Iden Kalemaj, for Fall 2019.
Everything you need (and more) should be in this repository, but feel free to contact us if you have any questions.


## Downloading and Setting Up

On your local machine, you can access our Rspec [here](https://raw.githubusercontent.com/gavinrbrown1/distributed-ensemble-project/master/setup_and_instructions/ensemble_classifier_rspec.xml)
After setting up the GENI nodes, log into each machine.

To download the file and install dependencies, download and run our setup script on each machine:
```
wget https://raw.githubusercontent.com/gavinrbrown1/distributed-ensemble-project/master/setup_and_instructions/setup.sh
sudo bash setup.sh
```
This will download the rest of the project files and install Anaconda.
You will be prompted for permission a few times; accept the defaults. 
The installation may take a few minutes.
After installing Anaconda, you will need to restart the shell for the changes to take effect.
After reconnecting, install the following Python packages on each machine:
```
conda install pytorch torchvision cpuonly -c pytorch
```
Then everything should be ready to go!

In the `setup_and_installation` folder, you will find a document titled "instructions.pdf"  with detailed step-by-step instructions for operation.
We also have included a video showing the process for starting experiments.

## Repository Structure

Here is a guide to the top-level folders in this repository:
* `client`, `manager`, and `classifier` hold the code used in operating the system.
* the `cache` folder within `manager` must be empty before you begin your initial experiments. It clears itself after each experiment, which is currently set to consist of 200 images (i.e. each experiment contains 200 images total).
* `document` contains the report and associated files.
* `results` contains low-level results saved by our machines, in CSV format.
* `analysis` contains scripts used to produce plots and statistics.
* As we said above, `setup_and_installation` provides tools and instructions for you to operate our system.
