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
    logzero.logfile(os.path.join(dir, "ZiTokenizerBuild.log"), mode='w')

    tokenizer = ZiTokenizer(dir)
    # tokenizer.build(min_ratio=1.5e-6, min_freq=0)
    tokenizer.build(min_ratio=2e-6, min_freq=0)

    tokenizer = ZiTokenizer(dir)
    line = "'〇㎡[คุณจะจัดพิธีแต่งงานเมื่อไรคะัีิ์ื็ํึ]Ⅷpays-g[ran]d-blanc-élevé » (白高大夏國)😀熇'\x0000𧭏"
    tokens = tokenizer.tokenize(line)
    logger.info(tokens)

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

    langs = ['aa', 'sr', 'om', 'tk', 'xh', 'zh', 'ja', 'th', 'ar', 'en', 'fr',
             'ru',   'global'][-1:]
    langs = get_langs()

    for lang in langs:
        dir = f"C:/data/languages/{lang}"
        test_lang(dir)

    """
    构建：按照频率选入词根，其次前缀后缀
    切字：词根最长匹配，其次前缀后缀最长匹配

"""
