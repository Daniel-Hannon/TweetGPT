import sqlite3
con = sqlite3.connect("twitter.db")
cur = con.cursor()

#read the contents of the databases 

trends = cur.execute("SELECT * FROM trends").fetchall()
tweets = cur.execute("SELECT * FROM tweets").fetchall()

# print(trends)
print(tweets)