import json
from pprint import pprint
import urllib
import httplib
import datetime, time

API_KEY = '09C43A9B270A470B8EB8F2946A9369F3'
host = 'api.topsy.com'
url = '/v2/content/tweets.json'

#########################################
# Convert unix time stamps to Y-M-D H:M:S
#########################################
def timestamp_to_str(unix_timestamp):
	return (
	    datetime.datetime.fromtimestamp(
	        int(unix_timestamp)
	    ).strftime('%Y-%m-%d %H:%M:%S')
	)

###########################################
# Question 1
# display the top 5 tweets (author, date,
# and tweet) given a search term or hashtag
###########################################
def top_5_tweets(term):
	"""searches for the top 5 tweets for a given term returns them
	input: hashtag (str)
	output: list of the top five tweets as strings
	"""
	#########   create UNIX timestamps
	start_date = datetime.datetime(2015,01,14, 12,30,0)
	end_date = datetime.datetime(2015,01,29, 17,15,0)
	mintime = int(time.mktime(start_date.timetuple()))
	maxtime = int(time.mktime(end_date.timetuple()))

	#########   set query parameters
	params = urllib.urlencode({'apikey' : API_KEY,
	                           'q' :term,
	                           'include_metrics':'1',
	                           'limit': 5})

	#########   create and send HTTP request
	req_url = url + '?' + params
	req = httplib.HTTPConnection(host)
	req.putrequest("GET", req_url)
	req.putheader("Host", host)
	req.endheaders()
	req.send('')

	#########   get response and print out status
	resp = req.getresponse()
	# print resp.status, resp.reason

	#########   extract tweets
	resp_content = resp.read()
	ret = json.loads(resp_content)
	tweets = ret['response']['results']['list']
	for tweet in tweets:
		# pprint(tweet)
		print tweet['author']['name']
		print timestamp_to_str(tweet['citation_date'])
		print tweet['highlight'], '\n'

	with open('top_tweets.txt', 'w+') as f:
		for tweet in tweets:
			f.write(json.dumps(tweet) + '\n')

###########################################
# Question 2
# Get all tweets of any of the hashtags:
#
# *-------------------------------------*
# | #Seahawks  |  #Patriots             |
# | #GoHawks   |  #GoPatriots           |
# | #Halftime  |  #superbowlcommercials |
# |            |  #SuperBowlXLIX        |
# *-------------------------------------*
###########################################
def get_all_tweets(hashtag):
	pass



if __name__ == '__main__':
	# data = []
	# with open('q1_file.txt', 'r') as js_dat:
	# 	for line in js_dat:
	# 		# ret = json.loads(line)
	# 		data.append(json.loads(line))

	# with open('pprint_q1_file.txt', 'w+') as f:
	# 	for dat in data:
	# 		pprint(dat, f)
	# 		f.write('\n-------------------------------------------------------\n\n')

	top_5_tweets('#GoPatriots')
