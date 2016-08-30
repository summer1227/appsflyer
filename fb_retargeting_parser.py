
''' This script analyzes the reengagement log AF send to FB
    Currently, it count the occurences of ""is_fb":true" in the second column of the tsv file
'''

import os
import pandas as pd

def parse_file(path, out):
	print ("Parsing ", path)
	# make sure null bytes are replaced. Otherwise will throw exception when processing
	fi = open(path, 'r', encoding='utf-8')
	data = fi.read()
	fi.close()
	fo = open(path+'.tmp', 'w', encoding='utf-8')
	fo.write(data.replace('\x00', ''))
	fo.close()
	
	fb = pd.read_csv(path+'.tmp', names=['req', 'resp', 'payload'], delimiter='\t')
	fb = fb.dropna()
	counter = 0
	# read second column, and remove NaN and null
	# response = [x for x in list(fb['resp'].dropna()) if x != 'null']
	
	for index, row in fb.iterrows():
		if "\"is_fb\":true" in row['resp']:
			counter += 1
			out.write(str(counter) + ":\n")
			out.write("Request: " + row['req'] + "\n")
			out.write("Response: " + row['resp'] + "\n")
			out.write("Payload: " + row['payload'] + "\n")
			out.write("\n")
	return counter
	

filepaths = os.listdir('.') # all files in the current directory
total = 0
out = open("out.txt", 'w', encoding='utf-8')

for filepath in filepaths:
    if filepath.endswith('.tsv'):
        path = filepath
        total += parse_file(path, out)


out.close()

print(total)


		

