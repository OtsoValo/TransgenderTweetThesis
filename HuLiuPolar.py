
from pymongo import MongoClient
import urllib
import nltk.sentiment
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
import re

#This function writes to standard output automatically 
#To get around problems comparing output to other types of senti classifiers 
#I wrote the output to a file then read in the file for comparisons later
import sys
sys.stdout = open('huliu', 'w')

client = MongoClient(database)
db = client[exclient]
col = db[excollection]

sentences = []

#1000 used for manual testing
cursor = col.find({"text":{"$exists":True}}, {"text": 1}).limit(1000)

tweets = []
tweet_list = []


#for each tweet in the file, add it to the list of tweets
for index in cursor: 
    tweet_list.append(index["text"])
#lowercase all words in tweets for cleanup  
for t in tweet_list:
    t_lower = t.lower()
    tokens = tokenizer.tokenize(t_lower)
    tweets.append(tokens)
    
#create English stop words list
from stop_words import get_stop_words
en_stop = get_stop_words('en')
#remove stop words from tokens
tokens = []
tweet_remove = ['rt','https','co','amp','transgender', 'trans']

emoji_pattern = re.compile(
    u"(\ud83d[\ude00-\ude4f])|"  # emoticons
    u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
    u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
    u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
    u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
    "+", flags=re.UNICODE)

#remove stop words
for t in tweets:
    token = [i for i in t if not i in en_stop]
    token = [i for i in token if not i in tweet_remove]
    token = [emoji_pattern.sub(r'', i) for i in token]
    tokens.append(token)

for to in tokens:
    key = ' '.join(to)
    sentences.append(key)

i = 0
m = {}
for s in sentences: 
    nltk.sentiment.util.demo_liu_hu_lexicon(s, plot=False)