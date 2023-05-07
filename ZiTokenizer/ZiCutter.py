# -*- coding: utf-8 -*-
import os

from logzero import logger

from ZiTokenizer import He2Zi
from ZiTokenizer.He2Zi import JieGou, GouJian


def slim(v):
    if len(v) <= 3:
        return v
    for i in range(1, len(v)-1):
        if v[i] not in JieGou:
            w = v[0]+v[i]+v[-1]
            return w
    assert len(v) == 3
    return v


def loadHeZi(path, JiZi, max_len=50):
    doc = open(path).read().splitlines()
    doc = [x.split('\t') for x in doc]
    doc = [(k, v) for k, v in doc if 0 < len(v) <= max_len and not set(v) - JiZi]
    HeZi = {k: v for k, v in doc}
    slim2Zi = {v: k for k, v in HeZi.items()}
    values = ''.join(HeZi.values())
    values = list(set(values))
    values.sort()
    jieGou = ''.join(set([x[0] for x in slim2Zi]))
    max_len = max(len(x) for x in slim2Zi)
    logger.info(
        f"  {path} {len(doc)}  JiZi:{len(JiZi)} --> loadHeZi {len(HeZi)}  values:{len(values)} slim2Zi:{len(slim2Zi)} jieGou:{jieGou} max_len:{max_len}")
    return HeZi, values, slim2Zi, jieGou, max_len


class ZiCutter:
    def __init__(self, dir=None, max_len=7):
        """
        """
        self.max_len = max_len
        self.here = os.path.dirname(__file__)
        self.HanZiDir = os.path.join(self.here, "HanZi")
        self.dir = dir
        if dir and os.path.exists(dir):
            HeZiPath = os.path.join(dir, "HeZi.txt")
            if os.path.exists(HeZiPath):
                self.load(dir)

    def load(self, dir):
        HeZiPath = os.path.join(dir, "HeZi.txt")
        JiZiPath = os.path.join(dir, "JiZi.txt")
        if os.path.exists(JiZiPath):
            JiZi = open(JiZiPath).read().splitlines()
        else:
            JiZi = GouJian
        JiZi = set(JiZi)
        logger.info(f"{JiZiPath} load  JiZi:{len(JiZi)}")

        HeZi, values, slim2Zi, jieGou, max_len = loadHeZi(HeZiPath, JiZi, self.max_len)
        self.slim2Zi = slim2Zi
        self.HeZi = HeZi
        self.jieGou = jieGou
        self.max_len = max_len
        self.vocab = values
        logger.info(f"{dir} loaded vocab:{len(self.vocab)}")

    def build(self, folder, roots, max_len=7):
        logger.warning(f" {folder} building")
        vocab = set(GouJian) | set(x for x in roots)
        JiZi = [x for x in vocab if len(x) == 1]
        logger.info(f"receive roots:{len(roots)} JiZi:{len(JiZi)}")

        ChaiZiPath = os.path.join(self.HanZiDir, "ChaiZi.txt")
        YiTiZiPath = os.path.join(self.HanZiDir, "YiTiZi.txt")
        HeZiPath = os.path.join(folder, "HeZi.txt")
        JiZiPath = os.path.join(folder, "JiZi.txt")
        He2Zi.build(JiZi, ChaiZiPath, YiTiZiPath, HeZiPath, JiZiPath, max_len)
        self.load(folder)

    def cutHanzi(self, zi) -> str:
        ids = self.HeZi.get(zi, zi)
        return ids

    def tokenize(self, line):
        tokens = [self.cutHanzi(x) for x in line]
        return tokens

    def combineHanzi(self, chars):
        tokens = []
        i = 0
        while i < len(chars):
            ok = False
            x = chars[i]
            if x in self.jieGou:
                for j in range(2, self.max_len):
                    D = ''.join(chars[i:i+j])
                    if D in self.slim2Zi:
                        tokens.append(self.slim2Zi[D])
                        i += len(D)
                        ok = True
                        break

            if not ok:
                tokens.append(x)
                i += 1
        return tokens
