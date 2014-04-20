# This script turns the Google Directions API's "polyline" data into a
# series of pairs of lat/long points. This is necessary for
# aggregating and eventually mapping the routes.

# Input file: 'google_directions_data/directions_records*****_*****'
# Output file: 'processed_data/coordinate_pairs.csv'

import csv
import os

# This function was sourced from the following Gist:
# https://gist.github.com/signed0/2031157
def decode(point_str):
    '''Decodes a polyline that has been encoded using Google's algorithm
    http://code.google.com/apis/maps/documentation/polylinealgorithm.html
    
    This is a generic method that returns a list of (latitude, longitude) 
    tuples.
    
    :param point_str: Encoded polyline string.
    :type point_str: string
    :returns: List of 2-tuples where each tuple is (latitude, longitude)
    :rtype: list
    
    '''
            
    # sone coordinate offset is represented by 4 to 5 binary chunks
    coord_chunks = [[]]
    for char in point_str:
        
        # convert each character to decimal from ascii
        value = ord(char) - 63
        
        # values that have a chunk following have an extra 1 on the left
        split_after = not (value & 0x20)         
        value &= 0x1F
        
        coord_chunks[-1].append(value)
        
        if split_after:
                coord_chunks.append([])
        
    del coord_chunks[-1]
    
    coords = []
    
    for coord_chunk in coord_chunks:
        coord = 0
        
        for i, chunk in enumerate(coord_chunk):                    
            coord |= chunk << (i * 5) 
        
        #there is a 1 on the right if the coord is negative
        if coord & 0x1:
            coord = ~coord #invert
        coord >>= 1
        coord /= 100000.0
                    
        coords.append(coord)
    
    # convert the 1 dimensional list to a 2 dimensional list and offsets to 
    # actual values
    points = []
    prev_x = 0
    prev_y = 0
    for i in xrange(0, len(coords) - 1, 2):
        if coords[i] == 0 and coords[i + 1] == 0:
            continue
        
        prev_x += coords[i + 1]
        prev_y += coords[i]
        # a round to 6 digits ensures that the floats are the same as when 
        # they were encoded
        points.append((round(prev_y, 6), round(prev_x, 6)))
    
    return points


########################################################################

# Get list of Google Directions outputs
filelist = ['google_directions_data/' + x \
             for x in os.listdir('google_directions_data/') \
             if 'directions_records' in x]
print filelist

# Combine all outputs into one list
routes = []
for item in filelist:
    with open(item, 'rU') as openfile:
        routes.extend(list(csv.DictReader(openfile)))

coordinate_pairs = []
for route_ix, route in enumerate(routes):
    if route_ix % 1000 == 0:
        print "At line", route_ix, 'of', len(routes)
    polyline = route['polyline']
    try:
        pairs_list = decode(polyline)
    except:
        print route
    
    for ix, point in enumerate(pairs_list[:-1]): #Don't include last
                                                 #item because you're
                                                 #looking at
                                                 #sequential pairs
        pairs_dict = {}
        pairs_dict['start_lat'] = point[0]
        pairs_dict['start_long'] = point[1]
        pairs_dict['end_lat'] = pairs_list[ix+1][0]
        pairs_dict['end_long'] = pairs_list[ix+1][1]
        pairs_dict['ride_count'] = route['ride_count']
        coordinate_pairs.append(pairs_dict)

with open('processed_data/coordinate_pairs.csv', 'w') as output_file:

    # Set parameters for .csv output file
    header = ['ride_count', 'start_lat', 'start_long', 'end_lat', 'end_long']
    output = csv.DictWriter(output_file, header)
    output.writeheader()

    # Write data to output
    output.writerows(coordinate_pairs)
