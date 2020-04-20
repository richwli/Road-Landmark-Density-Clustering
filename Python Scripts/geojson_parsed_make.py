from arcgis.gis import GIS
from arcgis.geocoding import reverse_geocode
gis = GIS("https://www.arcgis.com", "kagerou123", "11Kagerou11")
from geojson import MultiPoint, Feature, FeatureCollection, dump
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
                    prevPoint = floatPointToString(*trajectory[0])
                    unixTime = int(inputData[5])
                    removedDupesTraj = [prevPoint]
                    landmarks = [getReversed(*prevPoint)]
                    times = []
                    #debugIntersections = [getReversed(*prevPoint)]
                    for coord in trajectory[1:]:
                        point = floatPointToString(*coord)
                        lmPrev,lmPoint = getReversed(*prevPoint), getReversed(*point)
                        #print("prevPoint: ",prevPoint)
                        #print("point: ", point)
                        #lmPrev,lmPoint = '',''
                        #debugIntersections.append(lm2)
                        if(lmPrev != lmPoint):
                            prevPoint = point
                            removedDupesTraj.append(point)
                            landmarks.append(lmPoint)
                            times.append(unixTime)
                        unixTime+=15
                    featureProperty = {'timestamps':times,'landmarks':landmarks}
                    """      
                    print("unparsed: ",debugIntersections)
                    print('\n')
                    print("parsed: ",intersections)            
                    print('\n')
                    """
                    trip_id = inputData[0]
                    traj_multi_points = MultiPoint(removedDupesTraj)
                    traj_feature = Feature(geometry = traj_multi_points ,id = int(trip_id),properties = featureProperty )
                    traj_feature_collection_list.append(traj_feature)
                #print(traj_feature_collection_list)
                else: 
                    print(line)
            print(count)
            count+=1
            if count>1000: break
             
    return FeatureCollection(traj_feature_collection_list)
            
rawDataPath = "\\Users\\Owner\\Desktop\\ml-project\\train.csv"
outputPath = "\\Users\\Owner\\Desktop\\PythonCodes\\ML_Project\\parsed_points.geojson"
taxi_json = getData(rawDataPath)

"""
properties: { 
times:[]
landmarks:[]
                 }
"""

with open(outputPath, 'w') as f:
   dump(taxi_json, f)
