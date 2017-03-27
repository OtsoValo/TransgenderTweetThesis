import gensim 
from pymongo import MongoClient
import urllib
import nltk
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')

#Chosen best senti classifier
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import networkx as nx
import matplotlib.pyplot as plt

client = MongoClient(database)
db = client[exclient]

model =  gensim.models.LdaModel.load(example.model)

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
size = {}
topcs = []
for t in range(len(tweet_list)): 
    t_lower = tweet_list[t].lower()
    tokens = tokenizer.tokenize(t_lower)
    top = model.get_document_topics(dictionary.doc2bow(tokens))
    for num, prob in top:
        if num not in topcs: 
            topcs.append(num)
        if t in dic: 
            dic[t].append(num)
        else: 
            dic[t] = [num]
        if num in size: 
            size[num] += 1
        else: 
            size[num] = 1

#edges             
e = []
for item in dic: 
    for top in range(len(dic[item])):
        for t2 in range(top + 1, len(dic[item])):
            e.append((dic[item][top], dic[item][t2]))


#Graph
g = nx.Graph()
g.add_edges_from(e)

############################
#TODO#
val_map = {9: 1.0,
           12: 0.75,
           28: 0.0,
           80:0.25}

values = [val_map.get(node, 0.5) for node in g.nodes()]
############################

nx.draw(g, pos=pos, cmap=plt.get_cmap('RdYlGn'), nodelist=size.keys(), node_size=[v * 100 for v in size.values()], node_color=values, with_labels=False)
labels = {}    

for node in g.nodes():
    labels[node] = node

nx.draw_networkx_labels(g,pos,labels,font_size=16,font_color='black')

plt.show()
