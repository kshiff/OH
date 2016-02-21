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
import os.path
import sys
import argparse


class PodcastAnalyzer(object):
	def __init__(self, dataFile, picklefile=None):
		'''
		Constructor
		'''
		self.dataFile = dataFile
		if picklefile is None:
			self.stemmed_data, self.titles = self.intakeFile(dataFile, 'stemmed_data.pckl')
		else:	
			self.stemmed_data, self.titles = self.intakeFile(dataFile, picklefile)


	def intakeFile(self, filename, stemfile):
		'''
		Intakes a file in CSV format with columns 'Provider', 'Episode', and 'Summary'.

		Args:
			filename (str): name of input file if in same directory as script, full/relative path otherwise.
			stemfile (str): name of Pickle file containing stemmed data or the desired name of Pickle file if stemming needs to be performed.

		Returns:
			tuple: contains list containing stemmed words, list containing titles
		'''
		data = []
		titles = []
		#summaryData.csv
		with open(filename,'rb') as infile:
			reader = csv.reader(infile, delimiter=',')
			next(reader, None)
			for row in reader:
				# print row
				titles.append(row[0] + " - " + row[1])
				data.append(row[2])

		if os.path.isfile(stemfile):
			stemmed_data = pickle.load(open(stemfile, "rb"))
		else:	#"stemmed_data.pckl"
			stemmed_data = [list(gensim.utils.lemmatize(desc, stopwords=STOPWORDS))
			for desc in data]
			pickle.dump(stemmed_data, open(stemfile, "wb"))
			
		return (stemmed_data, titles)



	def iter_desc(self, x):
		'''
		Generator for descriptions

		'''
		for y in range(len(self.stemmed_data[x])):
			edited = self.stemmed_data[x][y].split("/")[0]
			yield edited #stemmed_data[x][y]



	def fit_model(self, min_df, max_df, ngram_range, k):
		'''
		Fits and applies a TFiDF vectorizer, then computes SVD of the vectors.

		Args:
			min_df (float): minimum document frequency. Used to exclude very rare words so not to unduly influence the system.
			max_df (floar): maximum document frequency. Used to exclude corpus-specific stop words. For example, podcast descriptions
				may excessively include 'episode.'
			ngram_range (tuple): the size of ngrams you're looking for. Groups words into phrases, e.g., 'White House' rather 
				than 'white' and 'house'.
		
		Returns:
			tuple: Contains U, s, and V matricies and Xk list and feature name list, in that order 
		'''

		list_data = []
		for p in range(len(self.stemmed_data)):
			list_data.append(" ".join(self.iter_desc(p)))

		# print list_data[0], ' ', len(list_data)

		# vectorizes descriptions
		vectorizer = TfidfVectorizer(stop_words='english', min_df=min_df, max_df=max_df, ngram_range=ngram_range) 
		vectors = vectorizer.fit_transform(list_data)

		feature_names = vectorizer.get_feature_names()
		#print len(feature_names)

		U,s,V = linalg.svds(vectors,k,which='LM')
		# print U.shape, V.shape, s.shape
		# print s[::-1]

		Xk = U*sp.sparse.diags(s,0)

		# print Xk[0]

		# print V.shape	
		# print V[:,0]
		# print V.shape[1]

		# plt.plot(s)
		# plt.show()
		return (U,s,V,Xk, feature_names)


	def writeData(self, topicWordFile, episodeTopicFile, dataTuple):
		'''
		Writes data to CSVs for computing similarities.

		Args:
			topicWordFile (str): desired name of file containing data coorelating words to 'topics'
			episodeTopicFile (str): desired name of file containing data coorelating episodes to 'topics'
			dataTuple (tuple): Contains U, s, and V matricies and Xk list and feature name list, in that order 
		'''

		U,s,V,Xk,feature_names = dataTuple

		with open(topicWordFile,'wb') as out:
			sw = csv.writer(out, delimiter=',')
			sw.writerow(feature_names)
			for i in range(V.shape[0]):
				sw.writerow(V[i])

		with open(episodeTopicFile,'wb') as out:
			sw = csv.writer(out, delimiter=',')
			sw.writerow(['episode', 'topics'])
			# print len(Xk)
			# print len(self.titles)
			for i in range(len(Xk)):
				data = [self.titles[i]]
				for x in range(Xk.shape[1]):
					data.append(Xk[i,x])
				sw.writerow(data) 


def main(argv):
	desc = 'Commandline python script that allows reading list of podcast URLs and generating a file containing desciptive data'
	parser = argparse.ArgumentParser(description=desc)
	parser.add_argument('podfile', type=str, help='filename of the file containing podcast data')
	#parser.add_argument('--output', '-o', type=str, help='filename the podcast data will be output to')
	args = parser.parse_args()

	pa = PodcastAnalyzer(args.podfile)
	fitData = pa.fit_model(min_df=0.0003,max_df=0.09, ngram_range=(1,3), k=10)
	pa.writeData(topicWordFile='topicWordData.csv',episodeTopicFile='episodeTopicData.csv',dataTuple=fitData)

if __name__ == "__main__":
	main(sys.argv)

