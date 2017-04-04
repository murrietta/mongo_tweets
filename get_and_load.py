import tweepy, json
from tweepy import OAuthHandler
 
print "\nSetting up tweet retrieval..."
consumer_key = 'VhFelIym0eSHK5xWIspNR6hgJ'
consumer_secret = 'k6gyQjI5BzzPPQq8Bc4g7FLmGPn9fuf5rdrjS7m6ZuVARqA0X7'
access_token = '4647114132-p1DnuzrgHZomyOcTeD7umjj4WTaAj94yyK1DWZy'
access_secret = '59tsK0Vdn3kJhATp2nbRKZ8CAPcMIsEfTkiNHK8S6pyYK'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

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
	print "\n\nBeginning retrieval"
	for username in names:
		print "{}".format("="*90)
		print "Retrieving tweets for {}".format(username)
		for i in range(8):
			print "Iteration {:0>2} of 8".format(i+1)
			print "Retrieving 200 tweets with tweet ID less than {:>18}...".format(max_id),
			if max_id == None:
				tweets.append(api.user_timeline(screen_name = username,
					count = number_of_tweets))
			else:
				tweets.append(api.user_timeline(screen_name = username,
					count = number_of_tweets,
					since_id=max_id))
			print "{:>20}".format("DONE!")
			print "{:>67}".format("Writing current set to {}...".format(filename)),
			with open(filename,'a') as outfile:
				for item in tweets:
					for tweet in item:
						json.dump(tweet._json,outfile,sort_keys=False )
						outfile.write("\n")
			print "{:>20}".format("DONE!")
			#max_id = min([x.id for x in tweets[-1]])
			try:
				max_id = tweets[-1][-1].id
			except:
				print "No id was available from the last set of tweets."
		max_id = None
	print "\nTweet retrieval complete!\n\n"
else:
	print "Canceled!\n\n"