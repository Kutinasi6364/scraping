import MeCab

tagger = MeCab.Tagger()
tagger.parse('')

# 形態素を表すNodeオブジェクト
node = tagger.parseToNode("すもももももももものうち")

while node:
  # surface 形態素文字列 feature 品詞文字列
  print(node.surface, node.feature)
  node = node.next # 次のNode
  