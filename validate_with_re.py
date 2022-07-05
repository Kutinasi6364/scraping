import re

def validate_price(value: str):
  if not re.search(r"^[0-9,]+$", value):
    raise ValueError(f"Inbalid price: {value}")

validate_price("3000")
validate_price("無料")