
# coding: utf-8

# In[1]:

import pymongo
connection = pymongo.MongoClient("mongodb://localhost")
db = connection.tnt


# In[13]:

venue_count = db.odi.aggregate([
    { "$group": { "_id": { "Venue": "$Venue", "Date": "$Date" } } }, 
    { "$group": { "_id": "$_id.Venue", "Count": { "$sum": 1 } } }, 
    { "$sort": { "Count": -1 } },
    { "$match": { "Count": { "$gte": 3 } } }
])['result']


# In[5]:

balls_bowled = db.odi.aggregate([
    { "$group": { "_id": "$Venue", "Balls": { "$sum": 1 } } }, 
    { "$sort": { "Balls": -1 } }
])['result']


# In[6]:

runs_scored = db.odi.aggregate([
    { "$group": { "_id": "$Venue", "Runs": { "$sum": "$Runs Batsman" } } }, 
    { "$sort": { "Runs": -1 } }
])['result']


# In[7]:

wickets = db.odi.aggregate([
    { "$match": { "Wicket Kind": 
                 { "$in": ["bowled", "caught", "caught and bowled", "lbw", "stumped", "hit wicket"] } } }, 
    { "$group": { "_id": "$Venue", "Wickets": { "$sum": 1 } } }, { "$sort": { "Wickets": -1 } }
])['result']


# In[8]:

fours = db.odi.aggregate([
    { "$match": { "Runs Batsman": 4 } }, 
    { "$group": { "_id": "$Venue", "Fours": { "$sum": 1 } } }, 
    { "$sort": { "Fours": -1 } }
])['result']


# In[9]:

sixes = db.odi.aggregate([
    { "$match": { "Runs Batsman": 6 } }, 
    { "$group": { "_id": "$Venue", "Sixes": { "$sum": 1 } } }, 
    { "$sort": { "Sixes": -1 } }
])['result']


# In[14]:

print venue_count[0]
print balls_bowled[0]
print runs_scored[0]
print wickets[0]
print fours[0]
print sixes[0]


# In[16]:

for venue in venue_count:
    db.venues.insert({ "_id": venue["_id"], "Matches": venue["Count"] })


# In[18]:

for venue in balls_bowled:
    db.venues.update({ "_id": venue["_id"] }, { "$set": { "Balls": venue["Balls"] } })

for venue in runs_scored:
    db.venues.update({ "_id": venue["_id"] }, { "$set": { "Runs": venue["Runs"] } })

for venue in wickets:
    db.venues.update({ "_id": venue["_id"] }, { "$set": { "Wickets": venue["Wickets"] } })

for venue in fours:
    db.venues.update({ "_id": venue["_id"] }, { "$set": { "Fours": venue["Fours"] } })

for venue in sixes:
    db.venues.update({ "_id": venue["_id"] }, { "$set": { "Sixes": venue["Sixes"] } })
    


# In[ ]:



