# -*- coding: utf-8 -*-
'''
This script is to plot the distribution of the click to install time of the Installation
raw data report on AppsFlyer dashboard
'''
import os
from dateutil.parser import parse
from pandas import DataFrame, Series
import pandas as pd
import matplotlib.pyplot as plt

# time2 - time1
def time_diff(time1, time2):
    result = []
    for (c1,c2) in zip(time1, time2):
        result.append(parse(c2) - parse(c1))
    return result

# process the first csv found. Need to change
filepaths = os.listdir('.') # all files in the current directory
for filepath in filepaths:
    if '.csv' in filepath:
        path = filepath
        break

data = pd.read_csv(path)

''' Plot the click to install time distribution '''
clicks = data['Click Time']
installs = data['Install Time']

diff = time_diff(clicks, installs)

# change from datetime object to actual minutes
diff_min = Series([d.seconds/60 for d in diff])

# Get the value count
diff_min_counter = diff_min.value_counts()

# reindex to make sure no index is missing
click_install_dist = diff_min_counter.reindex(range(0,max(diff_min_counter.index)))

''' Calculate the IP distribution '''
ips = data['IP']
ip_counter = ips.value_counts()

''' Plot '''
plt.subplot(2,1,1)
click_install_dist.plot()
plt.title('Click to Install time distribution')

plt.subplot(2, 1, 2)
ip_counter.plot()
plt.title('IP distribution')

plt.tight_layout()
plt.show()