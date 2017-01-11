# this script analyzes the monthly aggregated report from biz_dashboard
"""
It can be used to analyzed monthly reports by app, account, geo, and vertical
1. It scans all CSV files in the current directory
2. It reads an input from command line
3. Plot the monthly trend of the input item across all files
"""

import os
import sys
import csv
import matplotlib.pyplot as plt
import random


OS = 'ios' # "ios", "android", "all"
PLOT = 'install' # what metric to plot: rank, share, or install

# search appid in the given file, return the rank and the share
# if not found, return 0
def process_file(file, appid):
    reader = csv.reader(file)
    # get the index according to column name
    rank_index = 0
    share_index = 0
    install_index = 0
    first = next(reader) # first row
    for i in range(len(first)):
        if '#' in first[i]:
            rank_index = i
        elif '%' in first[i]:
            share_index = i
        elif 'Organic' == first[i]:
            install_index = i

    rank = 0
    share = 0
    install = 0
    for line in reader:
        if line[1] == appid:
            rank = line[rank_index]
            share = line[share_index]
            install = line[install_index] # non-organic install
            break
    return (rank, share, install)

# value should be of the dictionary format: {appid:(rank, share)}
def plot_figure(index, value, PLOT):
    for key in value.keys():
        if PLOT == 'share': # Y axis plot based on percentage
            plt.plot(index, value[key][1])
            for (x, share) in zip(index, value[key][1]):
                plt.text(x, random.uniform(0.95,1)*share, str(share))
        elif PLOT == 'rank': # Y axis plot based on ranking
            plt.plot(index, value[key][0])
            for (x, rank) in zip(index, value[key][0]):
                plt.text(x, random.uniform(0.92, 1)*rank, str(rank))
        elif PLOT == 'install':
            plt.plot(index, value[key][2])
            for (x, install) in zip(index, value[key][2]):
                plt.text(x, random.uniform(0.94, 1)*install, str(install))

    if PLOT == 'rank':
        plt.gca().invert_yaxis()  # invert Y axis to better display ranking
    plt.legend(value.keys(), loc=4)
    plt.show()


def scan_files(OS):
    filepaths = os.listdir('.')  # all files in the current directory
    filenames = {}
    for filepath in filepaths:
        if filepath.endswith('.csv'):
            result = filepath[:-4].split('_')  # get rid of '.csv', then split on '_'
            if len(result) > 2 and int(result[-1]) in range(13) and result[-2] == OS:  # last element is a month and of the right OS
                filenames[int(result[-1])] = filepath
            elif OS == 'all' and len(result) == 2: # Don't distinguish OS, so will process files like "1_account.csv"
                filenames[int(result[0])] = filepath

    return filenames

# read topN from a given file, and return the name
def get_topN(reader, N):
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

# --------------------------
# Main function starts here
# --------------------------

# read input from command line
if len(sys.argv) > 1: # if we have at least one input from commandline
    Y = {}
    for appid in sys.argv[1:]:
        index = []
        ranks = []
        shares = []
        installs = []
        filenames = scan_files(OS)
        for key in sorted(filenames.keys()):
            filename = filenames[key]
            index.append(key)
            with open(filename, newline='', encoding='utf-8') as f:
                print("Processing " + "2016." + str(key))
                (rank, share, install) = process_file(f, appid)
                ranks.append(int(rank))
                shares.append(float(share.replace('%', '')))
                installs.append(int(install.replace(',', '')))
        Y[appid] = (ranks, shares, installs)
    plot_figure(index, Y, PLOT)





