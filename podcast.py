'''
Script to download podcast information from RSS feed URLs. Currently pulls descriptions and itunes category.
'''
import feedparser
import csv
import re
import requests
from bs4 import BeautifulSoup
import simplejson as json

feeds = []

with open('RSS-Feeds_Karl.csv', 'rb') as f: 
	reader = csv.reader(f, delimiter=',')
	next(reader, None)
	for row in reader:
		# print row
		feeds.append(row[2])

# print feeds
i = 0
for link in feeds:
	response = requests.get(link)
	json = response.text.encode('utf-8')
	soup = BeautifulSoup(json)
	a = soup.find("itunes:category")
	print link
	if a is not None:
		print a['text']
	else:
		i = i+1
		print i
	# pod = feedparser.parse(link)
	# j = str(pod)
	# # print pod
	# j = re.sub(r"{\s*'?(\w)", r'{"\1', j)
	# j = re.sub(r",\s*'?(\w)", r',"\1', j)
	# j = re.sub(r"(\w)'?\s*:", r'\1":', j)
	# j = re.sub(r":\s*'(\w+)'\s*([,}])", r':"\1"\2', j)
	# print j
	# x = json.loads(j)
	# print json.dumps(x, indent=2)
	# for i in range(len(pod.entries)):
		# print str(pod.entries[i])
		# x = json.loads(str(pod.entries[i]))
		# print json.dumps(x, indent=2)
		# print pod.entries[i]
		# print "------------------------------------\n"
	
	
'''
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
'''
