from arcgis.gis import GIS
import sys

rawDataPath = "\\Users\\Owner\\Desktop\\ml-project\\train.csv"
gis = GIS("https://www.arcgis.com", "kagerou100", "11Kagerou11")
m = gis.map()
webmap = gis.content.get('41281c51f9de45edaf1c8ed44bb10e30')

from arcgis.mapping import WebMap
la_parks_trails = WebMap(webmap)

trajectories = []
def getData(path):
    #count = 0
    with open(path) as userInput:
        for line in userInput:
            inputData = line.split("\",\"")
            trajectory = inputData[8]
            trajectories.append(trajectory)
            
            #if count > 10000:
            #    break
            #print(trajectory)
            #count+=1

getData(rawDataPath)
print(sys.getsizeof(trajectories))