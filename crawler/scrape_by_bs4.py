from urllib.parse import urljoin
from bs4 import BeautifulSoup

with open("dp.html", encoding="UTF-8") as f:
  soup = BeautifulSoup(f, "html.parser")

# listBook クラス内の li タグ内の aタグ itemprop=url
for a in soup.select("#listBook > li > a[itemprop='url']"):
  url = urljoin("https://githo.jp/dp", a.get("href"))

  p = a.select("p[itemprop='name']")[0]
  title = p.text

  print(url, title)