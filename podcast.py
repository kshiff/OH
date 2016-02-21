'''
Karl Shiffler 
karlshiffler@gmail.com

Command line python script to download podcast information from RSS feed URLs. Currently pulls series title, episode title, description.


'''
import feedparser
import csv
import re
import argparse
from tqdm import tqdm
import sys

def intakeFile(filename):
	'''
	Read in URLs from list file and return list of URLs 

	Args:
		filename (str): name of input file if in same directory as script, full/relative path otherwise

	Returns:
		list: list of URLs
	'''
	feeds = []
	with open(filename, 'rb') as f: 
		reader = csv.reader(f, delimiter=',')
		next(reader, None)
		for row in tqdm(reader):
			if row[3] != 'None':
				feeds.append(row[3])
			else:
				feeds.append(row[2])
	return feeds	
	

def writeData(outfile, feeds):
	'''
	Parses RSS feeds and writes results to file.

	Args:
		outfile (str): name of file to write data to 
		feeds (list): list of URLs to podcasts' RSS feeds

	Returns:
		None
	'''
	errors = []
	with open(outfile,'wb') as out:
		sw = csv.writer(out, delimiter=',')
		sw.writerow(['provider', 'episode', 'summary'])
		for link in tqdm(feeds):
			# print link
			pod = feedparser.parse(link)
			# print pod.bozo
			try:
				provider = pod.feed.title

				provider = provider.encode('ascii','ignore')

				for i in range(len(pod.entries)):
					episode = pod.entries[i].title
					episode = episode.encode('ascii','ignore')

					# check if summary is truncated
					data = pod.entries[i].summary
					# data = pod.entries[0].content[0].value

					data = data.encode('ascii','ignore')
					data = re.sub(r'\n', '', data)
					data = re.sub(r'\<.*?\>', '', data)
					data = re.sub(r'\&.*?\;', '', data)
					data = re.sub(r'\{.*?\}', '', data)
					

					# if data.endswith("[...]"):
					# 	print "truncated"

					
					#print provider
					#print episode
					#print data
					#print "\n----------------------------------------------------------------------\n"
					sw.writerow([provider,episode,data])



			except AttributeError:
				errors.append([pod.feed, link])
	print 'Encountered ' + str(len(errors)) + ' errors in this list.'
	for c in range(len(errors)):
		print errors[c]


def main(argv):
	desc = 'Commandline python script that allows reading list of podcast URLs and generating a file containing desciptive data'
	parser = argparse.ArgumentParser(description=desc)
	parser.add_argument('podfile', type=str, help='filename of the podfile')
	parser.add_argument('--output', '-o', type=str, help='filename the podcast data will be output to')

	args = parser.parse_args()

	feeds = intakeFile(args.podfile)
	writeData(args.output, feeds)

if __name__ == "__main__":
	main(sys.argv)



