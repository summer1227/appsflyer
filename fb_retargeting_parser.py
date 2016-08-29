
''' This script analyzes the reengagement log AF send to FB
    Currently, it count the occurences of ""is_fb":true" in the second column of the tsv file
'''

import os
import pandas as pd

def parse_file(path):
	print ("Parsing ", path)
	# make sure null bytes are replaced. Otherwise will throw exception when processing
	fi = open(path, 'r', encoding='utf-8')
	data = fi.read()
	fi.close()
	fo = open(path+'.tmp', 'w', encoding='utf-8')
	fo.write(data.replace('\x00', ''))
	fo.close()
	
	fb = pd.read_csv(path+'.tmp', header=3, names=['req', 'resp'],usecols=[0,1], delimiter='\t')
	counter = 0
	# read second column, and remove NaN and null
	response = [x for x in list(fb['resp'].dropna()) if x != 'null']
	for r in response:
		if "\"is_fb\":true" in r:
			counter += 1

	return counter
	

filepaths = os.listdir('.') # all files in the current directory
total = 0
for filepath in filepaths:
    if filepath.endswith('.tsv'):
        path = filepath
        total += parse_file(path)
		
print(total)


		

