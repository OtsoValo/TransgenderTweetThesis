import sys
from pymongo import MongoClient
import urllib
import requests
import tweepy
import json


auth = tweepy.OAuthHandler(token, token)
auth.set_access_token(token, token)

#authenticate
api = tweepy.API(auth)

client = MongoClient(database)
db = client[exclient]

cols = db.collection_names()

for c in cols:
    col = db[c]
    cursor = col.find({"text":{"$exists":True}, "id":{"$exists":True}}, {"id": 1})
    #EnT for English Tweet object
    newname = "EnT" + c 
    newdb = db[newname]
    count = 0
    query = []

    for doc in cursor: 
        #twitter api allows requests in batches of 100 
        if(count == 100):
            if query:
                #can add wait on rate limit 
                tweets = api.statuses_lookup(query)
                for tweet in tweets: 
                    json_str = json.dumps(tweet._json)
                    done = json.loads(json_str)
                    #filter only english tweets
                    if(done["lang"] == "en"):
                        newdb.insert(done)

            query = []
            count = 0

        query.append(doc["id"])
        count += 1

    if query: 
        tweets = api.statuses_lookup(query)
        for tweet in tweets: 
            json_str = json.dumps(tweet._json)
            done = json.loads(json_str)
            if(done["lang"] == "en"):
                newdb.insert(done)