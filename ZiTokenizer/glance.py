
from collections import Counter
import os
import math
import bisect
import logzero
from logzero import logger


def load_frequency(p, max_len=20):
    doc = open(p).read().splitlines()
    for i in range(len(doc)):
        k, v = doc[i].split('\t')[:2]
        if len(k)>=20 or not k:
            continue
        doc[i] = (k, int(v))
    # doc = [x.split('\t') for x in doc]
    # doc = [(x[0], int(x[1])) for x in doc]
    # doc = [x for x in doc if x[1]!=1 or len(x[0])<20 ]
    logger.info(f" {p} load {len(doc)} words")
    return doc


def describe(doc, min_ratio=1.5e-6):
    total = sum(b for a, b in doc)
    word_len = sum(len(a)*b for a, b in doc)/total

    ratios = [b/total for a, b in doc]
    cover = ratios[:]
    for i in range(len(cover)):
        cover[i] += cover[i-1]

    cover_pos_ration = []
    pos = bisect.bisect_right(ratios[::-1], min_ratio)
    pos = len(doc)-1-pos
    ratio = ratios[pos]
    cover_pos_ration.append((-1, pos, doc[pos], ratio, cover[pos]))

    nums = [i/10 for i in range(10)]
    nums += [0.9+i/100 for i in range(1, 10)]
    for x in nums:
        pos = bisect.bisect_right(cover, x)
        pos = min(pos, len(doc)-1)
        ratio = ratios[pos]
        cover_pos_ration.append((x, pos, doc[pos], ratio, cover[pos]))

    return cover_pos_ration, total, word_len


def show(cover_pos_ration, total, word_len):
    logger.info((f"total:{total} word_len:{word_len}"))
    l = '\t'.join("x,pos,doc[pos],ratio,cover[pos]".split(','))
    logger.info(l)
    for row in cover_pos_ration:
        l = '\t'.join(str(x) for x in row)
        logger.info(l)


if __name__ == "__main__":
    import logzero
    from logzero import logger

    logzero.logfile(f"glance.log", mode="w")

    langs = ['aa', 'ar', 'en', 'fr', 'ja', 'ru', 'zh', 'th', 'sw', 'ur']
    for lang in langs:
        path = f"C:/data/lang/{lang}/word_frequency.tsv"
        doc = load_frequency(path)
        summary = describe(doc)
        show(summary)
        # for i, x in enumerate(summary):
        # logger.info((i, x))

"""

"""
