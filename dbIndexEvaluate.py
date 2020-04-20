# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 01:44:32 2019

@author: Owner
"""
import json
from sklearn.metrics import davies_bouldin_score
import numpy as np
import utm
from sklearn import metrics

path = "\\Users\\Owner\\Desktop\\PythonCodes\\ML_Project\\FINAL_DBSCAN_200M_250p_c.geojson"
with open(path) as f:
  features_list = json.load(f)["features"]
  points = []
  labels = []
  
  for feature in features_list:
      input_lat,input_lon = [feature['geometry']['coordinates'][0],
                feature['geometry']['coordinates'][1]]
      utmTup = utm.from_latlon(input_lat, input_lon)
      point = [utmTup[0],utmTup[1]]

      clusterID = feature['properties']['CLUSTER_ID']
      points.append(point)
      labels.append(clusterID)

X = np.array(points)
labels = np.array(labels)
#print(X)
#print(labels)
print("FINAL_HDBSCAN_125p_c")
print("Davies-Bouldin Index: ",davies_bouldin_score(X, labels))
print("Calinski-Harabasz: ",metrics.calinski_harabasz_score(X, labels))
print("Silhouette Score: ",metrics.silhouette_score(X, labels, metric='euclidean'))