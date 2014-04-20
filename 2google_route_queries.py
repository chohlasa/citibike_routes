 # This file takes each station pair and gets a potential bike route
# from the Google Directions API. It requires an API key to
# successfuly run. Put the API key immediately after the filename when
# you execute on the command line.

# Note: because the free Google Directions API only allows 2500
# queries per day, you must incremenetally build up a route index over
# a number of days. This script looks up the existing
# "directions_records" filename with the highest upper limit and
# continues from there. For example, if the file
# "directions_records7149_9648" is in the 'google_directions_data'
# folder, this script will start querying the Google Directions API at
# record index 9649.

# Input file: processed_data/station_pairs_ridecount_sorted.csv
# Output files: google_directions_data/directions_records*****_*****


from urllib2 import urlopen
from json import load
import sys
import os
import csv
import pandas as pd
pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 8)
pd.set_option('display.width', 200)

api_key = sys.argv[1]
baseURL = 'https://maps.googleapis.com/maps/api/directions/json?'

baseURL += '&key=' + api_key
baseURL += '&mode=bicycling'
baseURL += '&alternatives=false'
baseURL += '&sensor=false'

with open('processed_data/station_pairs_ridecount_sorted.csv', 'rU') as openfile:
    pairs_data = list(csv.DictReader(openfile))

prev_outputs = ['google_directions_data' + x for x in os.listdir('./google_directions_data') if 'directions_records' in x]
print prev_outputs
rangeStart = int(prev_outputs[-1].split('_')[-1].split('.')[0]) + 1
numQueries = 2499
print rangeStart
rangeEnd = rangeStart + numQueries
filename = 'google_directions_data/directions_records' + str(rangeStart).zfill(5) + '_' + str(rangeEnd).zfill(5) + '.csv'
print filename

with open(filename, 'w') as openfile:
    openfile.write('orig_ix,start_lat,start_long,end_lat,end_long,polyline,ride_count\n')

    count = 0
    for ix, row in enumerate(pairs_data[rangeStart:]):
        if row['start station id'] != row['end station id'] \
          and count < numQueries:
            count += 1
            print 'Starting row', ix
            print 'Query number', count
            origin = row['start station latitude']+','+row['start station longitude']
            dest = row['end station latitude']+','+row['end station longitude']
            URL = baseURL + '&origin=' + origin
            URL += '&destination=' + dest

            response = urlopen(URL)
            json_obj = load(response)
            
            print len(json_obj['routes'][0]['legs'][0]['steps']), "steps"

            for item in json_obj['routes'][0]['legs'][0]['steps']:
                orig_ix = str(ix)
                start = ',' + str(item['start_location']['lat']) + ',' + \
                  str(item['start_location']['lng'])
                end = ',' + str(item['end_location']['lat']) + ',' + \
                  str(item['end_location']['lng'])
                data =',' + item['polyline']['points'] + ',' + str(row['ride count'])
                openfile.write(orig_ix + start + end + data + '\n')
        elif count >= numQueries:
            break;
