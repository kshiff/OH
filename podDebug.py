import feedparser
import csv
import re

feeds = []

with open('RSS-Feeds_Karl.csv', 'rb') as f: 
	reader = csv.reader(f, delimiter=',')
	next(reader, None)
	for row in reader:
		# print row
		feeds.append(row[2])


pod = feedparser.parse(feeds[231])

print pod

'''
for i, link in enumerate(feeds):
	print i
	pod = feedparser.parse(link)

	provider = pod.feed.title


	for x in range(len(pod.entries)):
			episode = pod.entries[x].title
			episode = episode.encode('ascii','ignore')

			# check if summary is truncated
			data = pod.entries[x].summary
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
'''