

import got
#######################################################################################/
#    Title: GetOldTweets-python
#    Author: Jefferson Henrique
#    Date: 2016
#    Code version: 6bccada
#    Availability: https://github.com/Jefferson-Henrique/GetOldTweets-python
#
#######################################################################################/

from pymongo import MongoClient
import urllib
from tweepy.utils import import_simplejson

def main(): 
    password = urllib.quote_plus(examplepassword)
    client = MongoClient(exampledatabase)
    db = client[exampleclient]
    collection = db[examplecollection]
    json = import_simplejson()
    
    def storeTweet(tweet): 
        data ={}
        data['id'] = tweet.id
        data['permalink'] = tweet.permalink
        data['username'] = tweet.username
        data['text'] = tweet.text
        data['date'] = tweet.date
        data['retweets'] = tweet.retweets
        data['favorites'] = tweet.favorites
        data['mentions'] = tweet.mentions
        data['hashtags'] = tweet.hashtags
        data['geo'] = tweet.geo
        collection.insert(data)

    tweetCriteria = got.manager.TweetCriteria().setQuerySearch('transgender').setSince(exampleStart).setUntil(exampleEnd)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    for tweet in tweets: 
        storeTweet(tweet)
    

if __name__ == '__main__':
	main()