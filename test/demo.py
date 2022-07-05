import os

from logzero import logger

from ZiTokenizer.ZiTokenizer import ZiTokenizer


def get_langs():
    alphabet = ''.join(chr(x) for x in range(ord('a'), ord('z')+1))
    langs = [x+y for x in alphabet for y in alphabet]
    return langs


def test_lang(dir):
    freq_path = f"C:/data/languages/{lang}/word_frequency.tsv"
    if not os.path.exists(freq_path):
        return

    import logzero
    from logzero import logger
    # logzero.logfile(os.path.join(dir, "ZiTokenizerBuild.log"), mode='w')

    # tokenizer = ZiTokenizer(dir)
    # tokenizer.build(min_ratio=1.5e-6, min_freq=0)
    # tokenizer.build(min_ratio=2e-6, min_freq=0)

    tokenizer = ZiTokenizer(dir)
    line = "'〇㎡[คุณจะจัดพิธีแต่งงานเมื่อไรคะัีิ์ื็ํึ]Ⅷpays-g[ran]d-blanc-élevé » (白高大夏國)😀熇'\x0000𧭏"
    tokens = tokenizer.tokenize(line)
    logger.info(' '.join(tokens))

    indexs = tokenizer.encode(line)
    words = tokenizer.decode(indexs)
    logger.info(' '.join(words))

    # from ZiTokenizer.glance import load_frequency
    # shuf C:/data/languages/en/word_frequency.tsv | head -n 10
    doc = os.popen(f" shuf {freq_path} -n 10").read().splitlines()
    doc = [x.split('\t') for x in doc]
    doc = [(k, int(v)) for k, v in doc]
    for k, v in doc:
        row = [k, v, tokenizer.cut(k)]
        logger.info((row))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', default="global",  type=str)
    args = parser.parse_args()

    lang = args.lang

    langs = ['aa', 'sr', 'om', 'tk', 'xh', 'zh', 'ja', 'th', 'ar', 'en', 'fr','ru',   'global'][:]
    # langs = get_langs()

    for lang in langs:
        dir = f"C:/data/languages/{lang}"
        test_lang(dir)

"""
[I 220705 23:16:13 demo:30] ' 〇 #sq ed [ ค ณ- จะ- จ ด- พ #th ng แ- ต ง- ง- า -น -เม อไ- ร -ค -ะ ] #sm ht pays - g [ ran ] d - blanc - eleve » ( 白 高 大 夏 國 ) #gr ce 
⿰ 火 高 ' 00 ⿰ 言 臺
[I 220705 23:16:13 demo:34] ' 〇 #sq ed [ ค ณจะจ ดพ #th ng แต งงานเม อไรคะ ] #sm ht pays - g [ ran ] d - blanc - eleve » ( 白 高 大 夏 國 ) #gr ce ⿰ 火 高 ' 00 ⿰ 言 臺

"""
