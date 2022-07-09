
import unicodedata
import collections
import os
import math
import random

from logzero import logger

from UnicodeTokenizer.UnicodeTokenizer import UnicodeTokenizer
from ZiCutter.ZiCutter import ZiCutter
from ZiTokenizer.glance import load_frequency, describe, show
from ZiTokenizer.trie import Trie
from ZiTokenizer.ZiSegmenter import ZiSegmenter


class ZiTokenizer:
    def __init__(self, dir="", lang="", max_split=3, never_split=set(["[UNK]", "[SEP]", "[PAD]", "[CLS]", "[MASK]"])) -> None:
        self.max_split = max_split
        self.dir = dir
        self.lang = lang
        if not dir:
            here = os.path.dirname(__file__)
            self.dir = os.path.join(here, f"languages/{lang}")
        self.vocab_path = f"{self.dir}/vocab.txt"
        self.never_split = set(x for x in never_split)
        self.UnicodeTokenizer = UnicodeTokenizer(never_split=never_split)
        self.ZiCutter = ZiCutter(self.dir)
        self.vocab = []
        self.ZiSegmenter = ZiSegmenter(self.vocab)
        self.token2index = collections.OrderedDict()
        self.load()

    def load(self):
        root_words = set()
        prefixs = set()
        suffixs = set()
        if os.path.exists(self.vocab_path):
            vocab = open(self.vocab_path).read().splitlines()
        else:
            logger.error(
                f" no {self.vocab_path} ! use minium vocab; try ZiTokenizer(lang='global')")
            vocab = list(self.never_split | self.ZiCutter.vocab)
        self.vocab = vocab
        for i, x in enumerate(vocab):
            self.token2index[x] = i
        for x in vocab:
            if len(x) > 1:
                if x[:2] == '--':
                    suffixs.add(x[2:])
                    continue
                elif x[-2:] == '--':
                    prefixs.add(x[:-2])
                    continue
            root_words.add(x)
        self.never_split |= root_words
        self.UnicodeTokenizer = UnicodeTokenizer(never_split=self.never_split)
        self.ZiSegmenter = ZiSegmenter(root_words)
        # if not os.path.exists(self.dir):
        #     os.makedirs(self.dir)
        # HeZiPath = os.path.join(self.dir, "HeZi.txt")
        # if not os.path.exists(HeZiPath):
        #     logger.warning(f" {HeZiPath} not exist, building ZiCutter... ")
        #     self.ZiCutter.build(roots=root_words)

        logger.info(
            f" {self.vocab_path} load vocab:{len(vocab)}  root:{len(root_words)} prefix:{len(prefixs)} suffix:{len(suffixs)} ")

    def token_word(self, word):
        [heads, root, tails] = self.ZiSegmenter.token_word(word)
        if not root:
            chars = []
            for x in word[:self.max_split]:
                t = self.ZiCutter.cutChar(x)
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
        word_freq = load_frequency(p)
        cover_pos_ration, total, word_len = describe(word_freq, min_ratio)
        show(cover_pos_ration, total, word_len)
        k, v = cover_pos_ration[7][2]
        if v >= 2:
            min_freq = max(min_freq, 2)
        bottom = max(min_freq, (total*min_ratio))

        # root
        root_words = set([k for k, v in word_freq if v >= bottom])
        logger.info(
            f"min_ratio:{min_ratio} min_freq:{min_freq} bottom:{bottom:.2f} root_words:{len(root_words)}")

        self.ZiCutter.build(roots=root_words)
        root_words |= self.ZiCutter.vocab
        root_words |= self.never_split

        logger.info("  === token_root ===  ")
        sample = random.choices(word_freq, k=5)
        for k, v in sample:
            [prefix, root, suffix] = self.ZiSegmenter.token_root(k)
            row = [k, v, prefix, root, suffix]
            logger.info((row))

        # prefix,suffix
        prefix_counter = collections.Counter()
        suffix_counter = collections.Counter()
        for k, v in word_freq:
            if k in root_words:
                continue
            [prefix, root, suffix] = self.ZiSegmenter.token_root(k)
            if not root:
                continue
            if prefix:
                prefix_counter[prefix] += v
            if suffix:
                suffix_counter[suffix] += v
        del word_freq
        prefixs = [k for k, v in prefix_counter.items() if v >= bottom]
        del prefix_counter
        suffixs = [k for k, v in suffix_counter.items() if v >= bottom]
        del suffix_counter
        logger.info(f"prefixs:{len(prefixs)} suffixs:{len(suffixs)}")

        prefixs = [x+'--' for x in prefixs]
        root_words = [x for x in root_words]
        suffixs = ['--'+x for x in suffixs]
        vocab = sorted(prefixs)+sorted(root_words)+sorted(suffixs)
        with open(self.vocab_path, 'w') as f:
            for x in vocab:
                f.write(x+'\n')
        logger.info(f"save  vocab { len(vocab) }  -->{self.vocab_path} ")
        self.load()

    def tokenize(self, line):
        words = self.UnicodeTokenizer.tokenize(line)
        tokens = []
        for word in words:
            if not word:
                continue
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
