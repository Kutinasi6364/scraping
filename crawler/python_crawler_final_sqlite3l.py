# SQLite3 にスクレイピングした結果を保存
import re
import time
from typing import Iterator
import requests
import lxml.html
import sqlite3

# DB コネクション
conn = sqlite3.connect("crawler_final.db")
c = conn.cursor()

def main():
  # scraping テーブルの初期化
  c.execute("DROP TABLE IF EXISTS scraping")
  c.execute("CREATE TABLE scraping(url string, price string, content string)")
  
  session = requests.Session()
  response = requests.get("https://gihyo.jp/dp")
  urls = scrape_list_page(response)
  
  for url in urls:
    time.sleep(1)
    response = session.get(url)
    scrape_detail_page(response)
  
  # SQL 内容保存
  conn.commit()
  
  c.execute("SELECT * FROM scraping")
  # 結果を表示
  for row in c.fetchall():
    print(row)
  
  # コネクション 終了
  conn.close()

# イテレーターを使用
def scrape_list_page(response: requests.Response) -> Iterator[str]:
  html = lxml.html.fromstring(response.text)
  html.make_links_absolute(response.url)
  
  # スクレイピング結果を返す
  for a in html.cssselect("#listBook > li > a[itemprop='url']"):
    url = a.get("href")
    yield url

def scrape_detail_page(response: requests.Response) -> dict:
  html = lxml.html.fromstring(response.text)
  
  # DB へ登録
  for h3 in html.cssselect("#content > h3"):
    list = [(response.url, html.cssselect('.buy')[0].text.strip(), normalize_spaces(h3.text_content()))]
    c.execute("INSERT INTO scraping(url, price, content) VALUES (?, ?, ?)", (list[0]))

def normalize_spaces(s: str) -> str:
  return re.sub(r"\s+","",s).strip()

if __name__ == "__main__":
  main()