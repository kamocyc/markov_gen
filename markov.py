import io, sys
import random
import MeCab

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

tagger = MeCab.Tagger('')
tagger.parse('')

with open('markov_data_4.txt', 'r') as f:
  text = f.read()
  
node = tagger.parseToNode(text)
mkdict = {}

def getInitPrevs(node, n = 3):
  prevs = []
  for i in range(1, n + 1):
    if node is None:
      return prevs, None
    
    prevs.append(node.surface)
    node = node.next
  
  return prevs, node

# tupleに変換（入れ子）
def makeTuple(ls: list)-> list: 
  t = (ls[0], ls[1])
  ls.remove(ls[0]) 
  ls.remove(ls[1])
  
  while ls:
    t = (t, ls[0])
    ls.remove(ls[0])
  
  return t
  
  
prevs, node = getInitPrevs(node)

while node:
  surface = node.surface
  tup = tuple(prevs)
  if tup in mkdict:
    # 存在
    mkdict[tup].append(surface)
  else:
    # 新規
    mkdict[tup] = [surface]
  
  prevs.remove(prevs[0])
  prevs.append(node.surface)
  node = node.next

# 辞書ができたのでランダムに次を選んでいく
# 最初はランダムに選ぶ

keylist = list(mkdict.keys())

key = random.choice(keylist)

print(key)

keyNum = len(keylist)
avgl = 0
for i in range(1, keyNum):
  avgl = avgl + len(mkdict[keylist[i]]) / keyNum

print(avgl)

for k in list(key):
  print(k, end = '')

for i in range(1, 1000):
  cands = mkdict[key]
  nextWord = random.choice(cands)
  print(nextWord, end = '')
  keyaslist = list(key)
  keyaslist.remove(keyaslist[0])
  keyaslist.append(nextWord)
  key = tuple(keyaslist)
  
