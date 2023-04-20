
from collections import Counter
import math
import os
import logzero
from logzero import logger


def load_frequency(src, alpha=1, do_lower_case=True, length_hat=50, min_freq=1):
    freq = Counter()
    n_src = 0
    if ' ' not in src:
        src = 'cat '+src
    total = 0
    for l in os.popen(src):
        n_src += 1
        k, v = l.split('\t ')
        if len(k) > length_hat:
            continue
        if not k or len(k) == 0:
            continue
        v = math.pow(int(v), alpha)
        if v < min_freq:
            continue
        if do_lower_case:
            k = k.lower()
        freq[k] += v
        total += v
    logger.info(f" {src} n_src:{n_src}--> freq:{len(freq)} total:{total}")
    return freq, total


def describe(doc, total):
    idxs = [2**i for i in range(100)]
    covered = 0
    rows = ['']
    l = '\t'.join("pos,word,frequency,ratio,covered".split(','))
    rows.append(l)
    for i, (k, v) in enumerate(doc):
        I = i+1
        ratio = v/total
        covered += ratio
        if I in idxs or I == len(doc):
            row = (I, k, v, ratio, covered)
            l = '\t'.join(str(x) for x in row)
            rows.append(l)
    logger.info('\n'.join(rows))


if __name__ == "__main__":

    path = f"./demo/word_frequency.tsv"
    word_freq, total = load_frequency(path)
    summary = describe(word_freq, total)

"""

"""
