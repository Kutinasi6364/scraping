# ステータスコード別エラー処理
import time
import requests

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

# 
def fetch(url:str) -> requests.Response:
  # リトライ回数
  max_retries = 3
  retries = 0
  
  while True:
    try:
      print(f"Retrieving {url}...")
      # ステータス取得
      response = requests.get(url)
      print(f"Status: {response.status_code}")
      
      # ｴﾗｰｺｰﾄﾞ一覧ければ response を返す
      if response.status_code not in TEMPORARY_ERROR_CODES:
        return response
    # その他エラーの場合はログを出力
    except requests.exceptions.RequestException as ex:
      print(f"Network-lebel exception occured: {ex}")
    
    # リトライ数カウント
    retries += 1
    
    # リトライ回数チェック
    if retries >= max_retries:
      raise Exception("Too many retries.")
    
    # 待機時間
    wait = 2**(retries -1)
    print(f"Waiting {wait} seconds...")
    time.sleep(wait)
    
if __name__ == "__main__":
  main()