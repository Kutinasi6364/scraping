# バリデーションを定義
from jsonschema import validate

# バリデーション
schema = {"type": "object", # オブジェクト
          "properties": {
            "name": {"type": "string"}, # 文字列
            "price": {"type": "string", "pattern": "^[0-9,]+$"} # 数値と,のみ
          },
          "required": ["name", "price"] # 必須
        }

validate({"name": "ぶどう", "price": "3000"}, schema) # OK
validate({"name": "みかん", "price": "無料"}, schema) # 例外発生