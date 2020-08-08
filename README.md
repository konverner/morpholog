[![PyPI version](https://badge.fury.io/py/morpholog.svg)](https://badge.fury.io/py/morpholog)

## Morphological Tokenizer

Morphological tokenizer for Russian is able to split words into morphemes: prefixes, roots, infixes and postfixes 

![img](https://sun4-16.userapi.com/NGih2EKrWiPGqxnM2UvrBHrqgK2RcifpL_ADxw/GsPww6CXevs.jpg)


## Get started

Installation:

```

pip install morpholog

```


Tokenize word into morphemes:


```

from morphological_tokenizer Morpholog

morph = Morpholog()
morph.tokenize('ДОИМПЕРИАЛИСТИЧЕСКИМ')
['до-', 'империал', '-ист-', '-ическ-', '+им']

```

torken- : prefix

token : root

-token- : infix

+token : ending

-token : postfix


Get roots of word

```

from morphological_tokenizer Morpholog

morph = Morpholog()
morph.get_roots('картограф')
['карт', 'граф']


```

## Use Case

In Russian language, one can convert a verb into verbal noun (e.g. создать -> создание). So, it would be useful to 
convert a verbal noun into a verb because some rule-based algorithms work with verb phrases to extract entities from 
a sentence. We can do it with knowing its morphological roots, for example

```
morph1 = Morpholog()

result1 = morph1.get_roots('оплатить') # verb
result2 = morph1.get_roots('оплата') # verbal noun

print(result1, result2)
['плат'] ['плат'] # they have same roots

```
