# This script analyzes the raw data exported from Biz dashboard

"""
1. Identify the newly listed account in the raw data exported from Biz dashboard
    - Assume the directory contains monthly top1000 accounts. Files are named by the month (e.g., 8_account.csv refers to the data of August)
    - Take the first month (lowest number in filename) as the starting point, output account based on the pre-defined criteria
        - Rising star: newly appear in top100 for two consecutive months
        - Rock star: stay in top10 for two consecutive months

"""

"""
Logic flow
1. Scan all files in the directory, identify the sequence of file opening by their names
2. Open the first file, store top100 and top10 in as base
3. For each file open, determine if there is any star according to our criteria
"""


import os
import csv

# read topN from a given file, and return the name and non-organic installs
def read_topN(reader, N):
    names = []
    installs = []
    index = 0
    for line in reader:
        if index == 0:
            index = 1
        else:
            names.append(line[1])
            installs.append(line[3])
            index += 1
        if index > N:
            break
    return (names, installs)



# task 1: Rising star
# global variables for this task
top100_1 = [] # store the top100 of the previous month
top100_2 = [] # store the top100 of the month before previous

def rising_star(f):
    global top100_1
    global top100_2
    reader = csv.reader(f)
    (top100, installs) = read_topN(reader, 100)
    # if we are still processing for first 2 months, no need for further analysis
    if not top100_1 or not top100_2:
        pass
    else:
        for (name, install) in zip(top100, installs):
            if name not in top100_2 and name in top100_1:
                print("  Found a Rising Star: " + name + " (" + install + ")")
    top100_2 = top100_1
    top100_1 = top100


# task 2: Rock star
# global variable for this task
top10_1 = [] # store the top10 of the previous month

def rock_star(f):
    global top10_1
    reader = csv.reader(f)
    (top10, installs) = read_topN(reader, 10)
    if not top10: # first month
        pass
    else:
        for name in top10:
            if name in top10_1:
                print("  Found a Rock Star: " + name)
    top10_1 = top10

# Main function starts here
filepaths = os.listdir('.')  # all files in the current directory

# create a sorted list for file opening
filenames = {}
for filepath in filepaths:
    if filepath.endswith('.csv'):
        num_in_name = filepath[:filepath.index('_')]
        if int(num_in_name) in range(13): # a number indicates a month
            filenames[int(num_in_name)] = filepath

for key in sorted(filenames.keys()):
    filename = filenames[key]
    with open(filename, newline='', encoding='utf-8') as f:
        print("Processing " + "2016." + str(key))
        # rock_star(f)
        rising_star(f)


