from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import datetime

"""
This program opens a chrome browser and goes to the twitter trending page.
It then clicks on the first few trending topics and scrolls down to load all the tweets.
It then saves the tweets and meta information into a sqlite database.

Database Schema:

trending
------------
id | trending_topic_name 

tweet
----------------
id | tweet | likes | comments | retweets | date tweeted | date retrieved | foreign key trending topic id
"""

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
   for trend in trends:
      trend_name= trend.find_elements(By.CSS_SELECTOR, 'span')[3].text
      trend_names.append(trend_name)

   #loop through all the trending topics
   for trend_name in trend_names:
      searchbox= driver.find_element(By.CSS_SELECTOR, '[data-testid="SearchBox_Search_Input"]')
      print(trend)
      #click the search button by sending cntrl+a and delete
      searchbox.send_keys(u'\ue009'+'a')
      searchbox.send_keys(u'\ue017')

      #check if the trend is promoted
      if trend_name.__contains__("Promoted"):
         continue
      #put the trend name in the search box
      searchbox.send_keys(trend_name)
      searchbox.send_keys(u'\ue007')

      #write the tweets to a file in the folder temp_holder_for_test
      file_name = trend_name + ".txt"
      file = open("temp_holder_for_test/"+file_name,"w",encoding="utf-8")
      file.write("Tweets from Trend = "+trend_name+"\n")
      file.write("--------------------------------------------------\n")

      i=0

      #loop until 50 unique tweets are found or 75 scrolls are done
      while i < 50:
         #mark all the tweets on the page
         tweets = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
         for tweet in tweets:
            #Save the tweet statistics to put into a database
            tweet_text = tweet.find_element(By.CSS_SELECTOR,'div[data-testid="tweetText"]').text
            tweet_id = str(hash(tweet_text))
            comments = tweet.find_element(By.CSS_SELECTOR,'div[data-testid="reply"]').text
            retweets = tweet.find_element(By.CSS_SELECTOR,'div[data-testid="retweet"]').text
            likes = tweet.find_element(By.CSS_SELECTOR,'div[data-testid="like"]').text
            links = tweet.find_elements(By.CSS_SELECTOR,'a[role="link"]')
            #get the last link which is the views
            views = links[len(links)-1].text
            date_scraped = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # date_tweeted = tweet.find_element(By.CSS_SELECTOR,'time').get_attribute('datetime')

            file.write("Tweet ID: "+tweet_id+"\n")
            file.write("Tweet: "+tweet_text+"\n")
            file.write("Comments: "+comments+"\n")
            file.write("Retweets: "+retweets+"\n")
            file.write("Likes: "+likes+"\n")
            file.write("Views: "+views+"\n")
            # file.write("Date Tweeted: "+date_tweeted+"\n")
            file.write("Date Scraped: "+date_scraped+"\n")
            file.write("--------------------------------------------------\n")

         # Scroll down to bottom
         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

         # Wait to load page
         time.sleep(0.5)
         i+= len(tweets)
      driver.refresh()
      file.close()