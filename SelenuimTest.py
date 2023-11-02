from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import datetime
import sqlite3
con = sqlite3.connect("twitter.db")
cur = con.cursor()

## DROP TABLES FOR TESTING ONLY
# cur.execute("DROP TABLE IF EXISTS tweets")
# cur.execute("DROP TABLE IF EXISTS trends")

# Create a trends table with an id and a trending topic name 
'''trends
------------
id | trending_topic_name 
'''
cur.execute("CREATE TABLE IF NOT EXISTS trends(id INTEGER PRIMARY KEY AUTOINCREMENT, trending_topic_name)")

# create a tweets table with the all of the columns: tweet_id, trend_id, tweet_text, likes, comments, retweets, views, date_tweeted, date_scraped
'''tweets
----------------
tweet_id | foreign key trending topic id | tweet | likes | comments | retweets | views | date_tweeted | date_retrieved 
'''
cur.execute("CREATE TABLE IF NOT EXISTS tweets(tweet_id INTEGER PRIMARY KEY AUTOINCREMENT, trend_id, tweet ,likes ,comments, retweets, views, date_tweeted, date_retrieved, FOREIGN KEY(trend_id) REFERENCES trends(id))")

chrome_options = Options()
#Put your own path to the chrome user data folder
chrome_options.add_argument(r"--user-data-dir=C:\Users\danie\AppData\Local\Google\Chrome\User Data")

# chrome_options.add_argument("--headless")
chrome_options.add_argument("--full-screen")

if __name__ == "__main__":
   # open the browser
   driver = webdriver.Chrome(options=chrome_options)
   # go to the twitter trending page
   driver.get("https://twitter.com/explore/tabs/trending")
   # wait for the page to load
   driver.implicitly_wait(20)
   #get all the trending topics on the page
   trends = driver.find_elements(By.CSS_SELECTOR, '[data-testid="trend"]')
   trend_names = []
   for trend in trends[0:5]:
      trend_name= trend.find_elements(By.CSS_SELECTOR, 'span')[3].text
      trend_names.append(trend_name)

   #loop through the first 5 the trending topics, any more and twitter locks out the account temporarily 
   for trend_name in trend_names:
      searchbox= driver.find_element(By.CSS_SELECTOR, '[data-testid="SearchBox_Search_Input"]')

      #click the search button by sending cntrl+a and delete
      searchbox.send_keys(u'\ue009'+'a')
      searchbox.send_keys(u'\ue017')

      #check if the trend is promoted
      if trend_name.__contains__("Promoted"):
         continue
      #put the trend name in the search box
      searchbox.send_keys(trend_name)
      searchbox.send_keys(u'\ue007')

      ## write the tweets to a file in the folder temp_holder_for_test
      ## FOR TESTING ONLY
      # file_name = trend_name + ".txt"
      # file = open("temp_holder_for_test/"+file_name,"w",encoding="utf-8")
      # file.write("Tweets from Trend = "+trend_name+"\n")
      # file.write("--------------------------------------------------\n")

      # add the trend to the database
      cur.execute("INSERT INTO trends(trending_topic_name) VALUES (?)", (trend_name,))
      trend_id = cur.execute("SELECT (id) FROM trends WHERE trending_topic_name = (?)", (trend_name,)).fetchone()[0]

      i=0
      #loop until 50 unique tweets are found or 75 scrolls are done
      while i < 50:
         #mark all the tweets on the page
         tweets = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
         for tweet in tweets:
            #Save the tweet statistics to put into a database
            try:
               tweet_text = tweet.find_element(By.CSS_SELECTOR,'div[data-testid="tweetText"]').text
            except:
               tweet_text = "Null"
            tweet_id = str(hash(tweet_text))
            try:
               comments = tweet.find_element(By.CSS_SELECTOR,'div[data-testid="reply"]').text
            except:
               comments = "0"
            try:
               retweets = tweet.find_element(By.CSS_SELECTOR,'div[data-testid="retweet"]').text
            except:
               retweets = "0"
            try:
               likes = tweet.find_element(By.CSS_SELECTOR,'div[data-testid="like"]').text
            except:
               likes = "0"
            try:
               links = tweet.find_elements(By.CSS_SELECTOR,'a[role="link"]')
            except:
               views = "0"
            #get the last link which is the views
            else:
               views = links[len(links)-1].text
            date_scraped = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
               date_tweeted = tweet.find_element(By.CSS_SELECTOR,'time').get_attribute('datetime')
            except:
               date_tweeted = "Null"
            values= (tweet_text, likes, comments, retweets, views, date_tweeted, date_scraped)
            # replace any empty values with 0
            values = [value if value != "" else "0" for value in values]

            # check if the tweet is already in the database by tweet_id
            if cur.execute("SELECT * FROM tweets WHERE tweet = (?)", (tweet_text,)).fetchone() == None:
               # add to database
               cur.execute("INSERT INTO tweets(trend_id, tweet, likes, comments, retweets, views, date_tweeted, date_retrieved) VALUES (?,?,?,?,?,?,?,?)", (trend_id, values[0], values[1], values[2], values[3], values[4], values[5], values[6]))

            ## write all of values seperated by a unique key that likely wont show up in the tweet to the file
            ## FOR TESTING ONLY
            # file.write("%_*".join(values)+"\n")
            # file.write("--------------------------------------------------\n")

         # Scroll down to bottom
         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

         # Wait to load page
         time.sleep(0.5)
         i+= len(tweets)
         con.commit()

      ## FOR TESTING ONLY
      # file.close()
