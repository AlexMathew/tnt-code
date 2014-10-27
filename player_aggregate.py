
# coding: utf-8

# In[2]:

import pymongo
connection = pymongo.MongoClient("mongodb://localhost")
db = connection.tnt


# In[3]:

# Teams of batsmen
bat_teams = db.odi.aggregate([{ "$group": { "_id": { "Batsman": "$Batsman", "Team": "$BattingTeam" } } }])['result']


# In[4]:

# Teams of bowlers
bowl_teams = db.odi.aggregate([
    { "$project": { "Bowler": 1, "Team": { "$cond": [{ "$cmp": ["$BattingTeam", "$Team1"] }, "$Team1", "$Team2"] } } },
    { "$group": { "_id": { "Bowler": "$Bowler", "Team": "$Team" } } }
])['result']


# In[5]:

# Batting - Total innings batted
bat_innings = db.odi.aggregate([
    { "$group": { "_id": { "Batsman": "$Batsman", "Date": "$Date" } } },
    { "$group": { "_id": "$_id.Batsman", "Innings": { "$sum": 1 } } }
])['result']


# In[6]:

# Batting - Total balls faced
balls_faced = db.odi.aggregate([
    { "$group": { "_id": "$Batsman", "Balls": { "$sum": 1 } } }
])['result']


# In[7]:

# Batting - Total runs scored
runs_scored = db.odi.aggregate([
    { "$group": { "_id": "$Batsman", "Runs Scored": { "$sum": "$Runs Batsman" } } }
])['result']


# In[8]:

# Batting - Total times dismissed
outs = db.odi.aggregate([
    { "$match": { "Dismissed Player": { "$ne": "" } } },
    { "$group": { "_id": "$Dismissed Player", "Outs": { "$sum": 1 } } }
])['result']


# In[9]:

# Batting - Total fours
fours_bat = db.odi.aggregate([
    { "$match": { "Runs Batsman": 4 } },
    { "$group": { "_id": "$Batsman", "Fours": { "$sum": 1 } } }
])['result']


# In[10]:

# Batting - Total sixes
sixes_bat = db.odi.aggregate([
    { "$match": { "Runs Batsman": 6 } },
    { "$group": { "_id": "$Batsman", "Sixes": { "$sum": 1 } } }    
])['result']


# In[11]:

# Bowling - Total innings bowled
bowl_innings = db.odi.aggregate([
    { "$group": { "_id": { "Bowler": "$Bowler", "Date": "$Date" } } },
    { "$group": { "_id": "$_id.Bowler", "Innings": { "$sum": 1 } } }
])['result']


# In[12]:

# Bowling - Total balls bowled
balls_bowled = db.odi.aggregate([
    { "$group": { "_id": "$Bowler", "Balls": { "$sum": 1 } } }
])['result']


# In[13]:

# Bowling - Total runs conceded
runs_conceded = db.odi.aggregate([
    { "$group": { "_id": "$Bowler", "Runs Conceded": { "$sum": "$Runs Batsman" } } }
])['result']


# In[14]:

# Bowling - Total wickets
wickets = db.odi.aggregate([
    { "$match": { "Wicket Kind": { "$in": 
                                  ["bowled", "caught", "caught and bowled", "lbw", "stumped", "hit wicket"] 
                                  } } }, 
    { "$group": { "_id": "$Bowler", "Wickets": { "$sum": 1 } } }
])['result']


# In[15]:

# Bowling - Total fours
fours_bowl = db.odi.aggregate([
    { "$match": { "Runs Batsman": 4 } },
    { "$group": { "_id": "$Bowler", "Fours": { "$sum": 1 } } }
])['result']


# In[16]:

# Bowling - Total sixes
sixes_bowl = db.odi.aggregate([
    { "$match": { "Runs Batsman": 6 } },
    { "$group": { "_id": "$Bowler", "Sixes": { "$sum": 1 } } }
])['result']


# In[38]:

# Bowling - Total extras
extras = db.odi.aggregate([
    { "$group": { "_id": "$Bowler", "NoBalls": { "$sum": "$Runs Extras - NoBall" }, "Wides": { "$sum": "$Runs Extras - Wides" } } },
])['result']


# In[17]:

# Fielding - Total catches
catches = db.odi.aggregate([
    { "$match": { "Wicket Kind": "caught" } }, 
    { "$group": { "_id": "$Wicket Fielder", "Catches": { "$sum": 1 } } }
])['result']
for player in catches:
    if '(sub)' in player['_id']:
        catches[catches.index(player)] = { "Catches": player["Catches"], "_id": player["_id"].replace(' (sub)', '')}


# In[18]:

# Fielding - Total run outs
_runouts = db.odi.aggregate([
    { "$match": { "Wicket Kind": "run out" } }, 
    { "$group": { "_id": "$Wicket Fielder", "Run Outs": { "$sum": 1 } } }
])['result']
runouts = []
for runout in _runouts:
    for player in runout['_id'].split(','):
        runouts.append({ "Run Outs": runout['Run Outs'], "_id": player.replace(' (sub)', '') })


# In[19]:

# Fielding - Total stumpings
stumpings = db.odi.aggregate([
    { "$match": { "Wicket Kind": "stumped" } }, 
    { "$group": { "_id": "$Wicket Fielder", "Stumpings": { "$sum": 1 } } }, 
])['result']


# In[30]:

# Fielding - Byes per match
byes = db.odi.aggregate([
    { "$project": { "Team": { "$cond": [{ "$cmp": ["$BattingTeam", "$Team1"] }, "$Team1", "$Team2" ] }, "Date": 1, "Runs Extras - Byes": 1 } }, 
    { "$group": { "_id": { "Team": "$Team", "Date": "$Date" }, "Byes": { "$sum": "$Runs Extras - Byes" } } }, 
    { "$group": { "_id": "$_id.Team", "Matches": { "$sum": 1 }, "Byes": { "$sum": "$Byes" } } }, 
    { "$project": { "Byes per match": { "$divide": ["$Byes", "$Matches"] } } }
])['result']
byes_per_match = dict()
for team in byes:
    byes_per_match[team['_id']] = team['Byes per match']


# In[21]:

# Set up teams

for team in bat_teams:
    try:
        db.players.insert({ "_id": team['_id']['Batsman'], "Team": team['_id']['Team'] })
    except:
        pass
    
for team in bowl_teams:
    try:
        db.players.insert({ "_id": team['_id']['Bowler'], "Team": team['_id']['Team'] })
    except:
        pass


# In[22]:

# Set up batting stats

for player in bat_innings:
    db.players.update({ "_id": player['_id'] }, { "$set": { "Innings batted": player['Innings'] } })

for player in balls_faced:
    db.players.update({ "_id": player['_id'] }, { "$set": { "Balls faced": player['Balls'] } })

for player in runs_scored:
    db.players.update({ "_id": player['_id'] }, { "$set": { "Runs scored": player['Runs Scored'] } })

for player in outs:
    db.players.update({ "_id": player['_id'] }, { "$set": { "Outs": player['Outs'] } })

for player in fours_bat:
    db.players.update({ "_id": player['_id'] }, { "$set": { "Fours scored": player['Fours'] } })

for player in sixes_bat:
    db.players.update({ "_id": player['_id'] }, { "$set": { "Sixes scored": player['Sixes'] } })    


# In[39]:

# Set up bowling stats

for player in bowl_innings:
    db.players.update({ "_id": player['_id'] }, { "$set": { "Innings bowled": player['Innings'] } })
    
for player in balls_bowled:
    db.players.update({ "_id": player['_id'] }, { "$set": { "Balls bowled": player['Balls'] } })

for player in runs_conceded:
    db.players.update({ "_id": player['_id'] }, { "$set": { "Runs conceded": player['Runs Conceded'] } })

for player in wickets:
    db.players.update({ "_id": player['_id'] }, { "$set": { "Wickets": player['Wickets'] } })

for player in fours_bowl:
    db.players.update({ "_id": player['_id'] }, { "$set": { "Fours conceded": player['Fours'] } })

for player in sixes_bowl:
    db.players.update({ "_id": player['_id'] }, { "$set": { "Sixes conceded": player['Sixes'] } })    

for player in extras:
    db.players.update({ "_id": player['_id'] }, { "$set": { "Extras": player["Wides"] + player["NoBalls"] } })


# In[32]:

# Set up fielding stats

for player in stumpings:
    db.players.update({ "_id": player['_id'] }, { "$set": { "Stumpings": player['Stumpings'] } })
    
for keeper in db.players.find({ "Stumpings": { "$exists": True } }):
    db.players.update({ "_id": keeper['_id'] }, { "$set": { "Byes per match": byes_per_match[keeper['Team']] } })
    
for player in catches:
    db.players.update({ "_id": player['_id'] }, { "$inc": { "Catches": player["Catches"] } })
    
for player in runouts:
    db.players.update({ "_id": player['_id'] }, { "$inc": { "Run outs": player["Run Outs"] } })
    

