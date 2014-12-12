#!/usr/bin/python
import matplotlib.pyplot as plt
from pygmaps_ng import *
import numpy as np
import pdb
import random
import csv

#Read the files and process the information into three different lists
#time, latitude and longitude

def read_file():
	filename = raw_input("File: ")
	fileIn = open(filename, 'r') #Read GPS file with data
	timeArray  = [] 
	latPoints = [] 
	lonPoints = []
	i = j = k = 0
	for line in fileIn.readlines():
		direction = 1 # it is negative if direction is S or W
		dataList = line.split(' ')

		if dataList[0] == 'Format:' or dataList[0] == '\n':
			continue
		elif dataList[0] == 'Time:':
			#Need to do something with the time 
			timeArray.append(dataList[1])
			continue 

		elif dataList[0] == 'Latitude:':
			latitude = dataList[1]
			if len(latitude) < 9:
				continue #Error in the signal 
			latDegrees = float(latitude[:2])
			latFraction = float(latitude[2:])/60
			if dataList[3] == 'S\n' or dataList[3] == 's\n' :
				direction = direction * -1
			latDecimal = (latDegrees + latFraction) * direction #Convert lat point into decimal
			latPoints.append(latDecimal)
			continue

		elif dataList[0] == 'Longitude:':
			longitude = dataList[1]
			if len(longitude) < 10:
				continue #Error in the signal 
			lonDegrees = float(longitude[:3])
	        lonFraction = float(longitude[3:])/60
	        if dataList[3] == 'W\n' or dataList[3] == 'w\n' :
	        	direction = direction * -1

	        lonDecimal = (lonDegrees + lonFraction) * direction #Convert lon point into decimal
	        lonPoints.append(lonDecimal)
	        continue

	fileIn.close()
	return timeArray, latPoints, lonPoints

#Calculate teh centroid of a set of data
def centroid(latPoints, lonPoints):
	xCentroid = sum(latPoints) / len(latPoints)
	yCentroid = sum(lonPoints) / len(lonPoints)

	centre = [xCentroid, yCentroid]

	return centre

#Calculate root mean square error from all the points
def cal_RMSE(latPoints, lonPoints, centroidPoint):

	meanSum = 0.0
	for x, y in zip(range(0, len(latPoints)), range(0, len(lonPoints))):
		meanSum = meanSum + (((latPoints[x] - centroidPoint[0])**2 + (lonPoints[y] - centroidPoint[1])**2))

	return (meanSum/len(latPoints))**(0.5)


#Read initial coordiante from user input or map to plot the base map and 
#then plot the rest of the points 
def plot_points(timePoints, latPoints, lonPoints):
	print " [lat lon] (decimal coordinates) or [none] if you want use coordinate from file"
	inputUser = raw_input("Center Coordinates: ")

	if inputUser == 'none':
		latPlot = float(latPoints[0])
		lonPlot = float(lonPoints[0])
	else:
		points = inputUser.split(' ')
		latPlot = float(points[0])
		lonPlot = float(points[1])
	print latPlot 
	print lonPlot
	#gmap = pygmaps.gmap(latPlot, lonPlot, zoom=16)
	pathTemp = []
	colA = []
	colors = ['000000', '7fffd4', '006400', '483d8b', '8fbc8f', 'b22222', 'ffff00']
	print len(latPoints)
	print len(lonPoints)
	for i in range(0, len(latPoints)-1): #may need to change this one
		temp = (latPoints[i], lonPoints[i])	
		col = random.choice(colors)
		colA.append(col)
		pathTemp.append(temp)

	print "Please add '.csv' to the name"
	csvFile = raw_input("CSV File Name: ")	
	f = open(csvFile, 'wt')
	try:
		writer = csv.writer(f, delimiter='\t')
		writer.writerow(('lat', 'lon', 'color'))
		for i in range(0, len(colA)):
			if i == 0:
				writer.writerow((latPoints[i], lonPoints[i], colors[i]))
			writer.writerow((latPoints[i], lonPoints[i]))
	finally:
		f.close() 
	print "Please add '.html' to the name"
	url = raw_input("HTML File Name: ")	
	#url = 'mymap.draw.html'
	mymap = Map()
	app1 = App('test1',title="Test #1")
	mymap.apps.append(app1)
	
	dataset1 = DataSet('data1', title="Points" ,key_color='000000')
	app1.datasets.append(dataset1)

	for marker in csv2markers(csvFile):
		pt, color, title, text = marker
		dataset1.add_marker(pt,color=color,title=title,text=text)

	center = [latPlot, lonPlot]
	dataset1.add_marker(center,color=colors[6],title='Center',text='Center')
	
	centroidPoint = centroid(latPoints, lonPoints)
	RMSE = cal_RMSE(latPoints, lonPoints, centroidPoint)

	dataset2 = DataSet('Centroid', title="Centroid" ,key_color=colors[5])
	app1.datasets.append(dataset2)
	dataset2.add_marker(centroidPoint,color=colors[5],title='Centroid',text='Centroid RMSE ' + str(RMSE))
	
	mymap.build_page(center=center,zoom=20,outfile=url)
	
	return 

def main():
	timePoints, latPoints, lonPoints = read_file()
	plot_points(timePoints, latPoints, lonPoints)
	return 0
    
if __name__ == "__main__":
	main()
