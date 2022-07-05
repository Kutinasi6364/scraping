# CacheControl でキャッシュを処理
import requests
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache

session = requests.Session()
# キャッシュは webcache に保存
cached_session = CacheControl(session, cache=FileCache(".webcache"))

response = cached_session.get("https://docs.python.org/3/")

print(f"from_cache: {response.from_cache}") # キャッシュからのレスポンス True or False
print(f"status_code: {response.status_code}") # ステータスコード
print(response.text)