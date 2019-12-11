# distributed-ensemble-project

## Introduction

Hello! 
This is the Github repository for the CS 655 final project of Andrea Burns, Gavin Brown, and Iden Kalemaj, for Fall 2019.
Everything you need (and more) should be in this repository, but feel free to contact us if you have any questions.


## Downloading and Setting Up

In the "setup_and_installation" folder, you will find instructions for setup, installation, and operation.
In particular, you will find a GENI Rspec and a detailed step-by-step document for duplicating our results.
In addition, there are two scripts (setup_1.sh and setup_2.sh) that automatically download and install this repository and its requirements.

## Repository Structure

Here is a guide to the top-level folders in this repository:
* `client`, `manager`, and `classifier` hold the code used in operating the system.
* `document` contains the report and associated files.
* `results` contains low-level results saved by our machines, in CSV format.
* `analysis` contains scripts used to produce plots and statistics.
* As we said above, `setup_and_installation` provides tools and instructions for you to operate our system.

## To-Do List

Here are some things that need done.
* Implementation
  1. Test our ability to run multiple experiments automatically.
  3. Do we want to submit a simplified version that excludes the ability to rerun experiments?
* Report
  1. Final proof-reading
  2. Add screenshots to usage instructions
* Supplementary Materials, incl. stuff for report
  1. Video demo
  2. Rspec (put on github)
  3. Screenshots to show how it works
  4. Scripts to wget everything. But make them install it, if that's easier for us.
  5. Instructions for running an experiment.

Here are things we've put on the list that have been finished:
1. Adding FSMs
2. Adding explicit learning outcomes.
2. Write code to generate plots.

