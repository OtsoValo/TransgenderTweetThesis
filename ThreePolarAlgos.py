
from pymongo import MongoClient
import urllib
from senti_classifier import senti_classifier
import nltk.sentiment
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
import re

import sys

file = open('huliu', 'r') 
hl = []
for line in file: 
    hl.append(line)

f2 = open('ActualTransLabels.txt', 'r')
acc = []
for line in f2: 
    acc.append(float(line))

client = MongoClient(database)
db = client[client]
col = db[excollection]

sentences = []
sid = SentimentIntensityAnalyzer()

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

m = {}
scScore = 0 
hlScore = 0
ssScore = 0
for i in range(len(sentences)): 
    if(i >= 1001):
        break
    pos_score0, neg_score0 = senti_classifier.polarity_scores([sentences[i]])
    if pos_score0 > neg_score0: 
        if acc[i] == 1: 
            scScore += 1
        m[i] = [1]
    elif pos_score0 < neg_score0: 
        if acc[i] == 0: 
            scScore += 1
        m[i] = [0]
    else: 
        if acc[i] == .5: 
            scScore += 1
        m[i] = [.5]
        
    if hl[i] ==  "Neutral":
        if acc[i] == .5: 
            hlScore +=1
        m[i].append(0.5)
    elif hl[i] == "Positive":
        if acc[i] == 1: 
            hlScore +=1
        m[i].append(1)
    else: 
        if acc[i] == 0: 
            hlScore +=1
        m[i].append(0)
        
    ss = sid.polarity_scores(sentences[i])
    if ss["pos"] > ss["neg"] and ss["pos"] > ss["neu"]:
        if acc[i] == 1: 
            ssScore += 1 
        m[i].append(1)
    elif ss["pos"] < ss["neg"] and ss["neg"] > ss["neu"]:
        if acc[i] == 0: 
            ssScore += 1 
        m[i].append(0)
    else: 
        if acc[i] == .5: 
            ssScore += 1 
        m[i].append(.5)
        
        
print("acc len", len(acc))
print("scScore", scScore)
print("hlScore", hlScore)
print("ssScore", ssScore)
print(m)