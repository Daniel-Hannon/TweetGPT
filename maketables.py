import sqlite3
con = sqlite3.connect("twitter.db")
cur = con.cursor()
'''trending
------------
id | trending_topic_name 
tweet
----------------
id | tweet | likes | comments | retweets | date tweeted | date retrieved | foreign key trending topic id'''
cur.execute("CREATE TABLE trending(id, trending_topic_name)")
cur.execute("CREATE TABLE tweet(id ,trend_id, tweet ,likes ,comments,retweets,date_tweeted , date_retrieved)")
