import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import TweepError
from pymongo import MongoClient
from tweepy.utils import import_simplejson


json = import_simplejson()
client = MongoClient('dblocation') 

#authentication info
auth = tweepy.OAuthHandler(token, token)
auth.set_access_token(token, token)

#authenticate
api = tweepy.API(auth)

#set max num tweets 
tweet_num = 5000
tweet_list = []


class MyStreamListener(StreamListener):
    def __init__(self):
        self.i = 0
        
    def on_data(self, data):
        try:
            t = json.loads(data)
            db = client[exampleclient]
            collection = db[examplecollection]
            collection.insert_one(t) 
        except Exception as inst:
            print(inst)
            return True
  
        return True
        
    def on_error(self, status):
        print (status)
        return True;


#make the stream
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(api.auth, myStreamListener)

myStream.filter(track=['trans', 'transgender'], languages = ["en"], async = True)
