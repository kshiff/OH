'''
Karl Shiffler 
karlshiffler@gmail.com

Script generates the similarity matrix. Working on having it produce only half of the
matrix to save computation time.
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

# compute pairwise distances and write to file
with open('simData.csv','wb') as out:
	sw = csv.writer(out, delimiter=',')
	sw.writerow("index")
	for x in range(0,20178):
		print x
		
		ind = x
		target = data[ind] 

		result = [ind]

		D = pairDist(target, data)


		# D = pairDist(target, data[x:])
		# also switch direction of for loop
		# thereby halving the amount of calculations


		# Dt = D.transpose()
		result += list(D[0])
		# print result

		sw.writerow(result)
		# print result