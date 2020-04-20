from arcgis.gis import GIS
from arcgis.geocoding import reverse_geocode
gis = GIS("https://www.arcgis.com", "kagerou123", "11Kagerou11")
from geojson import Point, Feature, FeatureCollection, dump
import ast
def getReversed(lon,lat):
    revGeoDict = reverse_geocode([lon,lat],distance=1,return_intersection=True)
    return revGeoDict.get('address').get('ShortLabel')

def floatPointToString(s1,s2):
    return (float(s1),float(s2))

def getData(path):
    traj_feature_collection_list = []
    with open(path) as userInput:
        count = 0
        for line in userInput:
            if (count>2):
                inputData = ast.literal_eval(line)
                trajectory = ast.literal_eval(inputData[8].strip('\''))
                dataNotMissing = (inputData[7] == 'False')

                if(dataNotMissing and len(trajectory)>1):
                    trip_id = int(inputData[0])
                    prevPoint = floatPointToString(*trajectory[0])
                    firstFeaturePoint = Point(prevPoint)
                    unixTime = int(inputData[5])
                    firstLandmark = getReversed(*prevPoint)
                    firstProperty = {'timestamp':unixTime,
                                     'landmark':firstLandmark}
                    traj_feature = Feature(geometry = firstFeaturePoint ,
                                           id = trip_id,
                                           properties = firstProperty)
                    #print(traj_feature)
                    traj_feature_collection_list.append(traj_feature)
                    
                    for coord in trajectory[1:]:
                        unixTime+=15
                        point = floatPointToString(*coord)
                        lmPrev,lmPoint = getReversed(*prevPoint), getReversed(*point)
                        if(lmPrev != lmPoint):
                            prevPoint = point
                            traj_point = Point(point)
                            featureProperty = {'timestamp':unixTime,
                                               'landmark':lmPoint}
                            traj_feature = Feature(geometry = traj_point ,
                                                   id = trip_id,
                                                   properties = featureProperty)
                            traj_feature_collection_list.append(traj_feature)
                else: 
                    print(line)
            print(count)
            count+=1
            if count>1020: break
    return FeatureCollection(traj_feature_collection_list)
            
rawDataPath = "\\Users\\Owner\\Desktop\\ml-project\\train.csv"
outputPath = "\\Users\\Owner\\Desktop\\PythonCodes\\ML_Project\\parsed_sample_singleP_1000.geojson"
taxi_json = getData(rawDataPath)

"""
properties: { 
times:[]
landmarks:[]
                 }
"""

with open(outputPath, 'w') as f:
   dump(taxi_json, f)
