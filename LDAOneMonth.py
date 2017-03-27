from pymongo import MongoClient
import urllib
import nltk
import stop_words
import gensim
import re

#data cleaning: Tokenizing, Stopping, Stemming
#Tokenizing
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')

client = MongoClient(database)
db = client[exclient]

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
    
#stemming
from nltk.stem.porter import PorterStemmer
p_stemmer = PorterStemmer()
texts = []
for t in tokens:
    text = [p_stemmer.stem(i) for i in t]
    text = [i for i in text if not len(i) <= 1]
    texts.append(text)
    

##Constructing a document-term matrix
from gensim import corpora, models
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]  
#doc2bow converts text into bag-of-words. Corpus is a list of vectors. 
#use genism’s LdaModel function

num_topics = sqrt(2*len(tweet_list))

ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics, id2word=dictionary, passes = 10)
topics = ldamodel.show_topics(num_topics, num_words=10, formatted=False)
#save the model for use elsewhere
ldamodel.save("FileName.txt")

top_words = []

for topic in topics:
    for word, weight in topic[1]:
        top_words.append(word)
    print(", ".join(top_words))
    top_words = []