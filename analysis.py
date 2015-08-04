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

data = []
titles = []
with open('summaryData.csv','rb') as infile:
	reader = csv.reader(infile, delimiter=',')
	next(reader, None)
	for row in reader:
		# print row
		titles.append(row[0] + " - " + row[1])
		data.append(row[2])

# print type(data)
# print type(data[0])





### STEM AND VECTORIZE
### STOPWORD REMOVAL


# stemmed_data = [" ".join(SnowballStemmer("english", ignore_stopwords=True).stem(word)  
#          for sent in sent_tokenize(desc)
#          for word in word_tokenize(sent))
#          for desc in data]

# pickle.dump(stemmed_data, open("stemmed_data.pckl", "wb"))


stemmed_data = pickle.load(open("stemmed_data.pckl", "rb"))

print stemmed_data[0]


vectorizer = TfidfVectorizer(stop_words='english', min_df=0.0,max_df=0.09, ngram_range=(1,2))
vectors = vectorizer.fit_transform(stemmed_data)

print vectors[0]

# print (vectorizer.get_feature_names()[281])













k = 50
U,s,V = linalg.svds(vectors,k,which='LM')
print U.shape, V.shape, s.shape
print s[::-1]

Xk = U*sp.sparse.diags(s,0)

print Xk[]

# print V.shape	
# print V[:,0]
# print V.shape[1]

plt.plot(s)
plt.show()

'''
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
		sw.writerow(data) #[titles[i], Xk[i,0], Xk[i,1], Xk[i,2], Xk[i,3], Xk[i,4], Xk[i,5], Xk[i,6]])
'''