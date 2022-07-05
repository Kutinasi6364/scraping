# youtube データをMongoDBへ
import os
# import logging

from typing import Iterator, List
from dotenv import load_dotenv
from apiclient.discovery import build
from pymongo import MongoClient, ReplaceOne, DESCENDING
from pymongo.collection import Collection

load_dotenv(".env")
API_KEY = os.environ.get("KEY")
# logging.getLogger("googleapiclient.discovery_cache").setLevel(logging.ERROR) # 不要なログを出力しない

max_page = 1 # 検索するページ数
search_query = "サンシャイン池崎" # 検索内容
search_limit = 20 # 表示する件数

def main():
  client = MongoClient("localhost", 27017) # DB設定
  collection = client.youtube.videos # youtubeDB videos コレクションを指定
  
  # 動画を検索する項目とページ数
  for items_per_page in search_videos(search_query, max_page):
    save_to_mongodb(items_per_page) # MongoDB保存処理 collection,
  
  show_top_videos(collection) # ビューの多い動画を表示

# MAX_PAGE 分検索を行う
def search_videos(query: str, max_pages: int) -> Iterator[List[dict]]:
  i = 0 # 検索ページカウント用
  youtube = build("youtube", "v3", developerKey=API_KEY) # 接続
  
  search_request =  youtube.search().list(part="id", # id or snippet
                                         q=query, # 検索クエリ
                                         type="video", # channel playlist video
                                         maxResults=50) # 1ページ50件取得

  while search_request and i < max_pages:
    search_response = search_request.execute() # 検索実行
    video_ids = [item["id"]["videoId"] for item in search_response["items"]] # 動画のID取得
    
    # 動画の情報取得
    videos_response = youtube.videos().list(part="snippet, statistics",
                                            id=",".join(video_ids)
                                            ).execute()
    yield videos_response["items"]
    
    search_request = youtube.search().list_next(search_request, search_response)
    i += 1 # ページカウント
    
def save_to_mongodb(items: dict): # collection: Collection, 
  for item in items:
    item["_id"] = item["id"] # MongoDB _id = 動画 id
    
    # 動画情報をDBに保存
    for key, value in item["statistics"].items():
      item["statistics"][key] = int(value)
    
    # operations = [ReplaceOne({"_id": item["id"]}, item, upsert=True) for item in items]
    # result = collection.bulk_write(operations)
    # logging.info(f"Upserted {result.upserted_count} documents.")
    
def show_top_videos(collection: Collection):
  for item in collection.find().sort("statistics.viewCount", DESCENDING).limit(search_limit): 
    print(item["statistics"]["viewCount"], item["snippet"]["title"]) # 上位20件表示

if __name__ == "__main__":
  # logging.basicConfig(level=logging.INFO)
  main()