# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 02:36:44 2019

@author: Owner
"""

from sklearn import datasets
iris = datasets.load_iris()
X = iris.data
from sklearn.cluster import KMeans
from sklearn.metrics import davies_bouldin_score
kmeans = KMeans(n_clusters=3, random_state=1).fit(X)
labels = kmeans.labels_
print(X)
print(labels)
davies_bouldin_score(X, labels)  