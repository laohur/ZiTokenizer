
import unicodedata
import collections
import os
import math
import random

from logzero import logger

from ZiTokenizer.trie import Trie


class ZiSegmenter:
    def __init__(self, root_words, prefixs=set(), suffixs=set(),max_split=20):
        self.max_split = max_split
        self.root_words = set(x for x in root_words)
        self.prefixs = set(x for x in prefixs)
        self.suffixs = set(x for x in suffixs)
        self.rootAC = Trie().create_trie_from_list(self.root_words)

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
            return [word, None, None]

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

    def token_word(self, word):
        [prefix, root, suffix] = self.token_root(word)
        if not root:
            return [prefix, root, suffix]
        heads = []
        tails = []
        if prefix:
            heads = self.token_prefix(prefix)
        if suffix:
            tails = self.token_suffix(suffix)
        return [heads, root, tails]

