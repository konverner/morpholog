import pickle
import pymorphy2
import copy
from os import path

class Morpholog(pymorphy2.MorphAnalyzer):
  def __init__(self):
    super().__init__()
    self.map = copy.deepcopy(pickle.load(open(path.join(path.dirname(__file__), "map.pickle"), 'rb')))


  def tokenize(self,word):
    
    # flag is True if there is ending in word
    flag = False
    
    normal_form = self.normalize(word)

    word = word.lower()
    if normal_form not in self.map.keys():
      return [word]
    tokenized = copy.deepcopy(self.map[normal_form])
    if (tokenized == [] or tokenized == None):
      tokenized = [normal_form]
    if (word != normal_form):
      temp = word
      for i in range(len(tokenized)):
        temp = temp.replace(tokenized[i].replace('-', ''), '')
        if ('+' in tokenized[i]):
          tokenized[i] = '+' + word[-(len(tokenized[i])-1):]
          flag = True
      if (flag == False):
        tokenized.append("+"+temp)
      return tokenized
    
    for i in range(len(tokenized)):
      if ('j' in tokenized[i]):
        tokenized[i] = tokenized[i].replace('j', '')
    return tokenized


  def normalize(self,word):
    return self.parse(word)[0].normalized.word
  
  def get_roots(self,word):
    morphemes = self.tokenize(word)
    roots = list()
    for morphem in morphemes:
      if '-' not in morphem and '+' not in morphem:
        roots.append(morphem)
    return roots
