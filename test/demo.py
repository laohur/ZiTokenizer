import os

from logzero import logger

from UnicodeTokenizer.UnicodeTokenizer import UnicodeTokenizer
from ZiTokenizer.ZiSegmenter import ZiSegmenter
from ZiTokenizer.ZiTokenizer import ZiTokenizer


def get_langs():
    alphabet = ''.join(chr(x) for x in range(ord('a'), ord('z')+1))
    langs = [x+y for x in alphabet for y in alphabet]
    return langs


def test_segmenter():
    line = "'〇㎡[คุณจะจัดพิธีแต่งงานเมื่อไรคะัีิ์ื็ํึ]Ⅷpays-g[ran]d-blanc-élevé » (白高大夏國)😀熇'\x0000𧭏"
    roots = ['la', 'a', 'ay', 'le']
    prefixs = ['e', 'l']
    suffixs = ['n', 'e', 'v']
    words = UnicodeTokenizer().tokenize(line)
    cutter = ZiSegmenter(roots, prefixs, suffixs)
    for word in words:
        tokens = cutter.token_word(word)
        print(word, tokens)


def test_build(dir):
    freq_path = f"{dir}/word_frequency.tsv"
    if not os.path.exists(freq_path):
        logger.warning("no "+freq_path)
        return

    import logzero
    logzero.logfile(os.path.join(dir, "ZiTokenizerBuild.log"), mode='w')

    tokenizer = ZiTokenizer(dir)
    tokenizer.build(min_ratio=2e-6, min_freq=0)

    tokenizer = ZiTokenizer(dir)
    line = "'〇㎡[คุณจะจัดพิธีแต่งงานเมื่อไรคะัีิ์ื็ํึ]Ⅷpays-g[ran]d-blanc-élevé » (白高大夏國)😀熇'\x0000𧭏"
    tokens = tokenizer.tokenize(line)
    logger.info(' '.join(tokens))

    indexs = tokenizer.encode(line)
    words = tokenizer.decode(indexs)
    logger.info(' '.join(words))

    doc = os.popen(f" shuf {freq_path} -n 10").read().splitlines()
    doc = [x.split('\t') for x in doc]
    doc = [(k, int(v)) for k, v in doc]
    for k, v in doc:
        row = [k, v, tokenizer.cut(k)]
        logger.info((row))


def test_lang(lang):

    tokenizer = ZiTokenizer(lang=lang)

    line = "'〇㎡[คุณจะจัดพิธีแต่งงานเมื่อไรคะัีิ์ื็ํึ]Ⅷpays-g[ran]d-blanc-élevé » (白高大夏國)😀熇'\x0000𧭏"
    tokens = tokenizer.tokenize(line)
    logger.info(' '.join(tokens))

    indexs = tokenizer.encode(line)
    words = tokenizer.decode(indexs)
    logger.info(' '.join(words))


if __name__ == "__main__":
    test_segmenter()
    langs0 = ['ho', 'ff', 'aa', 'kj', 'kl', 'mh', 'xh', 'zh', 'ja',
              'th', 'ar', 'en', 'fr', 'ru',   'global'][:]
    langs = get_langs()
    langs = [x for x in langs if x not in langs0]
    langs = langs0

    for lang in langs[:3]:
        test_build(dir=f"C:/data/languages/{lang}")
        # test_lang(lang)

"""
[I 220705 23:16:13 demo:30] ' 〇 #sq ed [ ค ณ- จะ- จ ด- พ #th ng แ- ต ง- ง- า -น -เม อไ- ร -ค -ะ ] #sm ht pays - g [ ran ] d - blanc - eleve » ( 白 高 大 夏 國 ) #gr ce 
⿰ 火 高 ' 00 ⿰ 言 臺
[I 220705 23:16:13 demo:34] ' 〇 #sq ed [ ค ณจะจ ดพ #th ng แต งงานเม อไรคะ ] #sm ht pays - g [ ran ] d - blanc - eleve » ( 白 高 大 夏 國 ) #gr ce ⿰ 火 高 ' 00 ⿰ 言 臺

"""
