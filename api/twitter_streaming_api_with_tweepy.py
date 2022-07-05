import os
import tweepy
from dotenv import load_dotenv

load_dotenv(".env")

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_KEY_SECRET")
TOKEN = os.environ.get("TOKEN")
TOKEN_SECRET = os.environ.get("TOKEN_SECRET")

def main():
  auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
  auth.set_access_token(TOKEN, TOKEN_SECRET)
  stream = tweepy.Stream(auth, MyStreamListener())
  stream.sample(languages=["ja"])

# ここで StreamListener がないといわれる^^;
class MyStreamListener(tweepy.StreamListener):
  def on_status(self, status: tweepy.Status):
    print("@" + status.author.screen_name, status.text)

if __name__ == "__main__":
  main()
