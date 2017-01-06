# This script analyzes the raw data exported from Biz dashboard

"""
1. Identify the newly listed account in the raw data exported from Biz dashboard
    - Assume the directory contains monthly top1000 accounts. Files are named by the month (e.g., 8_account.csv refers to the data of August)
    - Take the first month (lowest number in filename) as the starting point, output account based on the pre-defined criteria
        - Rising star: newly appear in top100 for two consecutive months
        - Rock star: stay in top10 for two consecutive months
        - Decline clients: top100 clients, traffic drops 50% or more in two consecutive months
        - Organic clients: Organic installs > 2M for two consecutive months

"""

"""
Logic flow
1. Scan all files in the directory, identify the sequence of file opening by their names
2. Open the first file, store top100 and top10 in as base
3. For each file open, determine if there is any star according to our criteria
"""


import os
import csv

# read topN from a given file, and return the name and Non-organic / Organic installs
def read_topN(reader, N, read_organic):
    names = []
    installs = []
    index = 0
    for row in reader:
        if index == 0:
            index = 1
        else:
            names.append(row[1])
            if read_organic == True:
                installs.append(row[5]) # 6th column, Organic installs
            else:
                installs.append(row[3]) # 4th column, Non-organic installs
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
    (top100, installs) = read_topN(reader, 100, False)
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
    (top10, installs) = read_topN(reader, 10, False)
    if not top10: # first month
        pass
    else:
        for name in top10:
            if name in top10_1:
                print("  Found a Rock Star: " + name)
    top10_1 = top10

# task 3: Find clients whose traffic declines a lot (e.g., 50%)
top1000_1 = [] # all accounts of the previous month
top1000_installs_1 = []
top1000_2 = [] # all accounts of the month before previous
top1000_installs_2 = []

def decline(name, install, names, installs, percentage):
    for (n, i) in zip(names, installs):
        if name == n:
            if float(i.replace(',', ''))/float(install.replace(',', '')) <= percentage:
                return True
            break
    return False

def decline_clients(f):
    global top1000_1
    global top1000_2
    global top1000_installs_1
    global top1000_installs_2
    reader = csv.reader(f)
    (top1000, installs) = read_topN(reader, 1000, False)
    if not top1000_1 or not top1000_2:
        pass
    else:
        for (name, install) in zip(top1000_2[:100], top1000_installs_2[:100]):
            if decline(name, install, top1000_1, top1000_installs_1, 0.5) and decline(name, install, top1000, installs, 0.5):
                print("  Declined 50% for two months: " + name)

    top1000_2 = top1000_1
    top1000_1 = top1000
    top1000_installs_2 = top1000_installs_1
    top1000_installs_1 = installs


# task 4: Find clients with Organic installs more than 2M for two consecutive months
organic1000_1 = []
organic1000_installs_1 = []

def organic_clients(f):
    METRIC = 2000000
    global organic1000_1
    global organic1000_installs_1
    reader = csv.reader(f)
    (top1000, installs) = read_topN(reader, 1000, True)
    if not organic1000_1:
        pass
    else:
        for (name, install) in zip(top1000, installs):
            if int(install.replace(',', '')) > METRIC:
                for (name1, install1) in zip(organic1000_1, organic1000_installs_1):
                    if name1 == name and int(install1.replace(',', '')) > METRIC:
                        print("  Organic > 2M for two months: " + name)
                        break
    organic1000_1 = top1000
    organic1000_installs_1 = installs


# ---------------------------
# Main function starts here
# ---------------------------
filepaths = os.listdir('.')  # all files in the current directory

# create a sorted list for file opening
filenames = {}
for filepath in filepaths:
    if filepath.endswith('.csv'):
        result = filepath[:-4].split('_')  # get rid of '.csv', then split on '_'
        if len(result) == 2:
            num_in_name = result[0]
            if int(num_in_name) in range(13): # a number indicates a month
                filenames[int(num_in_name)] = filepath

for key in sorted(filenames.keys()):
    filename = filenames[key]
    with open(filename, newline='', encoding='utf-8') as f:
        print("Processing " + "2016." + str(key))
        # rock_star(f)
        # rising_star(f)
        # decline_clients(f)
        organic_clients(f)