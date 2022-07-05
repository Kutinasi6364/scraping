import requests
import lxml.html
import re

session = requests.Session()
response = session.get("https://kutinasi-hobbyjoy.com//mongodb/") # ページを取得
html = lxml.html.fromstring(response.text)


print(html.cssselect("article[itemprop='blogPost'] > header > h1")[0].text_content())
