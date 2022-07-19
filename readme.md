# ZiTokenizer

ZiTokenizer: tokenize word as Zi

read word as Zi

word = prefix + root + suffix

support 175 languages + global 
## use
* pip install ZiTokenizer
* toeknize language frequency and count word frequency (https://github.com/laohur/UnicodeTokenizer/blob/master/test/count_lang/count_word.py)
```python
from ZiTokenizer.ZiTokenizer import ZiTokenizer

# use
tokenizer = ZiTokenizer(lang="global")  # lang='ar', 'en', 'fr', 'ru', 'zh' ...
line = "'〇㎡[คุณจะจัดพิธีแต่งงานเมื่อไรคะัีิ์ื็ํึ]Ⅷpays-g[ran]d-blanc-élevé » (白高大夏國)熵😀'\x0000熇"
tokens = tokenizer.tokenize(line)
print(' '.join(tokens)) # ' 〇 ㎡ [ ค ณ-- จ-- ะ --จ ด-- พ ธ แต ง-- งา-- น-- เม อไ-- ร --ค --ะ ] ##s ht pays - g [ ran ] d - blanc - eleve » ( 白 高 大 夏 國 ) ⿰ 火 商 ##g ce ' 00 ⿰ 火 高

# build 
tokenizer = ZiTokenizer(mydir) # mydir include "word_frequency.tsv"
tokenizer.build(min_ratio=2e-6, min_freq=1)
tokenizer = ZiTokenizer(dir=mydir)

```
