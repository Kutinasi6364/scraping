from logging import exception
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

# Timeout ｻｰﾊﾞｰｴﾗｰ ｹﾞｰﾄｳｪｲ ﾘｸｴｽﾄ処理不可 ｹﾞｰﾄｳｪｲﾀｲﾑｱｳﾄ
TEMPORARY_ERROR_CODES = (408, 500, 502, 503, 504) # 一時的エラーを返す

def main():
  # ｽﾃｰﾀｽｺｰﾄﾞ 200, 404, 503 をランダムに返すURL
  response = fetch("http://httpbin.org/status/200,400,503")
  # エラー有り無し
  if 200 <= response.status_code < 300:
    print("Success")
  else:
    print("Error")

# デコレータ stop=3回リトライで終了 wait=指数関数敵に待機時間を増やす(一回目)
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1))
def fetch(url: str) -> requests.Response:
  print(f"Retrieving {url}...")
  # ステータス取得
  response = requests.get(url)
  print(f"Status: {response.status_code}")
      
  # ｴﾗｰｺｰﾄﾞ一覧ければ response を返す
  if response.status_code not in TEMPORARY_ERROR_CODES:
    return response
  
  # 一般エラーはリトライ
  raise exception(f"Temporary Error: {response.status_code}")

if __name__ == "__main__":
  main()