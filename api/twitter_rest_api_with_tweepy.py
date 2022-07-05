import os
import tweepy
from dotenv import load_dotenv

load_dotenv(".env")

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_KEY_SECRET")
TOKEN = os.environ.get("TOKEN")
TOKEN_SECRET = os.environ.get("TOKEN_SECRET")

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(TOKEN, TOKEN_SECRET)

api = tweepy.API(auth)
tweet_timeline = api.home_timeline()

for timeline  in tweet_timeline:
  print("@" + timeline.user.screen_name, timeline.text)