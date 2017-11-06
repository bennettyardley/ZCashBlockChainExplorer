import urllib2
import json
def buildChain():
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		   'Accept-Encoding': 'none',
		   'Accept-Language': 'en-US,en;q=0.8',
		   'Connection': 'keep-alive'}
	siteBuilder = 'https://api.zcha.in/v2/mainnet/blocks?sort=height&direction=descending&limit=20&offset='
	offset = 0
	data = []

	while offset < 1000:
		req = urllib2.Request((siteBuilder + str(offset)), headers=hdr)
		page = urllib2.urlopen(req)
		data += json.load(page)
		offset += 20

	with open('data.txt', 'w') as outfile:
			json.dump(data, outfile) 
