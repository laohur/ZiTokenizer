# ZiTokenizer

ZiTokenizer: tokenize word as Zi

read word as Zi

word = prefix + root + suffix


## use
* pip install ZiTokenizer
* toeknize language frequency and count word frequency (https://github.com/laohur/UnicodeTokenizer/blob/master/test/count_lang/count_word.py)
```python
from ZiTokenizer.ZiTokenizer import ZiTokenizer

# build 
tokenizer = ZiTokenizer(dir) # dir includ "word_frequency.tsv"
tokenizer.build(min_ratio=2e-6, min_freq=1)

# use
tokenizer = ZiTokenizer(dir)
line = "'〇㎡[คุณจะจัดพิธีแต่งงานเมื่อไรคะัีิ์ื็ํึ]Ⅷpays-g[ran]d-blanc-élevé » (白高大夏國)😀熇'\x0000𧭏"
tokens = tokenizer.tokenize(line)
print(tokens)
```
