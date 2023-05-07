
import ahocorasick

class ZiSegmenter:
    def __init__(self, root_words, prefixs=[], suffixs=[],max_split=3):
        self.max_split = max_split
        self.root_words = root_words
        self.prefixs = set(x for x in prefixs)
        self.suffixs = set(x for x in suffixs)
        self.rootAC = ahocorasick.Automaton()
        for i,x in enumerate(self.root_words):
            self.rootAC.add_word(x, x)
        self.rootAC.make_automaton()

    def token_root(self, word):
        matchs = list(self.rootAC.iter(word))
        if not matchs:
            return [word, None, None]
        length = max(len(x[1]) for x in matchs)
        long_match = [x for x in matchs if len(x[1]) == length]
        longest_match = long_match[(len(long_match))//2]
        end,root = longest_match
        prefix = word[:end-len(root)+1]
        suffix = word[end+1:]
        return [prefix, root, suffix]

    def token_prefix(self, grams):
        tokens = []
        for i in range(min(self.max_split,len(grams))):
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
        for i in range(min(self.max_split, len(grams))):
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


def test_segmenter():
    line = "'〇㎡[คุณจะจัดพิธีแต่งงานเมื่อไรคะัีิ์ื็ํึ]Ⅷpays-g[ran]d-blanc-élevé » (白高大夏國)😀'\x0000熵"
    roots = ['la', 'a', 'ay', 'le']
    prefixs = ['e', 'l']
    suffixs = ['n', 'e', 'v']
    # from ZiTokenizer.UnicodeTokenizer import UnicodeTokenizer
    from UnicodeTokenizer import UnicodeTokenizer

    words = UnicodeTokenizer().tokenize(line)
    cutter = ZiSegmenter(roots, prefixs, suffixs)
    for word in words:
        tokens = cutter.token_word(word)
        print(word, tokens)

if __name__ == "__main__":

    test_segmenter()