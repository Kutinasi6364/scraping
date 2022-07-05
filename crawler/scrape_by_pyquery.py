# pyquety encoding 不可
from pyquery import PyQuery as pq

with open("dp.html", encoding="UTF-8") as f:
  d = pq(f)

d = pq(filename="dp.html")
d.make_link_absolute("https://githo.jp/dp")

# listBook クラス内の li タグ内の aタグ itemprop=url
for a in d("#listBook > li > a[itemprop='url']"):
  url = d(a).attr("href")

  p = d(a).find("p[itemprop='name']")[0]
  title = p.text

  print(url, title)