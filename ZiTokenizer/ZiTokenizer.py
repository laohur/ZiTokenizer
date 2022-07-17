
import unicodedata
import collections
import os
import math
import random
import bisect

from logzero import logger

from UnicodeTokenizer import UnicodeTokenizer
from ZiCutter import ZiCutter
from ZiTokenizer.glance import load_frequency, describe, show
from ZiTokenizer.trie import Trie
from ZiTokenizer import ZiSegmenter


class ZiTokenizer:
    max_split = 3
    dir = ''
    lang = ''
    vocab_path = ''
    never_split = set()
    vocab = []
    unicodeTokenizer = None
    ziCutter = None
    ziSegmenter = None
    token2index = []

    def __init__(self, dir="", lang="global", max_split=3, never_split=[]) -> None:
        self.max_split = max_split
        self.dir = dir
        self.lang = lang
        if not dir:
            here = os.path.dirname(__file__)
            self.dir = os.path.join(here, f"languages/{lang}")
        self.vocab_path = f"{self.dir}/vocab.txt"
        self.never_split = set(x for x in never_split)

        self.token2index = collections.OrderedDict()
        self.load()

    def load(self):
        root_words = []
        prefixs = []
        suffixs = []
        if os.path.exists(self.vocab_path):
            vocab = open(self.vocab_path).read().splitlines()
            for x in vocab:
                if len(x) > 1:
                    if x[:2] == '--':
                        suffixs.append(x[2:])
                        continue
                    if x[-2:] == '--':
                        prefixs.append(x[:-2])
                        continue
                root_words.append(x)
            logger.info(
                f" {self.vocab_path} load vocab:{len(vocab)} root:{len(root_words)} prefix:{len(prefixs)} suffix:{len(suffixs)} ")
        else:
            root_words = list(self.never_split | ZiCutter.ZiCutter().vocab)
            prefixs = [x+'--' for x in ZiCutter.Alphabet]
            suffixs = ['--'+x for x in ZiCutter.Alphabet]
            vocab = sorted(root_words)+sorted(prefixs)+sorted(suffixs)
            logger.error(
                f"no {self.vocab_path}, default vocab:{len(vocab)} root:{len(root_words)} prefix:{len(prefixs)} suffix:{len(suffixs)} ")
        self.vocab = vocab
        for i, x in enumerate(vocab):
            self.token2index[x] = i

        root_words = set(root_words)
        prefixs = set(prefixs)
        suffixs = set(suffixs)

        never_split = self.never_split | root_words
        self.unicodeTokenizer = UnicodeTokenizer.UnicodeTokenizer(
            never_split=never_split)
        self.ziCutter = ZiCutter.ZiCutter(self.dir)
        self.ziSegmenter = ZiSegmenter.ZiSegmenter(
            root_words=root_words, prefixs=prefixs, suffixs=suffixs, max_split=self.max_split)

        # build local for languages
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        HeZiPath = os.path.join(self.dir, "HeZi.txt")
        if not os.path.exists(HeZiPath):
            logger.warning(f" {HeZiPath} not exist, building ZiCutter... ")
            self.ziCutter.build(roots=root_words)

    def token_word(self, word):
        [heads, root, tails] = self.ziSegmenter.token_word(word)
        if not root:
            chars = []
            for x in word[:self.max_split*2]:
                t = self.ziCutter.cutChar(x)
                chars += t
            return chars
        for i in range(len(heads)):
            heads[i] += '--'
        for i in range(len(tails)):
            tails[i] = '--' + tails[i]
        tokens = heads+[root]+tails
        return tokens

    def build(self, min_ratio=2e-6, min_freq=0):
        p = f"{self.dir}/word_frequency.tsv"
        if not os.path.exists(p):
            logger.warning(f" no {p}")
            return
        logger.warning(f" building from {p}")
        word_freq = load_frequency(p)
        if not word_freq:
            logger.error(f"no word_freq")
            return
        cover_pos_ration, total, word_len = describe(word_freq, min_ratio)
        show(cover_pos_ration, total, word_len)
        conver_half = cover_pos_ration[6]
        logger.info(f"conver_half {conver_half}")
        min_ratio = min(min_ratio, conver_half[-2])
        if conver_half[2][1] >= 2:
            min_freq = max(min_freq, 2)
        bottom = max(min_freq, (total*min_ratio))
        logger.info(
            f"min_ratio:{min_ratio} min_freq:{min_freq} bottom:{bottom:.2f}")

        char_counter = collections.Counter()
        for i in range(len(word_freq)):
            k, v = word_freq[i]
            for x in k:
                char_counter[x] += v
        hot = [k for k, v in word_freq if v >= bottom]
        chars = [k for k, v in char_counter.items() if v > bottom/5]
        root_words = set(hot) | set(chars)
        logger.info(
            f" words:{len(word_freq)} chars:{len(char_counter)} hot:{len(hot)} root_words:{len(root_words)}")

        self.ziCutter.build(roots=root_words)
        root_words |= self.ziCutter.vocab
        root_words |= self.never_split
        self.ziSegmenter = ZiSegmenter.ZiSegmenter(root_words=root_words)

        logger.info("  === token_root ===  ")
        sample = random.choices(word_freq, k=5)
        for k, v in sample:
            [prefix, root, suffix] = self.ziSegmenter.token_root(k)
            row = [k, v, prefix, root, suffix]
            logger.info((row))

        prefix_counter = collections.Counter()
        suffix_counter = collections.Counter()
        # ignore rare words and decline bottom may save time
        for k, v in word_freq:
            if k in root_words:
                continue
            [prefix, root, suffix] = self.ziSegmenter.token_root(k)
            if not root:
                continue
            if prefix:
                prefix_counter[prefix] += v
            if suffix:
                suffix_counter[suffix] += v
        del word_freq
        prefixs = [k for k, v in prefix_counter.items() if v >= bottom] + \
            list(ZiCutter.Nums)
        del prefix_counter
        suffixs = [k for k, v in suffix_counter.items() if v >= bottom] + \
            list(ZiCutter.Nums)
        del suffix_counter
        logger.info(f"prefixs:{len(prefixs)} suffixs:{len(suffixs)}")

        prefixs = [x+'--' for x in prefixs]
        root_words = [x for x in root_words]
        suffixs = ['--'+x for x in suffixs]
        vocab = sorted(root_words)+sorted(prefixs)+sorted(suffixs)
        with open(self.vocab_path, 'w') as f:
            for x in vocab:
                f.write(x+'\n')
        logger.info(f"save  vocab { len(vocab) }  -->{self.vocab_path} ")
        self.load()

    def tokenize(self, line):
        words = self.unicodeTokenizer.tokenize(line)
        tokens = []
        for word in words:
            if not word:
                continue
            if word in self.token2index:
                tokens.append(word)
            else:
                cuts = self.token_word(word)
                tokens += cuts
        tokens = [x for x in tokens if x]
        return tokens

    def tokens2indexs(self, tokens):
        idxs = [self.token2index[x] for x in tokens]
        return idxs

    def indexs2tokens(self, indexs):
        indexs = [self.vocab[x] for x in indexs]
        return indexs

    def encode(self, line):
        tokens = self.tokenize(line)
        indexs = self.tokens2indexs(tokens)
        return indexs

    def tokens2words(self, tokens):
        ts = tokens[:1]
        for i in range(1, len(tokens)):
            x = tokens[i]
            if len(ts[-1]) > 1 and ts[-1][-2:] == '--':  # prefix
                ts[-1] = ts[-1][:-2]+x
                continue
            if len(x) > 1 and x[:2] == '--':  # suffix
                ts[-1] += x[1:]
                continue
            ts.append(x)
        return ts

    def decode(self, indexs):
        tokens = self.indexs2tokens(indexs)
        words = self.tokens2words(tokens)
        return words
