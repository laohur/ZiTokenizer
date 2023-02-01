import collections
import os
import unicodedata

from logzero import logger

from UnicodeTokenizer import UnicodeTokenizer
from ZiTokenizer.ZiSegmenter import ZiSegmenter
from ZiTokenizer.ZiTokenizer import ZiTokenizer
from ZiTokenizer.glance import load_frequency


def test_segmenter():
    line = "'〇㎡[คุณจะจัดพิธีแต่งงานเมื่อไรคะัีิ์ื็ํึ]Ⅷpays-g[ran]d-blanc-élevé » (白高大夏國)😀'\x0000熵"
    roots = ['la', 'a', 'ay', 'le']
    prefixs = ['e', 'l']
    suffixs = ['n', 'e', 'v']
    words = UnicodeTokenizer().tokenize(line)
    cutter = ZiSegmenter(roots, prefixs, suffixs)
    for word in words:
        tokens = cutter.token_word(word)
        print(word, tokens)


def test_build(dir):
    from logzero import logger
    freq_path = f"{dir}/word_frequency.tsv"
    if not os.path.exists(freq_path):
        logger.warning("no "+freq_path)
        return

    import logzero
    logzero.logfile(os.path.join(dir, "ZiTokenizerBuild.log"), mode='w')

    tokenizer = ZiTokenizer(dir)
    tokenizer.build(min_ratio=1.5e-6, min_freq=3)

    doc = os.popen(f" shuf {freq_path} -n 10").read().splitlines()
    doc = [x.split('\t') for x in doc]
    doc = [(k, int(v)) for k, v in doc]
    for k, v in doc:
        row = [k, v, tokenizer.token_word(k)]
        logger.info((row))


def test_lang(lang=None, dir=None):
    if dir:
        tokenizer = ZiTokenizer(dir=dir)
    else:
        tokenizer = ZiTokenizer(lang=lang)

    line = "'〇㎡[คุณจะจัดพิธีแต่งงานเมื่อไรคะัีิ์ื็ํึ]Ⅷpays-g[ran]d-blanc-élevé » (白高大夏國)熵😀'\x0000熇"
    tokens = tokenizer.tokenize(line)
    logger.info(' '.join(tokens))

    indexs = tokenizer.encode(line)
    words = tokenizer.decode(indexs)
    logger.info(' '.join(words))


def is_cover(word, tokenizer):
    [heads, root, tails] = tokenizer.ziSegmenter.token_word(word)
    if not root:
        return False
    for x in heads:
        if x not in tokenizer.ziSegmenter.prefixs:
            return False
    for x in tails:
        if x not in tokenizer.ziSegmenter.suffixs:
            return False
    return True


def common_vocabs(lang, global_tokenizer) -> str:
    dir = f"C:/data/languages/{lang}"
    freq_path = f"{dir}/vocab.txt"
    if not os.path.exists(freq_path):
        return ''
    vocab = open(freq_path).read().splitlines()
    vocab = set(vocab)
    global_vocab = set(global_tokenizer.vocab)
    common = global_vocab & vocab
    freq_path = f"{dir}/word_frequency.tsv"
    word_freq = load_frequency(freq_path)

    total = 0
    cover = 0
    for k, v in word_freq:
        # if len(k) == 1 and unicodedata.category(k[0])[0] not in 'LN':
        #     continue
        total += v
        if is_cover(k, global_tokenizer):
            cover += v
    j = {"lang": lang, "vocab": len(vocab), "total": total, "common": len(
        common), "share": len(common)/len(vocab), "cover": cover/total}
    line = '\t'.join(f"{k}:{v}" for k, v in j.items())
    logger.info(line)
    return j


def test_share(langs, folder="C:/data/languages/global", local=False,max_split=1):
    test_build(folder)
    import logzero
    if local:
        folder='.'
    logzero.logfile(f"{folder}/common_vocabs_split{max_split}.log", mode='w')
    from logzero import logger
    if not local:
        global_tokenizer = ZiTokenizer(folder, max_split=max_split)

    keys = ['lang', 'vocab', 'total', 'common', 'share', 'cover']
    counter = {k: 0 for k in keys}
    result = []
    for lang in langs:
        if local:
            global_tokenizer = ZiTokenizer(
                f"C:/data/languages/{lang}", max_split=max_split)

        j = common_vocabs(lang, global_tokenizer)
        result.append(j)
        for k in keys[1:]:
            counter[k] += j[k]
    for k in keys[1:]:
        counter[k] /= len(langs)
    counter['lang'] = 'average'
    result.append(counter)

    doc = ['\t'.join(keys)]
    doc += ['\t'.join(str(r[k]) for k in keys) for r in result]
    logger.info('\n\n\n'+'\n'.join(doc))


def demo(lang="global"):
    tokenizer = ZiTokenizer(lang=lang)
    line = "'〇㎡[คุณจะจัดพิธีแต่งงานเมื่อไรคะัีิ์ื็ํึ]Ⅷpays-g[ran]d-blanc-élevé » (白高大夏國)😀熇'\x0000𧭏２０１９"
    tokens = tokenizer.tokenize(line)
    print(tokens)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--alpha", type=int, default=50)
    args = parser.parse_args()
    # test_segmenter()
    # tokenizer = ZiTokenizer(lang='global')
    # re = tokenizer.token_word("3882253")
    # demo()
    langs = os.listdir("C:/data/languages")  # 344
    langs = [x for x in langs if 'global' not in x]

    # langs=['ar','en','fr','ja','ru','zh','th','ur','zu','global']
    # langs = ['global']
    # langs=[]

    for lang in langs:
        dir = f"C:/data/languages/{lang}"
        if not os.path.exists(dir):
            continue
        if not os.path.isdir(dir):
            continue
        # test_build(dir)
        # test_lang(dir=dir)
        test_lang(lang)

    # test_share(langs, local=True,max_split=1)
    # for alpha in [25, 50, 75]:
    # for alpha in [60,70,80,90]:
    #     test_share(langs, f"C:/data/languages/global-{alpha}", max_split=1)

"""

"""
