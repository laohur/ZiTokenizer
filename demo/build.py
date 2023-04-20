import collections
import os
import random
import multiprocessing

from logzero import logger

from ZiTokenizer.UnicodeTokenizer import UnicodeTokenizer
from ZiTokenizer.ZiSegmenter import ZiSegmenter
from ZiTokenizer.ZiCutter import ZiCutter
from ZiTokenizer.ZiTokenizer import ZiTokenizer

from unit import test_build, test_line, get_langs
from glance import load_frequency, describe


def test_coverage(tokenizer, freq_path, alpha=1):
    word_freq, total = load_frequency(freq_path, alpha=alpha)
    cover = 0
    for k, v in word_freq.items():
        tokens = tokenizer.token_word(k)
        if tokens[0][:2] != '##':
            cover += v
    cover /= total
    return total, cover


def test_share(param, max_split=3):
    langs, folder, alpha = param
    import logzero
    logzero.logfile(f"{folder}/common_vocabs_split{max_split}.log", mode='w')
    from logzero import logger
    global_tokenizer = ZiTokenizer(folder, max_split=max_split)
    global_vocab = set(global_tokenizer.vocab)

    keys = ['lang', 'vocab', 'total', 'common', 'share', 'cover']
    row = '\t'.join(keys)
    logger.info(row)

    counter = {k: 0 for k in keys}
    result = []
    for (lang, freq_path) in langs:
        total, cover = test_coverage(global_tokenizer, freq_path, alpha=alpha)
        local_vocab = open(f"languages/{lang}/vocab.txt").read().splitlines()
        common = global_vocab & set(local_vocab)
        j = {
            "lang": lang,
            "vocab": len(local_vocab),
            "total": total,
            "common": len(common),
            "share": len(common)/len(local_vocab),
            "cover": cover
        }
        row = '\t'.join(str(j[k]) for k in keys)
        logger.info(row)
        result.append(j)
        for k in keys[1:]:
            counter[k] += j[k]
    # result.sort(key=lambda x: x['lang'])
    for k in keys[1:]:
        counter[k] /= len(langs)
    counter['lang'] = 'average'
    row = '\t'.join(str(counter[k]) for k in keys)
    logger.info(row)
    result.append(counter)

    doc = ['\t'.join(keys)]
    doc += ['\t'.join(str(r[k]) for k in keys) for r in result]
    logger.info('\n\n\n'+'\n'.join(doc))
    return param, counter


def local_coverage(langs):
    import logzero
    logzero.logfile(f"coverage_local.log", mode='w')

    keys = ['lang', 'vocab', 'total', 'common', 'share', 'cover']
    counter = {k: 0 for k in keys}
    result = []
    for (lang, freq_path) in langs:
        folder = f"./languages/{lang}"
        tokenizer = ZiTokenizer(folder, max_split=3)
        total, cover = test_coverage(tokenizer, freq_path)
        local_vocab = tokenizer.vocab
        j = {
            "lang": lang,
            "vocab": len(local_vocab),
            "total": total,
            "common": len(local_vocab),
            "share": len(local_vocab)/len(local_vocab),
            "cover": cover
        }
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


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--local", type=int, default=0)
    args = parser.parse_args()

    langs = get_langs()

    if args.local == 1:
        for (lang, freq_path) in langs:
            folder = f"languages/{lang}"
            tokenizer = test_build(freq_path, folder)
            test_line(tokenizer)
        local_coverage(langs)
    if args.local == 0:
        params = []
        for alpha in [50, 60, 70, 80, 90]:
            freq_path = f"C:/data/languages/*/word_frequency.tsv"
            folder = f"languages/global-{alpha}"
            if not os.path.exists(folder):
                os.makedirs(folder)
            test_build(freq_path, folder, alpha=alpha/100)
            params.append((langs, folder, alpha/100))
        import multiprocessing
        with multiprocessing.Pool() as pool:
            R = pool.imap_unordered(test_share, params)
            for r in R:
                print(r)

"""

"""
