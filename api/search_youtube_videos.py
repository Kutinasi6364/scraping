# youtube 動画を検索 簡易
import os
from dotenv import load_dotenv
from apiclient.discovery import build

load_dotenv(".env")

API_KEY = os.environ.get("KEY")

# youtube へのアクセスと情報を取得
youtube = build("youtube", "v3", developerKey=API_KEY)

# 検索条件を指定 手芸動画のプロパティ取得
serarch_response = youtube.search().list(part="snippet", # id or snippet
                                         q="サンシャイン池崎", # 検索クエリ
                                         type="video").execute() # channel playlist video

# 出力
for item in serarch_response["items"]:
  print(item["snippet"]["title"])