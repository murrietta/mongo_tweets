import tweepy, json, time, datetime
from tweepy import OAuthHandler
 
print "\nSetting up tweet retrieval..."
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

#trying with cursor
for status in tweepy.Cursor(api.user_timeline).items():
	print status._json['created_at']

#set count to however many tweets you want; twitter only allows 200 at once
number_of_tweets = 200

print "{:>20}: {}".format("Tweets per call",number_of_tweets)

#get tweets
#will get the 3200 by iterating 16 times and keeping track of max id
max_id = None
tweets = []
if max_id != None:
	print "{:>20}: {}".format("Starting tweet ID",max_id)
else:
	print "{:>20}: {}".format("Starting tweet ID","Latest")

filename = 'json_tweets.txt'
print "{:>20}: {}".format("Output file name",filename)

from username import username as names
print "{:>20}:".format("Selected users")
for username in names:
	print "{:>20}  {}".format(" ",username)

cont = raw_input("\nContinue? [Y/N]")

if cont.lower() == "y":
	with open(filename,'w') as outfile:
		dts = []
		print "\n\nBeginning retrieval"
		for username in names:
			print "{}".format("="*90)
			print "Retrieving tweets for {}".format(username)
			for i in range(3):
				print "Iteration {:0>2} of 3".format(i+1)
				print "Retrieving 200 tweets with tweet ID less than {:>18}...".format(max_id),
				if max_id == None:
					tweets.append(api.user_timeline(screen_name = username,
						count = number_of_tweets))
				else:
					tweets.append(api.user_timeline(screen_name = username,
						count = number_of_tweets,
						since_id=max_id))
				print "{:>20}".format("DONE!")
				try:
					max_id = tweets[-1][-1].id
				except:
					print "No id was available from the last set of tweets."
			print "{:>67}".format("Writing current set to {}...".format(filename)),
			for item in tweets:
				for tweet in item:
					#modify the created_at date for each tweet
					#it appears that some of them already come with the date in appropriate format?
					#print "Current tweet created_at format: {}".format(tweet._json['created_at'])
					try:
						dt = datetime.datetime.strptime(tweet._json['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
						#it is stored sort of like unix time but in micro seconds rather than milli seconds
						dts.append(dt)
						tweet._json['created_at'] = {"$date":time.mktime(dt.timetuple())*1000}
					except:
						#not sure what's going on why we could possibly get here and yet the last line under try is still executed successfully
						if tweet._json['created_at'].get('$date',False) == False:
							dt = datetime.datetime.fromtimestamp(tweet._json['created_at']/1000)
							dts.append(dt)
							tweet._json['created_at'] = {"$date": tweet._json['created_at']}
					json.dump(tweet._json,outfile,sort_keys=False)
					outfile.write("\n")
			print "{:>20}".format("DONE!")
			max_id = None
	print "\nDate range captured: {} to {}\nTweet retrieval complete!\n\n".format(min(dts),max(dts))
else:
	print "Canceled!\n\n"