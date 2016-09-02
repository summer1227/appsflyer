# This script extracts af_revenue and count the total from in-app events raw data, downloaded from Mojito

import os
import pandas as pd
import re

def parse_file(path):
	file = pd.read_table(path, header=0, delimiter='\t')
	revenue = file['event_value']
	count = 0.0
	for r in revenue:
		# remove \ and " from raw data
		r = re.sub('\\\\|"', "", r)
		m = re.match("(.+)af_revenue:([\d\.]+),", r)
		if m != None:
			count += float(m.group(2))

	return count
	


filepaths = os.listdir('.') # all files in the current directory
total = 0.0

for filepath in filepaths:
    if filepath.endswith('.tsv'):
        path = filepath
        total += parse_file(path)

print(total)