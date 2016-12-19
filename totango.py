# This script analyzes the raw data exported from Totango

"""
1. According to the pre-defined weight, calculate the quantitative measure of the advancement of the marketer of the app/client.
   The dimensions we currently consider include if the marketer uses (may also include how deep)
   - cohort
   - push (N/A)
   - re-targeting
   - in-app events (N/A)
   - OneLink (N/A)

The columns from the raw data are as follows:
    - Name
    - Account id
    - Status
    - Success Manager
    - Account Sub Status
    - Name of Account
    - Total Installs 30 days (organic, non organic,FB)
    - FB+Non Organic Installs last 60 days
    - dataexport-non_organic_in_app_events (14d)
    - Fraud_Insights (14d)
    - Events (14d)
    - Custom_Dashboard (14d)
    - Cohort (14d)
    - Activity (14d)
    - Retargeting (14d)
    - Retention (14d)
    - RightNow (14d)
    - dataexport-installs (14d)

"""


import os
import csv

# Define the dimensions we will use to calculate the score, and the corresponding weight associated with each dimension
# We define the score as a 100-point metric. So the sum of the weights below should be equal to 100
metrics = {
    'Cohort':40,
    'Retargeting':20,
    'Events':20,
    'Custom_Dashboard':10,
    'Activity':10
}

# calculate the advance score according to the metric defined
"""
line: a row in the raw data, represents an app and its associated information
indices: map each key in "metrics" to its column index in the raw data
"""
def parse_line(line, indices):
    score = 0
    for key in metrics:
        index = indices[key]
        if int(line[index]) > 0: # TODO: consider levels of advance
            score += int(metrics[key])
    return score

# open the file in path, perform the analysis, and write into the output file
def parse_file(path, writer):
    with open(path, newline='') as f:
        reader = csv.reader(f)
        counter = 0
        indices = {} # store the mapping between metrics and the index in csv
        for line in reader:
            if counter == 0: # header line
                for i in range(len(line)):
                    for key in metrics:
                        if key in line[i]:
                            indices[key] = i
                counter += 1
                # output the header line
                line.append('Score')
                writer.writerow(line)
            else:
                score = parse_line(line, indices)
                # output the original line from raw data, plus the score
                output = line
                output.append(str(score))
                writer.writerow(output)


# Main function starts here
filepaths = os.listdir('.')  # all files in the current directory
for filepath in filepaths:
    if filepath.endswith('.csv'):
        with open('output.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            parse_file(filepath, writer)
        break


