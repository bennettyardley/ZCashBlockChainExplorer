from __future__ import print_function
from BuildChain import buildChain
from prettytable import PrettyTable
import time
import os
import datetime
import json
import urllib2

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		   'Accept-Encoding': 'none',
		   'Accept-Language': 'en-US,en;q=0.8',
		   'Connection': 'keep-alive'}
site = 'https://api.zcha.in/v2/mainnet/blocks?sort=height&direction=descending&limit=20&offset=0'
site3 = 'https://api.zcha.in/v2/mainnet/blocks?sort=height&direction=descending&limit=1&offset=0'
zecusd = 'https://api.cryptonator.com/api/ticker/zec-usd'

#Run buildChain or use previously stored data
download = raw_input("Would you like to download the most recent block chain? (1.Yes 2.No): ")
if download == '1':
	print ("Downloading")
	buildChain()

with open('data.txt', 'r') as data_file:    
		data = json.load(data_file)
#Calculates time	
timeList = []
for k in data:
	timeList.append(k['timestamp'])

cnt = len(timeList)
add = 0
j = 1
while j < cnt:
	add += timeList[j - 1] - timeList[j]
	j += 1

avg = add / cnt
avgM = avg / 60 % 60
avgS = avg % 60

#Prints table of information
table = PrettyTable(["Block #", "Miner", "Time"])
while True:
	os.system('cls')
	req2 = urllib2.Request(site, headers=hdr)
	page2 = urllib2.urlopen(req2)
	data2 = json.load(page2)
	timeList2 = []
	for k in data2:
		timestamp = (
			datetime.datetime.fromtimestamp(
				int(k['timestamp'])
			).strftime('%I:%M %p')
		)
		#Assigns names to common pools
		if(k['miner'] == 't1SaATQbzURpG1qU3vz9Wfn3pwXoTqFtTq2'):
			k['miner'] = 'Suprnova'
		elif(k['miner'] == 't1Xk6GeseeV8FSDpgr359yL2LmaRtUdWgaq'):
			k['miner'] = 'Coinotron'
		elif(k['miner'] == 't1ZJQNuop1oytQ7ow4Kq8o9if3astavba5W'):
			k['miner'] = 'Flypool'
		elif(k['miner'] == 't1aZvxRLCGVeMPFXvqfnBgHVEbi4c6g8MVa'):
			k['miner'] = 'F2Pool'			
		elif(k['miner'] == 't1hASvMj8e6TXWryuB3L5TKXJB7XfNioZP3'):
			k['miner'] = 'Nanopool'
		elif(k['miner'] == 't1KstPVzcNEK4ZeauQ6cogoqxQBMDSiRnGr'):
			k['miner'] = 'Coinmine.pl'
		table.add_row([k['height'], k['miner'], timestamp])
		timeList2.append(k['timestamp'])
	print(table)
	table.clear_rows()
	
	req4 = urllib2.Request(zecusd, headers=hdr)
	page4 = urllib2.urlopen(req4)
	data4 = json.load(page4)
	#Prints current ZCash information
	print("1 ZEC is worth $" + data4['ticker']['price'])
	
	print("Average time between block: " + str(int(avgM)) + " minutes and " + str(int(avgS)) + " seconds")
	#Calculates time since last block
	req3 = urllib2.Request(site3, headers=hdr)
	page3 = urllib2.urlopen(req3)
	data3 = json.load(page3)
	while data2[0]['height'] == data3[0]['height']:
		currentTime = time.time()
		timeDif = currentTime - timeList2[0];
		difM = timeDif / 60 % 60
		difS = timeDif % 60
		print(str(int(difM)) +' minutes and ' + str(int(difS)) + ' seconds since last block', end='\r')
		time.sleep(1)
		req3 = urllib2.Request(site3, headers=hdr)
		page3 = urllib2.urlopen(req3)
		data3 = json.load(page3)

