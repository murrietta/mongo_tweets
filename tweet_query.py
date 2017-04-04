from pymongo import MongoClient
from datetime import datetime
import pprint
from bson.son import SON

#setup connection
client = MongoClient('localhost', 27017)
db = client.project_4.tweets

#setup pipeline variable, I usually wouldn't bother but mongodb queries get messsy quickly
pipelines = [[
	{"$unwind": "$entities.hashtags"},
	{"$group": {"_id": "$entities.hashtags.text", "count": {"$sum": 1}}},
	{"$sort": SON([("count", -1)])}
]]

#save the output to variable res
res = [[x for x in db.aggregate(pipelines[-1])]]

#print only those that had a count over 50
for r in res[-1]:
	if r['count']>=50:
		print r

#dates are now stored as dates in MongoDB so we can query on dates
#although it would be trivial to step though the months in python,
#we'll use the capabilities of mongodb's query language to group
#counts by month
for htag in ('DataSciBowl','Data4Good'):
	pipelines.append([
		{"$match":{"entities.hashtags.text":htag}},
		{"$group": {"_id": {"$substr": ['$created_at', 0, 7]},"tweet_count": {"$sum": 1}}},
		{"$sort": SON([("created_at", -1)])}
	])
	res.append({htag:[x for x in db.aggregate(pipelines[-1])]})

#making a pandas dataframe of the aggregate data and plotting
ls = []
for x in res[-2:]:
	for y in x.values()[0]:
		y.update({"hashtag":x.keys()[0]})
		ls.append(y)

import pandas as pd
from matplotlib import pyplot as plt
#ggplot style usually looks good without any modifications
plt.style.use('ggplot')
df = pd.DataFrame(ls)
df['_id'] = pd.to_datetime(df['_id'])
plt.plot_date(df[df['hashtag']=='DataSciBowl'].loc[:,'_id'],
	df[df['hashtag']=='DataSciBowl'].loc[:,'tweet_count'],'-',marker="o",linewidth=7.5,markersize=10,label='#DataSciBowl')
plt.plot_date(df[df['hashtag']=='Data4Good'].loc[:,'_id'],
	df[df['hashtag']=='Data4Good'].loc[:,'tweet_count'],'-',marker="o",linewidth=7.5,markersize=10,label='#Data4Good')
plt.legend(fontsize=20)
plt.show()

#looking at tweets by user by the last few months
users = [x for x in db.aggregate([{"$unwind": "$user"},{"$group":{"_id":"$user.screen_name","tweet_count":{"$sum":1}}},{"$sort": SON([("tweet_count", -1)])}])]
for user in users:
	pipelines.append([
		{"$match":{"user.screen_name":user['_id']}},
		{"$group": {"_id": {"$substr": ['$created_at', 0, 7]},"tweet_count": {"$sum": 1}}},
		{"$sort": SON([("created_at", -1)])}
	])
	res.append({user['_id']:[x for x in db.aggregate(pipelines[-1])]})

#making a pandas dataframe of the aggregate data and plotting
ls = []
for x in res[-6:]:
	for y in x.values()[0]:
		y.update({"username":x.keys()[0]})
		ls.append(y)
df2 = pd.DataFrame(ls)
df2['_id'] = pd.to_datetime(df2['_id'])
df2 = df2.sort_values('_id')
for i in range(6):
	#plt.subplot(231 + i)
	plt.plot_date(df2[df2['username']==df2.username.unique()[i]].loc[:,'_id'],
		df2[df2['username']==df2.username.unique()[i]].loc[:,'tweet_count'],'-',marker="o",linewidth=7.5,markersize=10,label='@{}'.format(df2.username.unique()[i]))
plt.xlim(xmax=pd.to_datetime('20170501'))
plt.legend(fontsize=20)
plt.show()

#quick check that @dpatil's tweets didn't get a messed up 'created_at' field
for x in db.find({'user.screen_name':users[2]['_id']}):
	print x['created_at']