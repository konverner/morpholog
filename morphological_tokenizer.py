import mwclient
import re

class Morpholog:
  def __init__(self):
    self.base = mwclient.Site('ru.wiktionary.org')

  def parse(self, word):
    result = None
    page = self.base.pages[word]
    temp = page.text().split("\n\n")
    for i in range(len(temp)):
      if ('морфо-ru' in temp[i]):
        result = temp[i].split('|')[1:]
    if (result != None):
      result[-1] = result[-1].replace('}','')
      if 'и=т' in result:
        del result[result.index('и=т')]
    return result
  
  def get_roots(self, word):
    result = list()
    temp = self.parse(word)
    if (temp == None): 
      return None
    else:
      for i in range(len(temp)):
        if ('-' not in temp[i] and '+' not in temp[i] and '=' not in temp[i]):
          result.append(temp[i])
      return result
    
  def define(self, word):
    page = self.base.pages[word]
    temp = page.text().split("\n\n")
    for i in range(len(temp)):
      if ('=== Значение ===' in temp[i]):
        result = temp[i].split("\n#")[1:]
        return result
    return None
