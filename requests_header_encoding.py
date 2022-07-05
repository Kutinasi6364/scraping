import io
import sys
import requests

# 標準入出力からのリダイレクトの文字コードを「utf-8」にする
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url = sys.argv[1] # 指定URL
r = requests.get(url) # webページゲット

print(f'encoding: {r.encoding}',file = sys.stderr) # エンコーディングを標準エラー出力に出力する。
print(r.text) # デコードしたレスポンスボディを標準出力に出力する。