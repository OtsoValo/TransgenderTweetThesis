from pymongo import MongoClient
import urllib


client = MongoClient(database)
db = client[exclient]
cols = db.collection_names()

dic = {}

for col in cols: 
    collection = db[col]
    cursor = collection.find({"username":{"$exists":True}}, {"username": 1})
    for item in cursor:
        key = item["username"]
        dic[key] = dic.get(key, 0) + 1
        
for thing in dic: 
    if dic[thing] > 1:
        print(thing, dic[thing])
print(len(dic))