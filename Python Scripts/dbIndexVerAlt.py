import json
from sklearn.metrics import davies_bouldin_score
import numpy as np

path = "\\Users\\Owner\\Desktop\\PythonCodes\\ML_Project\\FINAL_DBSCAN_100M_100p_c.geojson"
with open(path) as f:
  features_list = json.load(f)["features"]
  clusterDict = {}
  
  for feature in features_list:
      point = [feature['geometry']['coordinates'][0],
                feature['geometry']['coordinates'][1]]
      clusterID = feature['properties']['CLUSTER_ID']
      if(clusterDict.get(clusterID) == None):
          clusterDict[clusterID] = [point]
      else:
          pointsList = clusterDict[clusterID]
          pointsList.append(point)
          clusterDict.update({clusterID: pointsList})
X = []
labels = []

for key in clusterDict.keys():
    X.append(clusterDict[key])
    labels.append(key)
labels = np.array(labels) 
print(X)
print(labels)
davies_bouldin_score([], labels)