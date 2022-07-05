# 動かない WikiExtractor.py が原因
from importlib.resources import path
import sys
import logging
from collections import Counter
from pathlib import Path
from typing import List, Iterator, TextIO
import MeCab

tagger = MeCab.Tagger('')
tagger.parse('')

def main():
  input_dir = Path(sys.argv[1])
  frequency = Counter()
  
  for path in sorted(input_dir.glob('*/wiki_*')):
    logging.info(f"Processing {path}...")
    
    with open(path) as file:
      frequency += count_words(file)
    
    for word, count in frequency.most_common(30):
      print(word, count)

def count_words(file: TextIO) -> Counter:
  frequency = Counter()
  num_docs = 0
  
  for content in iter_doc_contents(file):
    words = get_words(content)
    frequency.update(words)
    num_docs += 1
  
  logging.info(f"Fount {len(frequency)} words from {num_docs} documents.")
  return frequency

def iter_doc_contents(file: TextIO) -> Iterator[str]:
  for line in file:
    if line.startswith("<doc"):
      buffer = []
    elif line.startswith("</doc>"):
      content = ''.join(buffer)
      yield content
    else:
      buffer.append(line)

def get_words(content: str) -> List[str]:
  words = []
  node = tagger.parseToNode(content)
  
  while node:
    pos, pos_sub1 = node.feature.split(",")[:2]
    
    if pos == "名刺" and pos_sub1 in ("固有名詞", "一般"):
      words.append(node.surface)
    
    node = node.next
  return words

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  main()