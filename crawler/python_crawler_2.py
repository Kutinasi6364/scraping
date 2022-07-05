from typing import Iterator
import requests
import lxml.html

def main():
  response = requests.get("https://gihyo.jp/dp")
  urls = scrape_list_page(response)
  
  for url in urls:
    print(url)

def scrape_list_page(response: requests.Response) -> Iterator[str]:
  html = lxml.html.fromstring(response.text)
  html.make_links_absolute(response.url)
  
  for a in html.cssselect("#listBook > li > a[itemprop='url']"):
    url = a.get("href")
    yield url
    
if __name__ == "__main__":
  main()