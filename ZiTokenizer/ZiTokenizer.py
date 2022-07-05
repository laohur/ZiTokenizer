
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


class ZiTokenizer:
    def __init__(self, dir, max_split=3, never_split=set(["[UNK]", "[SEP]", "[PAD]", "[CLS]", "[MASK]"])) -> None:
        self.max_split = max_split
        self.dir = dir
        self.vocab_path = f"{self.dir}/vocab.txt"
        self.ZiCutter = ZiCutter(dir)
        self.UnicodeTokenizer = UnicodeTokenizer()
        self.vocab = []
        self.never_split = never_split
        self.token2index = collections.OrderedDict()
        if os.path.exists(self.vocab_path):
            self.load()

    def load(self):
        self.root_words = set()
        self.prefixs = set()
        self.suffixs = set()
        vocab = open(self.vocab_path).read().splitlines()
        self.vocab = vocab
        for i, x in enumerate(vocab):
            self.token2index[x] = i
        for x in vocab:
            if len(x) > 1:
                if x[0] == '-':
                    self.suffixs.add(x[1:])
                    continue
                elif x[-1] == '-':
                    self.prefixs.add(x[:-1])
                    continue
            self.root_words.add(x)
        self.never_split|=self.root_words
        self.UnicodeTokenizer = UnicodeTokenizer(never_split=self.never_split)

        self.rootAC = Trie().create_trie_from_list(self.root_words)
        logger.info(
            f" {self.vocab_path} load vocab:{len(vocab)}  root:{len(self.root_words)} prefix:{len(self.prefixs)} suffix:{len(self.suffixs)} ")

    def token_root(self, word):
        matchs = self.rootAC.parse_text(word)
        if matchs:
            length = max(len(match.keyword) for match in matchs)
            matchs = [match for match in matchs if len(
                match.keyword) == length]
            longest_match = matchs[len(matchs)//2]
            root = longest_match.keyword
            prefix = word[:longest_match.start]
            suffix = word[longest_match.end:]
            return [prefix, root, suffix]
        else:
            chars = []
            for x in word[:self.max_split]:
                t = self.ZiCutter.cutChar(x)
                chars += t
            return [chars, None, None]

    def token_prefix(self, grams):
        tokens = []
        for i in range(self.max_split):
            if not grams:
                break
            for i in range(len(grams)):
                a = grams[:len(grams)-i]
                if a in self.prefixs:
                    tokens.append(a)
                    grams = grams[len(a):]
                    break
        return tokens

    def token_suffix(self, grams):
        tokens = []
        for i in range(self.max_split):
            if not grams:
                break
            for i in range(len(grams)):
                a = grams[i:]
                if a in self.suffixs:
                    tokens.insert(0, a)
                    grams = grams[:-len(a)]
                    break
        return tokens

    def token_all(self, word):
        [prefix, root, suffix] = self.token_root(word)
        if not root:
            return [prefix, root, suffix]
        heads = [prefix] if prefix else []
        tails = [suffix] if suffix else []
        if prefix:
            heads = self.token_prefix(prefix)
        if suffix:
            tails = self.token_suffix(suffix)
        return [heads, root, tails]

    def cut(self, word):
        [prefix, root, suffix] = self.token_all(word)
        if not root:
            return prefix
        heads = []
        tails = []
        if prefix:
            heads = [x+'-' for x in prefix]
        if suffix:
            tails = ['-'+x for x in suffix]
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
        pair = cover_pos_ration[5][2]
        if pair[1] >= 2:
            min_freq = max(min_freq, 2)
        botton = max(min_freq, int(total*min_ratio))

        # root
        root_words = set([k for k, v in word_freq if v > botton])
        self.ZiCutter.build(roots=root_words)
        root_words |= self.ZiCutter.vocab
        self.root_words = root_words
        logger.info(
            f"total:{total} min_ratio:{min_ratio} min_freq:{min_freq} botton:{botton} root_words:{len(root_words)}")

        rootAC = Trie().create_trie_from_list(root_words)
        self.rootAC = rootAC

        logger.info("  === token_root ===  ")
        sample = random.choices(word_freq, k=5)
        for k, v in sample:
            [prefix, root, suffix] = self.token_root(k,)
            row = [k, v, prefix, root, suffix]
            logger.info((row))

        # prefix,suffix
        prefix_counter = collections.Counter()
        suffix_counter = collections.Counter()
        for k, v in word_freq:
            if k in root_words:
                continue
            [prefix, root, suffix] = self.token_root(k)
            if not root:
                continue
            if prefix:
                prefix_counter[prefix] += v
            if suffix:
                suffix_counter[suffix] += v
        del word_freq
        prefixs = set(k for k, v in prefix_counter.items() if v >= botton)
        del prefix_counter
        logger.info(f"prefixs:{len(prefixs)}")
        suffixs = set(k for k, v in suffix_counter.items() if v >= botton)
        del suffix_counter
        logger.info(f"suffixs:{len(suffixs)}")
        self.prefixs = prefixs
        self.suffixs = suffixs
        self.save()

    def save(self):
        prefixs = [x+'-' for x in self.prefixs]
        root_words = [x for x in self.root_words]
        suffixs = ['-'+x for x in self.suffixs]
        vocab = []
        vocab += sorted(prefixs)
        vocab += sorted(root_words)
        vocab += sorted(suffixs)

        with open(self.vocab_path, 'w') as f:
            for x in vocab:
                f.write(x+'\n')
        logger.info(f"save  vocab { len(vocab) }  -->{self.vocab_path} ")

    def tokenize(self, line):
        words = self.UnicodeTokenizer.tokenize(line)
        tokens = []
        for word in words:
            if not word:
                continue
            cuts = self.cut(word)
            tokens += cuts
        tokens = [x for x in tokens if x]
        return tokens

    def tokens2indexs(self,tokens):
        idxs = [self.token2index[x] for x in tokens]
        return idxs

    def indexs2tokens(self,indexs):
        indexs = [self.vocab[x] for x in indexs]
        return indexs

    def encode(self,line):
        tokens=self.tokenize(line)
        indexs = self.tokens2indexs(tokens)
        return indexs

    def tokens2words(self,tokens):
        ts=tokens[:1]
        for i in range(1,len(tokens)):
            x=tokens[i]
            if len(ts[-1])>1 and ts[-1][-1]=='-':  # prefix
                ts[-1]=ts[-1][:-1]+x
                continue
            if len(x)>1 and x[0]=='-': # suffix
                ts[-1]+=x[1:]
                continue
            ts.append(x)
        return ts
    
    def decode(self,indexs):
        tokens=self.indexs2tokens(indexs)
        words=self.tokens2words(tokens)
        return words

def get_langs():
    alphabet = ''.join(chr(x) for x in range(ord('a'), ord('z')+1))
    langs = [x+y for x in alphabet for y in alphabet]
    return langs


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', default="global",  type=str)
    args = parser.parse_args()
    print(args)
    lang = args.lang

    langs = ['sw', 'ur', 'ar', 'en', 'fr', 'ja', 'ru', 'zh', 'th']
    # langs = get_langs()

    for lang in langs:
        # dir = f"C:/data/lang/{lang}"
        dir = f"C:/data/languages/{lang}"
        freq_path = f"C:/data/languages/{lang}/word_frequency.tsv"
        if not os.path.exists(freq_path):
            continue
        cutter = ZiTokenizer(dir)
        cutter.build(min_ratio=1.5e-6, min_freq=1)

        cutter = ZiTokenizer(dir)
        cutter.test(10)

"""

"""
