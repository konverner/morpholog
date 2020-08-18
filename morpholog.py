'''

Constantin Werner , 18.08.2020
const.werner@gmail.com

'''

import pickle
import pymorphy2
import copy
from os import path

class Morpholog(pymorphy2.MorphAnalyzer):
  def __init__(self):
    super().__init__()
    self.map = copy.deepcopy(pickle.load(open("/content/map.pickle", 'rb')))
    self.words = sorted(list(self.map.keys()))
    
    self.prefixes = ['с','вы','до','за','над','об','от','пере','по','под','анти','архи','де','дез','дис','ин','контр','ре','суб','экс','пре','при']
    self.suffixes = ['ик','ек','ок','ёк','еньк','оньк','ечк','очк','ушк','юшк','ышк','ник','чик','щик','тель','ист','ск','ов','ев','н','ти','чь','ова','ева']
    self.postfixes = ['ся', 'cь']
    self.endings = ['а','я','ы','и','у','ю','ой','ей','и','ю','ой','ей','е','о','ом','ем','ая','яя','ое','ее','ого','его','ому','ему','ом','ем','их','ых','ими','ыми','им','ым','ую','юю','ой','ей','ешь','ете','ем','ут','ют','ишь','ите','ат','ят','им']

  def root_words(self,word, print_root=False):
    result = []

    root = self.get_roots(word)[0][0]
    if (print_root == True):
      print("ROOT: ", root)

    for word_i in self.words:
      morphemes_i = self.map[word_i]
      if (morphemes_i):
        if (root in morphemes_i):
          result.append(word_i)
      
    return result

  def is_trans(self,verb):
    return ('tran' in self.parse(verb)[0].tag)


  def noun2verb(self,noun):
    noun_morphems = self.tokenize(noun)[0]
    for verb in self.words:
      if (verb[0] > noun[0]):
        return None 
      verb_morphems = self.map[verb]
 

      if (verb_morphems and noun_morphems):
        
        if ('-' in verb_morphems[0] and '-' in noun_morphems[0]
          and verb_morphems[0] == noun_morphems[0]):
          n = len(verb_morphems)
          if (n > 3):
            if (verb_morphems[1][:2] == noun_morphems[1][:2] and verb_morphems[-1] == '+ть'):
              return verb
          if (n > 1):
            if (verb_morphems[1][:2] == noun_morphems[1][:2] and verb_morphems[-1] == 'ть'):
              return verb

        else:
          if (verb_morphems[0] == noun_morphems[0]):
            return verb

  def _tokenize_unk(self,word):
    result = []
    temp = word
    

    for postfix in self.postfixes:
      if (postfix in temp and -temp.index(postfix) == -len(temp)+len(postfix)):
        result.append('-'+postfix)
        temp = temp[:temp.index(postfix)]
        postfix = True
    
    
    for ending in self.endings:
      if (ending in temp and word.index(ending)+len(ending) == len(word)):
        result.append('+'+ending)
        temp = temp[:temp.index(ending)]
        break;
    
    
    for suffix in self.suffixes:
      if (suffix in temp and word.index(suffix)+len(suffix) == len(word)):
        result.append('-'+suffix+'-')
        temp = temp[:temp.index(suffix)] + temp[len(suffix):]
        break;
    for prefix in self.prefixes:
      if (prefix in temp and temp.index(prefix) == 0):
        result.append(prefix+'-')
        temp = temp[len(prefix):len(temp)]
        break;

    result.append(temp)
    
    formated = [None]*6
    if ('' in result): result.remove('')
    if result != []:
      for morpheme in result:
        if (morpheme[-1] == '-'):
          formated[0] = morpheme
        elif (morpheme[-1] == '-' and morpheme[0] == '-'):
          formated[2] = morpheme
        elif ('-' not in morpheme):
          formated[1] = morpheme
        elif (morpheme[0] == '+'):
          formated[3] = morpheme
        elif (morpheme[0] == '-'):
          formated[4] = morpheme

      return [morpheme for morpheme in formated if morpheme != None]
    return None

      

  def tokenize(self,data):
    
    result = list()

    data = data.split(' ')

    for word in data:
      word = word.lower()
      normal_form = None
      # flag is True if there is ending in word
      flag = False

      if word not in self.words:
        normal_form = self.normalize(word)
      else:
        normal_form = word

      if normal_form not in self.words:
        result.append(self._tokenize_unk(normal_form))
      
      else:
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
          result.append(tokenized)
        
        for i in range(len(tokenized)):
          if ('j' in tokenized[i]):
            tokenized[i] = tokenized[i].replace('j', '')
        result.append(tokenized)
    
    return result


  def normalize(self,word):
    return self.parse(word)[0].normalized.word
  
  def get_roots(self,word):
    morphemes = self.tokenize(word)
    roots = list()
    for morphem in morphemes:
      if '-' not in morphem and '+' not in morphem:
        roots.append(morphem)
    return roots
