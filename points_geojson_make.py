# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 20:30:57 2019

@author: Owner
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 02:14:01 2019

@author: Owner
"""

from geojson import MultiPoint, Feature, FeatureCollection, dump
import json
import ast
import sys

def getData(path):
    traj_feature_collection_list = []
    with open(path) as userInput:
        count = 0
        for line in userInput:
            if (count>2):
                inputData = ast.literal_eval(line)
                trip_id = inputData[0]
                trajectory = ast.literal_eval(inputData[8].strip('\''))
                points_string_format = [(float(coord[0]),float(coord[1])) for coord in trajectory]
                points_string = MultiPoint(points_string_format)
                traj_feature = Feature(geometry = points_string ,id = int(trip_id))
                traj_feature_collection_list.append(traj_feature)
            count+=1
            if count>1000: break
             
    return FeatureCollection(traj_feature_collection_list)
            
rawDataPath = "\\Users\\Owner\\Desktop\\ml-project\\train.csv"
outputPath = "\\Users\\Owner\\Desktop\\PythonCodes\\ML_Project\\unparsed_points.geojson"
taxi_json = getData(rawDataPath)


with open(outputPath, 'w') as f:
   dump(taxi_json, f)