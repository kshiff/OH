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


ind = 20177 #index of episode you want predictions for
			#could change this to be an argument of the script
			#allowing for calls to specific episodes 

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

numR = 30 #number of recommendations you want
ordered = sorted(results)

#print ordered results
for i in range(numR):
	print ordered[i]
	if i == 0:
		standard = data[ordered[i][2]]