# MongoDB にスクレイピングした結果を保存
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
  response = session.get("https://gihyo.jp/dp") # ページを取得
  urls = scrape_list_page(response) # 詳細(商品)ページURLリストを抽出
  
  for url in urls: # 詳細(商品)ページ
    key = extract_key(url) # URLからkeyとなる部分を抽出
    ebook = collection.find_one({"key": key}) # DBにkeyが存在するか確認
  
    if not ebook: # DB に存在しない
      time.sleep(1)
      response = session.get(url)
      ebook = scrape_detail_page(response) # 詳細(商品)情報を抽出
      collection.insert_one(ebook) # DBに保存
  
  print(ebook)

# 詳細(商品)ページのURLリストを取得
def scrape_list_page(response: requests.Response):
  html = lxml.html.fromstring(response.text)
  html.make_links_absolute(response.url)
  
  for a in html.cssselect("#listBook > li > a[itemprop='url']"):
    url = a.get("href")
    yield url

# 詳細(商品)情報を抽出
def scrape_detail_page(response: requests.Response) -> dict:
  html = lxml.html.fromstring(response.text)
  ebook = {"url": response.url,
           "key": extract_key(response.url),
           "title": html.cssselect("#bookTitle")[0].text_content(),
           "price": html.cssselect(".buy")[0].text.strip(),
           "content:": [ normalize_space(h3.text_content()) for h3 in html.cssselect("#content > h3")]
           }
  return ebook

# URL からkeyの部分を抽出
def extract_key(url: str) -> str:
  m = re.search(r"/([^/]+)$", url) # 最後の/から末尾
  return m.group(1)

# 1回以上の空白を1つの空白に置換
def normalize_space(s: str) -> str:
  return re.sub(r"\s+"," ",s).strip()

if __name__ == "__main__":
  main()