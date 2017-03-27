import gensim 
from pymongo import MongoClient
import urllib
import nltk
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')

from nltk.sentiment.vader import SentimentIntensityAnalyzer

client = MongoClient(database)
db = client[exclient]

model =  gensim.models.LdaModel.load("Example.model")

cursor = db.excollection.find({"text":{"$exists":True}}, {"text": 1})

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

   
    
from gensim import corpora, models
dictionary = corpora.Dictionary(tweets)

dic = {}

for t in tweet_list: 
    t_lower = t.lower()
    tokens = tokenizer.tokenize(t_lower)
    top = model.get_document_topics(dictionary.doc2bow(tokens))
    for num, prob in top: 
        if num in dic: 
            dic[num].append(t.encode('ascii','ignore'))
        else: 
            dic[num] = [t.encode('ascii','ignore')]

count2 = {}
count3 = {}

sid = SentimentIntensityAnalyzer()

for topic in dic: 
    #method 1 
    s = ", ".join(dic[topic])
    #Senti classifier of choice here 
    ss = sid.polarity_scores(s)
    print("Pos: ", ss["pos"], "Neg: ",ss["neg"], "Neu: ", ss["neu"])
    
    #method 2
    count2[topic] = {}
    count2[topic]["pos"] = 0
    count2[topic]["neg"] = 0
    count2[topic]["neu"] = 0
    for sent in dic[topic]:
        ss = sid.polarity_scores(sent)
        if ss["pos"] > ss["neg"] and ss["pos"] > ss["neu"]:
            count2[topic]["pos"] += 1
        elif ss["pos"] < ss["neg"] and ss["neg"] > ss["neu"]:
            count2[topic]["neg"] += 1
        else: 
            count2[topic]["neu"] += 1

    print(count2[topic]["pos"], count2[topic]["neg"], count2[topic]["neu"])
    
    #method 3 
    count3[topic] = {}
    count3[topic]["pos"] = 0
    count3[topic]["neg"] = 0
    count3[topic]["neu"] = 0
    
    for sent in dic[topic]:
        ss = sid.polarity_scores(sent)
        count3[topic]["pos"] += ss["pos"]
        count3[topic]["neg"] += ss["neg"]
        count3[topic]["neu"] += ss["neu"]
    print(count3[topic]["pos"], count3[topic]["neg"], count3[topic]["neu"])
    
    
    