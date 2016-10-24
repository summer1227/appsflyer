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
    for i in range(len(df)):
        if df.ix[i]['App Name'] == appid: # App Name
            value = df.ix[i]['In-App Events']  # In-App Events
            return value
    return 0


filepaths = os.listdir('.')  # all files in the current directory

with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    index = []

    index.append('AppId')
    for i in range(1, 13):
        index.append(str(i))

    writer.writerow(index)
    if len(sys.argv) > 1:
        for appid in sys.argv[1:]:
            output = [appid]
            for i in range(1, 13):
                output.append('0')
            for filepath in filepaths:
                if filepath.endswith('.csv'):
                    if filepath[:filepath.index('.csv')] in index:
                        path = filepath
                        value = parse_file(path, appid)
                        output[int(filepath[:filepath.index('.csv')])] = str(value)

            writer.writerow(output)

