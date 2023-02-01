
from collections import Counter
import os
import logzero
from logzero import logger


def load_frequency(p, do_lower_case=True, remove_blank=True, tgt=''):
    freq = Counter()
    n_src = 0
    if '/' in p.strip().split()[0]:
        p = 'cat '+p
    for l in os.popen(p):
        n_src += 1
        k, v = l.split('\t ')
        if len(k) > 50:
            continue
        if do_lower_case:
            k = k.lower()
        if remove_blank:
            k = k.strip()
        if not k:
            continue
        freq[k] += int(v)
    # words = [(k, v) for k, v in freq.items() if v > 1]
    words = list(freq.items())
    logger.info(f" {p} n_src:{n_src}--> freq:{len(freq)}")
    del freq
    words.sort(key=lambda x: (-x[1], len(x[0]), x[0]))
    if tgt:
        with open(tgt, "w") as f:
            for k, v in words:
                f.write(f"{k}\t {v}"+'\n')
        line = f" word_counter:{len(words)} --> {tgt}  "
        logger.info(line)
    return words


def describe(doc):
    total = sum(x[1] for x in doc)
    word_len0 = sum(len(a) for a, b in doc)/total
    word_len = sum(len(a)*b for a, b in doc)/total
    logger.info((f"total:{total} word_len0:{word_len0} word_len:{word_len}"))

    idxs = [1000*i for i in range(1, 101)]
    covered = 0
    rows = ['']
    l = '\t'.join("pos,word,frequency,ratio,covered".split(','))
    rows.append(l)
    for i, (k, v) in enumerate(doc):
        ratio = v/total
        covered += ratio
        row = (i+1, k, v, ratio, covered)
        l = '\t'.join(str(x) for x in row)
        if i+1 in idxs:
            rows.append(l)
        if i>=1e5:
            break
    logger.info('\n'.join(rows))
    return total



if __name__ == "__main__":
    import logzero

    logzero.logfile(__file__+".log", mode="w")

    langs = ['aa', 'ar', 'en', 'fr', 'ja', 'ru', 'zh', 'th', 'sw', 'ur']
    for lang in langs:
        path = f"C:/data/lang/{lang}/word_frequency.tsv"
        doc = load_frequency(path)
        summary = describe(doc)

"""

"""
