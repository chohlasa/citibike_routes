# This script takes the parsed bikeroutes (which are simply pairs of
# lat/long points) and first filters out all the duplicates. This
# includes lines with two identical endpoints (adds the ridecount),
# and lines in opposite directions but two identical endpoints (adds
# the ridecount).

# Input file: 'processed_data/coordinate_pairs.csv'
# Output file: 'processed_data/coordinate_pairs_flattened.csv'

import pandas as pd
pd.set_option('display.width', 1000)

# JOINING LINES

# Starting with lines with same start and end points
pairs = pd.io.parsers.read_table('coordinate_pairs.csv', sep=',')
print pairs[pairs['start_lat'] == 40.71210]
print "The output above..."
print "Should be much longer than the output below."
pairs = pairs.groupby(['start_lat','start_long','end_lat','end_long']).sum()
pairs["index"] = pairs.reset_index().index
print pairs[pairs.index.get_level_values('start_lat') == 40.71210]

# Much more complicated: matching lines with inverted identical start
# and end points
print "\nThese are the reverse pairs from the same point."
print pairs[pairs.index.get_level_values('end_lat') == 40.71210]

inv_pairs = pairs.copy()
inv_pairs.reset_index(inplace=True)
inv_pairs.columns = ['end_lat', 'end_long', 'start_lat', \
                          'start_long', 'ride_count', 'index']
inv_pairs.set_index(['start_lat', 'start_long', 'end_lat', 'end_long'], \
                         inplace=True)
merged_df = inv_pairs.join(pairs, how="inner", rsuffix="_orig", lsuffix="_inv")
merged_df = merged_df[merged_df['index_orig'] < merged_df['index_inv']]

# print merged_df[merged_df.index.get_level_values('start_lat') == 40.71210]
# print merged_df[merged_df.index.get_level_values('end_lat') == 40.71210]

pairs = pairs[~pairs['index'].isin(merged_df['index_inv'])]
merged_df = merged_df.drop(['index_inv', 'ride_count_orig', 'index_orig'], axis=1)
pairs = pairs.join(merged_df, how="left")
pairs = pairs.fillna(0)
pairs['ride_count'] = pairs['ride_count'] + pairs['ride_count_inv']
pairs = pairs.drop(['ride_count_inv', 'index'], axis=1)

pairs = pairs.reset_index()
pairs.sort('ride_count', ascending=True, inplace=True)
#print pairs
pairs.to_csv('processed_data/coordinate_pairs_flattened.csv', index=False)
