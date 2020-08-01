# Morphological Tokenizer

Morphological tokenizer for Russian is able to split words into morphemes: prefixes, roots, infixes and postfixes 

![img](https://sun4-16.userapi.com/NGih2EKrWiPGqxnM2UvrBHrqgK2RcifpL_ADxw/GsPww6CXevs.jpg)

# Get started 

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

\*- prefix
\* - root
-\* postfix
-\*- infix
+\* - ending

Also, Morpholog class is able to define a word and extract a root

```

result = morph.get_roots('картограф')
result
['карт', 'граф']

morph.define('картограф')
[' [[специалист]] в области [[картографии]] {{пример|}}', ' ']

```
