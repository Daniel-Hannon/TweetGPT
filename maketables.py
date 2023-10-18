import sqlite3
con = sqlite3.connect("twitter.db")
cur = con.cursor()

# Create a trends table with an id and a trending topic name 
'''trends
------------
id | trending_topic_name 
'''
cur.execute("CREATE TABLE IF NOT EXISTS trends(id INTEGER PRIMARY KEY AUTOINCREMENT, trending_topic_name)")

# create a tweets table with the all of the columns: tweet_id, trend_id, tweet_text, likes, comments, retweets, views, date_tweeted, date_scraped
'''tweets
----------------
tweet_id | foreign key trending topic id | tweet_text | likes | comments | retweets | views | date_tweeted | date_retrieved 
'''
cur.execute("CREATE TABLE IF NOT EXISTS tweets(tweet_id INTEGER PRIMARY KEY AUTOINCREMENT, trend_id, tweet ,likes ,comments, retweets, views, date_tweeted, date_retrieved, FOREIGN KEY(trend_id) REFERENCES trends(id))")

file = open("temp_holder_for_test/#chilisgrillandbarbz.txt", "r", encoding="utf-8")
tweet_from_file = file.read().split("\n--------------------------------------------------\n")
trend = (tweet_from_file[0].split(" = ")[1])

cur.execute("INSERT INTO trends(trending_topic_name) VALUES (?)", (trend,))
rows= cur.execute("SELECT * FROM trends").fetchall()
trend_id = rows[-1][0]

for tweet in tweet_from_file[1:-1]:
    values = tweet.split("%_*")
    #values = [tweet_text, likes, comments, retweets, views, date_tweeted, date_retrieved]
    cur.execute("INSERT INTO tweets(trend_id, tweet, likes, comments, retweets, views, date_tweeted, date_retrieved) VALUES (?,?,?,?,?,?,?,?)", (trend_id, values[0], values[1], values[2], values[3], values[4], values[5], values[6]))

tweets_indb= cur.execute("SELECT * FROM tweets").fetchall()
con.commit()
