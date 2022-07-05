from urllib.parse import urljoin
from bs4 import BeautifulSoup

cnt = 0
book_url = []
book_title = []

# スクレイピングの実行
soup = BeautifulSoup(open("dp.html", encoding="UTF-8"), "html.parser")

item_url = soup.find_all("a", attrs={"itemprop": "url"})
item_title = soup.find_all("p", attrs={"itemprop": "name"})

for i in item_url:
  # ebookを含むURLのみ
  if "ebook" in i.get("href"):
    # 絶対パスで取得
   book_url.append(urljoin("https://gihyo.jp/", i.get("href")))
   break

for i in item_title:
  book_title.append(i.text)

for cnt in range(len(book_url)):
  print(book_url[cnt] + " " + book_title[cnt])