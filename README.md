[![PyPI version](https://badge.fury.io/py/morpholog.svg)](https://badge.fury.io/py/morpholog)

## Morpholog

Morpholog is a tool for dealing with morphological structure of russian words. 

![img](https://sun4-16.userapi.com/NGih2EKrWiPGqxnM2UvrBHrqgK2RcifpL_ADxw/GsPww6CXevs.jpg)


## Get started

Installation:

```

pip install morpholog

```

## Documentation

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

morph.root_words('город',print_root=True)

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

4) Convert a verbal noun into a verb

```

morph.noun2verb('оформление')

'оформить'

```

4) Convert a particle into a verb

```

morph.ptcp2verb('отправленный')

'отправить'

```

### What about neologisms?

Many neologisms are not presented in the dictionary, so, Morpholog 'makes guess' about it:

```
morph.tokenize('чилить')

[['чил', '+ить']]

morph.noun2verb('хайп')

'хайпить'

morph.noun2verb('хардкор')

'хардкорить

```
