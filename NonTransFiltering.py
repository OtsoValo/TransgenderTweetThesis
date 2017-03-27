from pymongo import MongoClient
import urllib


client = MongoClient(database)
db = client[exclient]

cols = db.collection_names()

#################################################################################
#List of words containing "Trans" retrieved from....
#http://www.morewords.com/contains/trans/
#Then manually edited to remove the words wanted to be included 
#Transok was hand made to reflect words that indicated the tweet was actually 
#about transgender individuals 
#################################################################################
not_allowed = [line.rstrip('\n') for line in open('trans.txt')]
good = [line.rstrip('\n') for line in open('transok.txt')]

for c in cols: 
    col = db[c]
    cursor = col.find({"text":{"$exists":True}, "id":{"$exists":True}}, {"text": 1, "id" : 1})

    for o in cursor: 
        i = o["text"]
        i = i.lower()
        if any(no in i for no in not_allowed):
            if not any(yes in i for yes in good):
                item = col.find({"id" : o["id"]})
                for t in item: 
                    db["invalid"].insert(t)
                col.remove({"id" : o["id"]})