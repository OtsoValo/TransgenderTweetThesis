import gensim 
from pymongo import MongoClient
import urllib
import nltk
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
#best senti classifier
from nltk.sentiment.vader import SentimentIntensityAnalyzer

client = MongoClient(database)
db = client[exclient]

model =  gensim.models.LdaModel.load("example.model")

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


###############################################
#TODO
###############################################
for topic in dic: 
    #method 1 
    s = ", ".join(dic[topic])
    #Senti classifier of choice here 
    pos_score0, neg_score0 = senti_classifier.polarity_scores([s])
    print("Pos: ", pos_score0, "Neg: ", neg_score0)
    
    #method 2
    count2[topic] = {}
    count2[topic]["pos"] = 0
    count2[topic]["neg"] = 0
    count2[topic]["neu"] = 0
    for sent in dic[topic]:
        pos_score0, neg_score0 = senti_classifier.polarity_scores([sent])
        if pos_score0 > neg_score0:
            count2[topic]["pos"] += 1
        elif pos_score0 < neg_score0:
            count2[topic]["neg"] += 1
        else:
            count2[topic]["neu"] += 1
    print(count2[topic]["pos"], count2[topic]["neg"], count2[topic]["neu"])
    #method 3 
    count3[topic] = {}
    count3[topic]["pos"] = 0
    count3[topic]["neg"] = 0
    #optional 
    count3[topic]["neu"] = 0
    
    for sent in dic[topic]:
        pos_score0, neg_score0 = senti_classifier.polarity_scores([sent])
        count3[topic]["pos"] += pos_score0
        count3[topic]["neg"] += neg_score0
        #optional 
        #count3[topic]["neu"] += neu_score0
    print(count3[topic]["pos"], count3[topic]["neg"])
    #count2[topic]["neu"])