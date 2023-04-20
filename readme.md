# ZiTokenizer

Tokineze all languages text into Zi.

support 300+ languages from wikipedia, including global 


## use
* pip install ZiTokenizer

```python
from ZiTokenizer.ZiTokenizer import ZiTokenizer

# use
tokenizer = ZiTokenizer()  
line = "'〇㎡[คุณจะจัดพิธีแต่งงานเมื่อไรคะัีิ์ื็ํึ]Ⅷpays-g[ran]d-blanc-élevé » (白高大夏國)😀熇'\x0000𧭏2022２０１９\U0010ffff"
indexs = tokenizer.encode(line)
tokens = tokenizer.decode(indexs)
line2=tokenizer.tokens2line(tokens)

# build
demo/unit.py
```

## UnicodeTokenizer
basic tokeinzer

## ZiCutter
汉字拆字
> '瞼' -> ['⿰', '目', '僉']

## ZiSegmenter
word => prefix + root + suffix
> 'modernbritishdo' -> ['mod--', 'er--', 'n--', 'british', '--do']

## languages
default using "golabl" vocob, others from https://laohur.github.io/ZiTokenizer/index.html
> tokenizer = ZiTokenizer(vocab_dir)  
