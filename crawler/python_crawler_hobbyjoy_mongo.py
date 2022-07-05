# MongoDB仕様
import re
import time
import requests
import lxml.html
from pymongo import MongoClient

def main():
  client = MongoClient("localhost", 27017) # DB設定
  collection = client.scraping.article # scrapingDB article コレクションを指定
  collection.create_index("key", unique=True) # Unique キーを作成

  session = requests.Session()
  response = session.get("https://kutinasi-hobbyjoy.com/") # ページを取得
  urls = scrape_list_url(response) # 詳細(商品)ページURLリストを抽出
  
  for url in urls: # 詳細(商品)ページ
    keyurl = extract_key(url) # URLからkeyとなる部分を抽出
    hobbyjoy = collection.find_one({"key": keyurl}) # DBにkeyが存在するか確認
  
    if not hobbyjoy: # DB に存在しない
      time.sleep(1)
      response = session.get(url)
      hobbyjoy = scrape_detail_page(response. key) # 詳細(商品)情報を抽出
      collection.insert_one(hobbyjoy) # DBに保存
  
  print(hobbyjoy)

# 詳細(商品)ページのURLリストを取得
def scrape_list_url(response: requests.Response):
  html = lxml.html.fromstring(response.text)
  html.make_links_absolute(response.url)
  
  for a in html.cssselect("#list > a"):
    url = a.get("href")
    yield url
    

# 詳細(商品)情報を抽出
def scrape_detail_page(response: requests.Response, key) -> dict:
  html = lxml.html.fromstring(response.text)
  hobbyjoy = {"url": response.url,
           "key": key,
           "title": normalize_space(html.cssselect("article[itemprop='blogPost'] > header > h1")[0].text_content()),
           "content:": [ normalize_space(h2.text_content()) for h2 in html.cssselect("h2 > span")]
           }
  return hobbyjoy

# URL からkeyの部分を抽出
def extract_key(url: str) -> str:
  keyurl = re.search(r"/([^/]+)/$", url) # 最後の/から末尾
  return keyurl.group(1)

# 1回以上の空白を1つの空白に置換
def normalize_space(s: str) -> str:
  return re.sub(r"\s+"," ",s).strip()

if __name__ == "__main__":
  main()