# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 04:19:38 2019

@author: Owner
"""
from arcgis.gis import GIS
from arcgis.geocoding import reverse_geocode,geocode
gis = GIS("https://www.arcgis.com", "kagerou123", "11Kagerou11")
from geojson import Point, Feature, FeatureCollection, dump
import ast
import json 

def getReversed(lon,lat):
    revGeoDict = reverse_geocode([lon,lat],distance=1,return_intersection=True)
    return revGeoDict.get('address').get('ShortLabel')

def topLandmarkInClustDict(lmDict):
    unsortedList = []
    for key in lmDict.keys():
        pair = key, lmDict[key]
        unsortedList.append(pair)
    unsortedList.sort(key=lambda x:x[1])
    #print("SortedList: ",unsortedList)
    return unsortedList[-1]

path = "\\Users\\Owner\\Desktop\\PythonCodes\\ML_Project\\FINAL_HBSCAN_125p_c.geojson"
with open(path) as f:
  features_list = json.load(f)["features"]
  clusterDict = {}
  
  for feature in features_list:
      point = (feature['geometry']['coordinates'][0],
                feature['geometry']['coordinates'][1])
      clusterID = feature['properties']['CLUSTER_ID']
      landmark_name = ''
      if (clusterID != -1): #ignores -1 clusters
          landmark_name = getReversed(*point)
          if(clusterDict.get(clusterID) == None): #init cluster in dict
              clusterDict[clusterID] = {landmark_name : 1}
          else:
              landmark_dict = clusterDict[clusterID]
              if(landmark_dict.get(landmark_name) == None): #landmark not within dict
                  landmark_dict[landmark_name] = 1
              else:
                  landmark_dict.update({landmark_name:landmark_dict[landmark_name]+1})

#print(clusterDict)     
topLandmarksInClusters = []
     
for key in clusterDict.keys():
    clusterTopLandmark = topLandmarkInClustDict(clusterDict[key])
    #print(clusterTopLandmark)
    topLandmarksInClusters.append(clusterTopLandmark)

n=5
topLandmarksInClusters.sort(key=lambda x:x[1])
topNLandmarks = list((map(lambda x: x[0] ,
                     topLandmarksInClusters[len(topLandmarksInClusters)-n:])))
print(topNLandmarks)

point_feature_collection_list = []
for landmark in topNLandmarks:
    intersectionAddress = {'Address' : landmark,
                           'City' : 'Porto',
                           'Country': 'PRT'}
    point = geocode(intersectionAddress)[0]['location']
    coordinate = [point['x'],point['y']]
    featurePoint = Point(coordinate)
    landmark_feature = Feature(geometry = featurePoint ,
                                           properties = {})
    point_feature_collection_list.append(landmark_feature)


fc = FeatureCollection(point_feature_collection_list)
outputPath = "\\Users\\Owner\\Desktop\\PythonCodes\\ML_Project\\FINAL_traj_5_landmarks_HBclusters_125p_c.geojson"
with open(outputPath, 'w') as f:
   dump(fc, f)
    
