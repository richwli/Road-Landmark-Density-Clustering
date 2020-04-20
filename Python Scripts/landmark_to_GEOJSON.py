import csv
import numpy as np
import operator
from collections import defaultdict
from arcgis.gis import GIS
from arcgis.geocoding import reverse_geocode
from geojson import Feature, Point, FeatureCollection

gis = GIS()
map = gis.map()
data = './train.csv'
trips = defaultdict(lambda: defaultdict(list))
allcoords = []
separated_coords = []
times = []
addressDict = {}

def polyline_converter(polyline, timestamp):
    sep = []
    polyline = polyline.split(']')
    for pair in polyline:
        #print(pair)
        p = pair
        if len(p) < 2:
            continue
        if pair[0] == ',':
            p = pair[2:]
        left = float(p.split(',')[0].replace('[', '').replace(']', ''))
        right = float(p.split(',')[1].replace('[', '').replace(']', ''))
        if -9 < left < -8 and 40 < right < 42:  # there was a weird outlier in the data
            allcoords.append([left, right])
            sep.append([left, right])
    separated_coords.append((sep, timestamp))


with open(data, newline='') as file:
    counter = 0
    reader = csv.reader(file)
    next(file)
    for row in reader:
        counter += 1
        TRIP_ID, CALL_TYPE, ORIGIN_CALL, ORIGIN_STAND, TAXI_ID, TIMESTAMP, DAY_TYPE, MISSING_DATA, POLYLINE = row
        polyline_converter(POLYLINE, TIMESTAMP)
        if counter == 1:  # limit on amount of trips processed
            break

ncoords = np.array(allcoords)

reversed_coords = []
for (trip, time) in separated_coords:
    print("Next trip")
    current_coords = []
    visited = []
    for coordinate in trip:
        results = reverse_geocode(coordinate)
        current_coords.append(results)
        if results['address']['PlaceName'] == '':
            address = results['address']['ShortLabel']
            if address in addressDict and address not in visited:
                addressDict[address][0] += 1
                visited.append(address)
            elif address not in visited:
                addressDict[address] = [1, [results['location']['x'], results['location']['y']]]
                visited.append(address)
    reversed_coords.append((current_coords, time))

print(addressDict)

sorted_d = sorted(addressDict.items(), key=operator.itemgetter(1), reverse=True)

k = 5
landmarks = sorted_d[:k]
print(landmarks)

feature_collection = FeatureCollection([])
for (landmark, coord) in landmarks:
    x = coord[1][0]
    y = coord[1][1]
    to_add = Feature(geometry=Point((x, y)))
    feature_collection['features'].append(to_add)

print(feature_collection)

