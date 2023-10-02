from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from datetime import date

chrome_options = Options()
#Put your own path to the chrome user data folder
chrome_options.add_argument(r"--user-data-dir=C:\Users\danie\AppData\Local\Google\Chrome\User Data")

chrome_options.add_argument("--headless")
# chrome_options.add_argument("--full-screen")

if __name__ == "__main__":
   # open the browser
   driver = webdriver.Chrome(options=chrome_options)
   # go to the twitter trending page
   driver.get("https://twitter.com/explore/tabs/trending")
   #click on the first trending topic
   driver.implicitly_wait(20)
   first_trending_topic = driver.find_element(By.XPATH, "//*[@id=\"react-root\"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/section/div/div/div[3]/div/div/div")
   hashtag=first_trending_topic.text   #save the topic to write to the file
   hashtag = hashtag.replace("\n", " ")
   first_trending_topic.click() #go to the topic page

   #write the header for a file with the tweets
   file_name = "tweets_from_"+str(date.today())+".txt"
   file = open(file_name, "w")
   file.write("Tweets from " + str(date.today()) +": Hashtag = "+str(hashtag)+"\n")
   file.write("--------------------------------------------------\n")

   tweets_dict = {}
   i=0
   j=0

   #loop until 50 unique tweets are found or 75 scrolls are done
   while i < 50 and j < 75:
      #mark all the tweets on the page
      tweets = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
      for tweet in tweets:
         #Save the tweet of the text in a dictionary
         tweet_text = tweet.find_element(By.CSS_SELECTOR,'div[data-testid="tweetText"]').text
         hashed = hash(tweet_text) #hash the tweet to check if it is unique or not
         if hashed not in tweets_dict:
            tweets_dict[hashed] = tweet_text
            i+=1
         
       # Scroll down to bottom
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

      # Wait to load page
      time.sleep(0.5)
      j+=1

   #write the tweets to the file
   for tweet in tweets_dict:
      file.write(tweets_dict[tweet] + "\n")
      file.write("--------------------------------------------------\n")

   #close the file and the browser
   file.close()