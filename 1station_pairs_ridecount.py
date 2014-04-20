# This script looks at raw CitiBike data and generates counts for each
# pair of CitiBike stations (only where someone actually moved a bike
# between two stations)

# Input files: raw_data/[20**-** - Citi Bike trip data.csv]
# Output file: processed_data/station_pairs_ridecount.csv

import pandas as pd
pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 8)
pd.set_option('display.width', 200)

import os

bikefiles = ['raw_data/' + x for x in os.listdir('raw_data') if 'Citi Bike trip data' in x]

def ridePairs (filename):
    rides = pd.DataFrame.from_csv(filename)
    
    station_pairs = pd.DataFrame(rides.groupby(['start station id', 'end station id'])['starttime'].count())
    station_pairs.columns = ['ride count']

    rides = rides.drop_duplicates(cols=['start station id', 'end station id'])

    month_pairs = rides.join(station_pairs, on=['start station id', 'end station id'], how="left")

    selected_cols = ['start station id', 'start station latitude', 'start station longitude', \
                     'end station id', 'end station latitude', 'end station longitude', 'ride count']
    return month_pairs.sort('ride count', ascending=False)[selected_cols]

print "Starting month", bikefiles[0]
all_pairs = ridePairs(bikefiles.pop(0))

for filename in bikefiles:
    print "Starting month", filename
    all_pairs = pd.concat([all_pairs, ridePairs(filename)])
    print "Done with month", filename

no_sum = ['start station id', 'start station latitude', 'start station longitude', \
          'end station id', 'end station latitude', 'end station longitude']
summed_pairs = all_pairs.groupby(no_sum).sum().sort_index()
print summed_pairs
summed_pairs.to_csv('processed_data/station_pairs_ridecount.csv')
