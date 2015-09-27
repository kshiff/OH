'''
Karl Shiffler 
karlshiffler@gmail.com

Script to download podcast information from RSS feed URLs. Currently pulls series title, episode title, description.
'''
import feedparser
import csv
import re
import requests
from bs4 import BeautifulSoup
import simplejson as json

feeds = []

# Read in from list of URLs 
with open('RSS-Feeds_Karl.csv', 'rb') as f: 
	reader = csv.reader(f, delimiter=',')
	next(reader, None)
	for row in reader:
		# print row
		feeds.append(row[2])
	
	
# Write results to file
with open('summaryData.csv','wb') as out:
	sw = csv.writer(out, delimiter=',')
	sw.writerow(['provider', 'episode', 'summary'])
	for link in feeds:
		# print link
		pod = feedparser.parse(link)
		# print pod.bozo

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

			
			print provider
			print episode
			print data
			print "\n----------------------------------------------------------------------\n"
			sw.writerow([provider,episode,data])

