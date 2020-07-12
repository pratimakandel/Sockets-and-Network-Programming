#!/usr/bin/env python

import argparse
import urllib.request
import re
import urllib

seen = list()
x = 0
def search_links(url, depth):

	global x
	#connect to a url, use the above seen list to make sure you
	#haven't connect to that url before.
	url_has_been_seen = (url in seen)
	if (url.startswith("http://") and (not url_has_been_seen)):
		seen.append(url)

		#start crawling

		url2 = url.replace("http://", "", 1)
		path = url2.split('/')
		host = path[0]
		with urllib.request.urlopen(url) as response:
			html = response.read()
		
		links = re.findall('href="(.*?)"', str(html))

		for link in links:
			
			if link.startswith("http"):
				path1 = link.split('/')[-1]
				if path1 == "":
						filename = "index_" + str(x)
						try:
							d = urllib.request.urlopen(link)
						except:
							pass
						else:
							result6 = d.status
							if result6 == 200:
								urllib.request.urlretrieve(link, filename + ".html")
								x += 1
		
				else:
						try:
							c = urllib.request.urlopen(link)
						except:
							pass
						else:
							result5 = c.status
							if result5 == 200:
								urllib.request.urlretrieve(link, path1)
		
			else:
				#if the link has no host (concatenate the host and the link)
				link1 = "http://" + host + "/"  + link
				path2 = link1.split('/',1)
				page2 = path2[1].replace('/', "")
				try:
					b  = urllib.request.urlopen(link1)
				except:
				  	pass
				else: 
					result1 = b.status
					if result1 == 200:
						if(page2.endswith('.html')):
							urllib.request.urlretrieve(link1, page2)
		if(int (depth) > 0):
			if(link.startswith('http')):
				a = urllib.request.urlopen(link)
				result = a.status
				if result == 200:
					search_links(link, int (depth) -1)
		else:
			exit()
               

	
		
						
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Webpage link scraper')
	parser.add_argument('--url', action="store", dest="url", required=True)
	parser.add_argument('--depth', action="store", dest="depth", default=2)
	
	given_args=parser.parse_args()
	
	try:
		search_links(given_args.url, given_args.depth)
	except KeyboardInterrupt:
			print("Aborting the search")
			
