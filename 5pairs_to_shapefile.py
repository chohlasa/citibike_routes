import shapefile
import csv

with open('processed_data/coordinate_pairs_flattened.csv', 'rU') as pairsfile:
    data = list(csv.DictReader(pairsfile))

w = shapefile.Writer(shapeType=3)
w.autoBalance = 1
w.field('ride_count')
w.field('start_lat')
w.field('start_long')
w.field('end_lat')
w.field('end_long')

for pair in data:
    w.poly(parts=[[[float(pair['start_long']),float(pair['start_lat'])], \
                   [float(pair['end_long']),float(pair['end_lat'])]]])
    w.record(pair['ride_count'], pair['start_lat'], pair['start_long'],\
             pair['end_lat'], pair['end_long'])
        
filename = 'bikeroutes_shapefile'
w.save(filename)

# create the PRJ file
prj = open("geometries/%s.prj" % filename, "w")
epsg = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
prj.write(epsg)
prj.close()
