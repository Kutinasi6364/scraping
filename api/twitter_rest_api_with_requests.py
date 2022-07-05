import os
from requests_oauthlib import OAuth1Session

# enbiron で環境変数から認証情報を取得
TWITTER_API_KEY = ""
TWITTER_API_SECRET_KEY = ""
TWITTER_API_ACCESS_TOKEN = ""
TWITTER_API_ACCESS_TOKEN_SECRET = ""

twitter = OAuth1Session(TWITTER_API_KEY,
                        TWITTER_API_SECRET_KEY,
                        TWITTER_API_ACCESS_TOKEN,
                        TWITTER_API_ACCESS_TOKEN_SECRET)

# タイムラインの取得
response = twitter.get("https://api.twitter.com/1.1/statuses/home_timeline.json")
print(response)
# jsonでパース
for status in response.json():
  # ユーザー名とツイートを表示
  print("@" + status["user"]["screen_name"], status["text"])
  