'''

Constantin Werner , 27.08.2020
const.werner@gmail.com

'''

import pickle
import pymorphy2
import copy
from os import path

class Morpholog(pymorphy2.MorphAnalyzer):
  def __init__(self):
    super().__init__()
    self.map = copy.deepcopy(pickle.load(open(path.join(path.dirname(__file__), "map.pickle"), 'rb')))
    self.words = sorted(list(self.map.keys()))
    self.util = dict() # it stores indecies of first occurences of words with the given first letter
    
    for i in range(len(self.words)):
      first_letter = self.words[i][0]
      if first_letter not in self.util.keys():
        self.util[first_letter] = i
    

    self.vowels = ['а', 'у', 'о', 'ы', 'и', 'э', 'я', 'ю', 'ё', 'е']
    self.consonants =  ['б', 'в', 'г', 'д', 'ж', 'з', 'й', 'к', 'л', 'м', 'н', 'п', 'р', 'с', 'т', 'ф', 'х', 'ц', 'ч', 'ш', 'щ']
    self.prefixes = ['с','вы','до','за','над','об','от','пере','по','под','анти','архи','де','дез','дис','ин','контр','ре','суб','экс','пре','при']
    self.suffixes = ['ик','ек','ок','ёк','еньк','оньк','ечк','очк','ушк','юшк','ышк','ник','чик','щик','тель','ист','ск','ов','ев','н','ти','чь','ова','ева']
    self.postfixes = ['ся', 'cь']
    self.endings = ['а','я','ы','и','у','ю','ой','ей','и','ю','ой','ей','е','о','ом','ем','ая','яя','ое','ее','ого','его','ому','ему','ом','ем','их','ых','ими','ыми','им','ым','ую','юю','ой','ей','ешь','ете','ем','ут','ют','ишь','ите','ат','ят','им']

  def root_words(self,word, print_root=False):
    result = []

    roots = self.get_roots(word)
    
    if roots == None:
      return word

    for root in roots:
      temp = []
      if (print_root == True):
        print("ROOT: ", root)

      for word_i in self.words:
        if (root in word_i):
          roots_word_i = self.get_roots(word_i)
          if roots_word_i != None:
            for root_word_i in roots_word_i:
              if root_word_i == root:
                temp.append(word_i)
      result.append(temp)
      
    return result
  
  def _get_most_similiar(self, target,cands):
    
    scores = dict()

    for cand in cands:
      scores[cand] = 0
      for i in range(min(len(target),len(cand))):
        if (target[i] == cand[i]):
          scores[cand] += 1
        elif ((target[i] == 'е' and cand[i] == 'и') or\
              (target[i] == 'и' and cand[i] == 'е')):
          scores[cand] += 1
    
    max_score = -1
    max_cand = None 
    for cand in cands:
      if scores[cand] > max_score:
        max_cand = cand
        max_score = scores[cand]
    return max_cand



  def is_trans(self,verb):
    return ('tran' in self.parse(verb)[0].tag)


  def ptcp2verb(self,ptcp):

    if ('PRTF' not in self.parse(ptcp)[0].tag and 'PRTS' not in self.parse(ptcp)[0].tag):
      return None

    ptcp_root = self.get_roots(ptcp)[0]
    ptcp_prefix = self.get_prefix(ptcp)

    # words that can be a verb we are looking for
    candidates = []

    idx = self.util[ptcp[0]]
    for i in range(idx,len(self.words)):
      word = self.words[i]
      if (len(word) > 2): 
        if (word[0] > ptcp[0] or word[1] > ptcp[1]):
            break 
        if (word[0] == ptcp[0]):
          if ("INFN" in self.parse(word)[0].tag):
            verb_morphemes = self.map[word]
            if verb_morphemes != None and verb_morphemes != []: 
              if '-' in verb_morphemes[0]:
                if (verb_morphemes[0] == ptcp_prefix):
                  if (len(verb_morphemes) > 1):
                    if (verb_morphemes[1] == ptcp_root):
                      candidates.append(word)
              else:
                if (verb_morphemes[0] == ptcp_root):
                  candidates.append(word)

    return self._get_most_similiar(ptcp,candidates)

  def noun2verb(self,noun):
    if ('UNKN' in self.parse(noun)[0].tag):
      if noun[-1] in self.consonants:
        return noun + 'ить'
      return noun + 'ть'

    if ('NOUN' not in self.parse(noun)[0].tag):
      return None

    noun_root = self.get_roots(noun)[0]
    noun_prefix = self.get_prefix(noun)

    # words that can be a verb we are looking for
    candidates = []

    idx = self.util[noun[0]]
    for i in range(idx,len(self.words)):
      word = self.words[i]
      if (len(word) > 2): 
        if (word[0] > noun[0] or word[1] > noun[1]):
            break 
        if (word[0] == noun[0]):
          if ("INFN" in self.parse(word)[0].tag):
            verb_morphemes = self.map[word]
            if verb_morphemes != None and verb_morphemes != []: 
              if '-' in verb_morphemes[0]:
                if (verb_morphemes[0] == noun_prefix):
                  if (len(verb_morphemes) > 1):
                    if (verb_morphemes[1] == noun_root):
                      candidates.append(word)
              else:
                if (verb_morphemes[0] == noun_root):
                  candidates.append(word)
    if candidates == []:
      if noun[-1] in self.consonants:
        return noun + 'ить'
      return noun + 'ть'
    return self._get_most_similiar(noun,candidates)


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
    
    if word in self.map.keys() and self.map[word] != []:
      morphemes = self.map[word]
    else:
      morphemes = self.tokenize(word)[0]
      
    roots = list()
    if morphemes != None: 
      for morphem in morphemes:
        if '-' not in morphem and '+' not in morphem:
          roots.append(morphem) 
    if roots == []:
      return None
    return roots
  
  def get_prefix(self,word):
    if word in self.map.keys():
      morphemes = self.map[word]
    else:
      morphemes = self.tokenize(word)[0]
    
    if morphemes != None:
      for morpheme in morphemes:
        if len(morpheme) > 1:
          if morpheme[-1] == '-':
            return morpheme
    return ''

  def get_ending(self,word):
    if word in self.map.keys():
      morphemes = self.map[word]
    else:
      morphemes = self.tokenize(word)[0]

    if morphemes != None:
      for morpheme in morphemes:
        if (len(morpheme) > 1):
          if morpheme[0] == '+':
            return morpheme
