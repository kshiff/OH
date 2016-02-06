'''
Karl Shiffler 
karlshiffler@gmail.com

Script takes an episode index as input and outputs desired number of recommendations.
'''
import csv
import cPickle as pickle
import scipy.sparse.linalg as linalg
import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics.pairwise import pairwise_distances as pairDist
import operator

# read in data
episode = []
data = []
with open('episodeTopicData.csv','rb') as infile:
	reader = csv.reader(infile, delimiter=',')
	next(reader, None)
	for row in reader:
		episode.append(row[0])
		data.append(row[1:])

avg_list = []
for x in range(0, 177):
	ind = x #20177  #index of episode you want predictions for
				#need to change this to be an argument of the script

	target = data[ind] 
	print episode[ind]

	D = pairDist(target, data)
	Dt = D.transpose()

	m = .5 	# upper limit for most dissimlar episodes you'll include
			# this step could probably be removed
	results = []
	for i in range(len(Dt)):
		if Dt[i] <= m:
			results.append([Dt[i], episode[i], i])

	numR = 5 #number of recommendations you want
	ordered = sorted(results)

	#print ordered results

	l1 = []
	for i in range(numR):
		l1.append(ordered[i][0][0])
		#print ordered[i][0][0], ordered[i][1:]
		if i == 0:
			standard = data[ordered[i][2]]

	avg_list.append(np.average(l1))

print 'Total average = ' + str(np.average(avg_list))