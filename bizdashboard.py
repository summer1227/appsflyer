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

# read topN from a given file, and return the first 2 columns
def read_topN(reader, N):
    names = []
    index = 0
    for line in reader:
        if index == 0:
            index = 1
        else:
            names.append(line[1])
            index += 1
        if index > N:
            break
    return names



# task 1: Rising star
# global variables for this task
top100_1 = [] # store the top100 of the previous month
top100_2 = [] # store the top100 of the month before previous

def rising_star(reader):
    global top100_1
    global top100_2
    top100 = read_topN(reader, 100)
    # if we are still processing for first 2 months, no need for further analysis
    if not top100_1 or not top100_2:
        pass
    else:
        for name in top100:
            if name not in top100_2 and name in top100_1:
                print("  Found a Rising Star: " + name)
    top100_2 = top100_1
    top100_1 = top100


# task 2: Rock star
# global variable for this task
top10_1 = [] # store the top10 of the previous month



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
        print("Processing " + filename)
        reader = csv.reader(f)
        rising_star(reader)

