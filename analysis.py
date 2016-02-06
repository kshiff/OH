'''
Karl Shiffler 
karlshiffler@gmail.com

Script stems and vectorizes descriptions, then computes SVD and outputs feature vectors. 
'''

from sklearn.feature_extraction.text import TfidfVectorizer 
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import csv
import cPickle as pickle
import scipy.sparse.linalg as linalg
import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
import pandas as pd
import seaborn as sns
import gensim
from gensim.parsing.preprocessing import STOPWORDS

data = []
titles = []
with open('summaryData.csv','rb') as infile:
	reader = csv.reader(infile, delimiter=',')
	next(reader, None)
	for row in reader:
		# print row
		titles.append(row[0] + " - " + row[1])
		data.append(row[2])


### STEM AND VECTORIZE
### STOPWORD REMOVAL
# I stem the data once and save it as a pickle object, allowing me to play around with different
# SVD computations without restemming each time.

### comment these three lines after the first time you run it
# stemmed_data = [list(gensim.utils.lemmatize(desc, stopwords=STOPWORDS))
# 	for desc in data]
# pickle.dump(stemmed_data, open("stemmed_data.pckl", "wb"))

### uncomment this line after the first time you run it to save computation time 
### for subsequent runs
stemmed_data = pickle.load(open("stemmed_data.pckl", "rb"))

def iter_desc(x):
	for y in range(len(stemmed_data[x])):
		edited = stemmed_data[x][y].split("/")[0]
		yield edited #stemmed_data[x][y]



list_data = []

for p in range(len(stemmed_data)):
	list_data.append(" ".join(iter_desc(p)))



# vectorizes descriptions
vectorizer = TfidfVectorizer(stop_words='english', min_df=0.0003,max_df=0.09, ngram_range=(1,2))
vectors = vectorizer.fit_transform(list_data)

feature_names = vectorizer.get_feature_names()



# print type(vectors)

### COMPUTING SVD

k = 7 #desired number of features in target vector
U,s,V = linalg.svds(vectors,k,which='LM')
print U.shape, V.shape, s.shape
print s[::-1]

Xk = U*sp.sparse.diags(s,0)

print Xk[0]

# print V.shape	
# print V[:,0]
# print V.shape[1]

# plt.plot(s)
# plt.show()



### SAVING OUTPUT

with open('topicWordData.csv','wb') as out:
	sw = csv.writer(out, delimiter=',')
	sw.writerow(vectorizer.get_feature_names())
	for i in range(V.shape[0]):
		sw.writerow(V[i])

# print Xk[-1]

with open('episodeTopicData.csv','wb') as out:
	sw = csv.writer(out, delimiter=',')
	sw.writerow(['episode', 'topics'])
	for i in range(len(Xk)):
		data = [titles[i]]
		for x in range(Xk.shape[1]):
			data.append(Xk[i,x])
		sw.writerow(data) 
