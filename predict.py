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

episode = []
data = []
with open('episodeTopicData.csv','rb') as infile:
	reader = csv.reader(infile, delimiter=',')
	next(reader, None)
	for row in reader:
		episode.append(row[0])
		data.append(row[1:])

# print episode[133]
# 133
# 2510
# 4883
# 473
# 994
ind = 153
target = data[ind] #data[133]
print episode[ind]

D = pairDist(target, data)
Dt = D.transpose()

m = .5
results = []
for i in range(len(Dt)):
	if Dt[i] <= m:
		results.append([Dt[i], episode[i], i])

numR = 30
ordered = sorted(results)#, key=lambda result: results[1])
# results.sort()
for i in range(numR):
	print ordered[i]
	if i == 0:
		standard = data[ordered[i][2]]
	# else:	
		# for x in range(len(data[ordered[i][2]])):
			# print (float(standard[x]) - float(data[ordered[i][2]][x]))


# print len(ordered)