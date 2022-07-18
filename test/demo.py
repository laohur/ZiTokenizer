import os
import unicodedata

from logzero import logger

from UnicodeTokenizer.UnicodeTokenizer import UnicodeTokenizer
from ZiTokenizer.ZiSegmenter import ZiSegmenter
from ZiTokenizer.ZiTokenizer import ZiTokenizer
from ZiTokenizer.glance import load_frequency


def get_langs():
    alphabet = ''.join(chr(x) for x in range(ord('a'), ord('z')+1))
    langs = [x+y for x in alphabet for y in alphabet]
    return langs


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

    tokenizer = ZiTokenizer(dir, max_split=3, never_split=[
                            "[UNK]", "[SEP]", "[PAD]", "[CLS]", "[MASK]"])
    tokenizer.build(min_ratio=2e-6, min_freq=0)

    doc = os.popen(f" shuf {freq_path} -n 10").read().splitlines()
    doc = [x.split('\t') for x in doc]
    doc = [(k, int(v)) for k, v in doc]
    for k, v in doc:
        row = [k, v, tokenizer.token_word(k)]
        logger.info((row))


def test_lang(lang):

    tokenizer = ZiTokenizer(lang=lang)

    line = "'〇㎡[คุณจะจัดพิธีแต่งงานเมื่อไรคะัีิ์ื็ํึ]Ⅷpays-g[ran]d-blanc-élevé » (白高大夏國)熵😀'\x0000熇"
    tokens = tokenizer.tokenize(line)
    logger.info(' '.join(tokens))

    indexs = tokenizer.encode(line)
    words = tokenizer.decode(indexs)
    logger.info(' '.join(words))


def is_cover(word, ziSegmenter, heads, root, tails):
    if not root:
        return 0
    l = len(root)
    for x in heads:
        if x in ziSegmenter.prefixs:
            l += len(x)
    for x in tails:
        if x in ziSegmenter.suffixs:
            l += len(x)
    return l == len(word)


def common_vocabs(lang, global_vocab, global_tokenizer):
    dir = f"C:/data/languages/{lang}"
    freq_path = f"{dir}/vocab.txt"
    if not os.path.exists(freq_path):
        return
    vocab = open(freq_path).read().splitlines()
    vocab = set(vocab)
    common = global_vocab & vocab
    freq_path = f"{dir}/word_frequency.tsv"
    word_freq = load_frequency(freq_path)

    total = 0
    cover = 0
    for k, v in word_freq:
        if len(k) == 1 and unicodedata.category(k[0])[0] not in 'LN':
            continue
        total += v
        [heads, root, tails] = global_tokenizer.ziSegmenter.token_word(k)
        if is_cover(k, global_tokenizer.ziSegmenter, heads, root, tails):
            cover += v
    logger.info(
        f" {lang} vocab:{len(vocab)}  common:{len(common )} share:{len(common)/len(vocab)} cover:{cover/total} ")


if __name__ == "__main__":
    # test_segmenter()
    # tokenizer = ZiTokenizer(lang='global')
    # re = tokenizer.token_word("3882253")

    langs0 = ['ho', 'ff', 'aa', 'kj', 'kl', 'mh', 'xh', 'zh', 'ja',
              'th', 'ar', 'en', 'fr', 'ru',   'global'][:]
    langs = get_langs()
    # langs = [x for x in langs if x not in langs0]
    langs = ['global']+langs
    langs = ['bn']

    # import logzero
    # logzero.logfile("common_vocabs.log", mode='w')
    # global_tokenizer = ZiTokenizer("C:/data/languages/global", max_split=1)
    # global_vocab = set(global_tokenizer.vocab)

    for lang in langs:
        test_build(dir=f"C:/data/languages/{lang}")
        # test_lang(lang)
        # break
        # common_vocabs(lang, global_vocab, global_tokenizer)

"""
[I 220718 00:19:43 ZiTokenizer:58]  C:/data/languages/global/vocab.txt load vocab:116710 root:77271 prefix:23034 suffix:16405
[I 220718 00:19:45 ZiCutter:98] C:/data/languages/global\JiZi.txt load  JiZi:9572
[I 220718 00:19:45 ZiCutter:49]   C:/data/languages/global\HeZi.txt JiZi:9572 --> loadHeZi 93812  values:9572
[I 220718 00:19:45 ZiCutter:103] C:/data/languages/global\HeZi.txt HeZi:93812 values:9572
[I 220718 00:19:45 ZiCutter:106] C:/data/languages/global loaded vocab:10931
[I 220718 00:19:47 ZiTokenizer:58]  C:\ProgramData\Miniconda3\lib\site-packages\ZiTokenizer\languages/global/vocab.txt load vocab:116710 root:77271 prefix:23034 suffix:16405
[I 220718 00:19:49 ZiCutter:98] C:\ProgramData\Miniconda3\lib\site-packages\ZiTokenizer\languages/global\JiZi.txt load  JiZi:9572
[I 220718 00:19:49 ZiCutter:49]   C:\ProgramData\Miniconda3\lib\site-packages\ZiTokenizer\languages/global\HeZi.txt JiZi:9572 --> loadHeZi 93812  values:9572
[I 220718 00:19:49 ZiCutter:103] C:\ProgramData\Miniconda3\lib\site-packages\ZiTokenizer\languages/global\HeZi.txt HeZi:93812 values:9572
[I 220718 00:19:49 ZiCutter:106] C:\ProgramData\Miniconda3\lib\site-packages\ZiTokenizer\languages/global loaded vocab:10931
[I 220718 00:19:51 demo:58] ' 〇 ㎡ [ ค ณ-- จ-- ะ --จ ด-- พ ธ แต ง-- งา-- นเม อไ-- ร --ค --ะ ] ##s ht pays - g [ ran ] d - blanc - eleve » ( 白 高 大 夏 國 ) ⿰ 火 商 ##g ce ' 00 ⿰ 火 高
[I 220718 00:19:51 demo:62] ' 〇 ㎡ [ ค ณจะ-จ ดพ ธ แต งงานเม อไร-ค-ะ ] ##s ht pays - g [ ran ] d - blanc - eleve » ( 白 高 大 夏 國 ) ⿰ 火 商 ##g ce ' 00 ⿰ 火 高

"""
