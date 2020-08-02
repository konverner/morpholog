## Morphological Tokenizer

Morphological tokenizer for Russian is able to split words into morphemes: prefixes, roots, infixes and postfixes 

![img](https://sun4-16.userapi.com/NGih2EKrWiPGqxnM2UvrBHrqgK2RcifpL_ADxw/GsPww6CXevs.jpg)

## Get started

``` mwclient ``` module is required 


```

from morphological_tokenizer Morpholog

morph = Morpholog()

result = morph.parse('картограф')
print(result)
['карт', '-о-', 'граф']


result = morph.parse('бравирование')
print(result)
['брав', '-ир-', '-ова', '-ниj', '+е']

result = morph.parse('оформленный')
print(result)
['о-', 'формл', '-енн', '+ый']

```

torken- : prefix

token : root

-token : postfix

-token- : infix

+token : ending

Also, Morpholog class is able to define a word and extract a root

```

result = morph.get_roots('картограф')
result
['карт', 'граф']

morph.define('картограф')
[' [[специалист]] в области [[картографии]] {{пример|}}', ' ']

```

## Use Case

In Russian language one can convert a verb into verbal noun (e.g. создать -> создание). So, it would be useful to 
convert a verbal noun into a verb because some rule-based algorithms work with verb phrases to extract entities from 
a sentence. We can do it with knowing its morphological roots, for example

```
morph1 = Morpholog()

result1 = morph1.get_roots('оплатить') # verb
result2 = morph1.get_roots('оплата') # verbal noun

print(result1, result2)
['плат'] ['плат'] # they have same roots

```
