[![PyPI version](https://badge.fury.io/py/morpholog.svg)](https://badge.fury.io/py/morpholog)

## Morpholog

Morpholog is tool for dealing with morphological structure of a russian word. 
It can tokenize words into morphemes: prefixes, roots, infixes and postfixes, find same-root words and convert verbal noun into verb.  

![img](https://sun4-16.userapi.com/NGih2EKrWiPGqxnM2UvrBHrqgK2RcifpL_ADxw/GsPww6CXevs.jpg)


## Get started

Installation:

```

pip install morpholog

```

1) Tokenize word into morphemes:


```

from morphological_tokenizer Morpholog

morph = Morpholog()
morph.tokenize('ДОИМПЕРИАЛИСТИЧЕСКИМ')
['до-', 'империал', '-ист-', '-ическ-', '+им']

```

token- : prefix

token : root

-token- : infix

+token : ending

-token : postfix


2) Get roots of word

```

from morphological_tokenizer Morpholog

morph = Morpholog()
morph.get_roots('картограф')
['карт', 'граф']


```

3) Find same-root words of the given word

```

morph.root_words('город')

ROOT:  город
['выгородить',
 'выгородиться',
 'городить',
 
  ...
 
 'по-городски',
 'подгородить',
 'подгородный',
 'полгорода',
 'пригород',
 'пригородить',
 'пригородный',
 'разгородить',
 'разгородиться']

```

4) Convert verbal noun into verb

```

morph.noun2verb('оформление')

'оформить'

```

