# this script analyzes the monthly aggregated report from biz_dashboard
"""
1. read all files in current directory
2. find the line with the specific appid (input from command line)
3. read the corresponding install/events value
4. put together as a monthly trend
"""

import os
import pandas as pd
import sys
import csv


def parse_file(path, appid):
    df = pd.read_csv(path)
    if appid == 0: # if appid = 0, return total number of events in this file
        total = 0
        for i in range(len(df)):
            total += int(df.ix[i]['In-App Events'].replace(',','')) # to correctly handle comma-separated int
        return total

    for i in range(len(df)):
        if df.ix[i]['App Name'] == appid: # App Name
            value = df.ix[i]['In-App Events']  # In-App Events
            return value
    return 0


filepaths = os.listdir('.')  # all files in the current directory

with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    index = []

    # construct the headers of the file, and write as the first row
    index.append('AppId')
    for i in range(1, 13):
        index.append(str(i))
    writer.writerow(index)

    if len(sys.argv) > 1: # if we have at least one input from commandline
        for appid in sys.argv[1:]:
            output = [appid]
            for i in range(1, 13): # construct the initial output line
                output.append('0')
            for filepath in filepaths:
                if filepath.endswith('.csv'):
                    if filepath[:filepath.index('.csv')] in index: # the file name without .csv, which should be a month in numbers
                        path = filepath
                        value = parse_file(path, appid)
                        output[int(filepath[:filepath.index('.csv')])] = str(value)

            writer.writerow(output)

        # write total number of events as the last row
        output = ['Total events']
        for i in range(1, 13):  # construct the initial output line
            output.append('0')
        for filepath in filepaths:
            if filepath.endswith('.csv'):
                if filepath[:filepath.index('.csv')] in index:  # the file name without .csv, which should be a month in numbers
                    path = filepath
                    value = parse_file(path, 0)
                    output[int(filepath[:filepath.index('.csv')])] = str(value)
        writer.writerow(output)
