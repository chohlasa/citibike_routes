from geojson import Feature, LineString, FeatureCollection, dumps
import csv

with open('processed_data/coordinate_pairs_flattened.csv', 'rU') as pairsfile:
    pairs = list(csv.DictReader(pairsfile))

lines = []
for ix, pair in enumerate(pairs):
    lines.append(Feature(geometry=LineString([(float(pair['start_long']), float(pair['start_lat'])), \
                                              (float(pair['end_long']), float(pair['end_lat']))]), \
                        properties={'ride_count': pair['ride_count']}))

output = FeatureCollection(lines)

with open('geometries/bikeroutes.geojson', 'w') as jsonOutput:
    jsonOutput.write(dumps(output))
