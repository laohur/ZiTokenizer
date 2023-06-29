# -*- coding: utf-8 -*-

import unicodedata


class UnicodeTokenizer:
    def __init__(self,  do_lower_case=False, never_split=[], highUnicodePoint=8192, strip=False, add_dummy_prefix=False):
        self.do_lower_case = do_lower_case
        self.highUnicodePoint = highUnicodePoint
        self.strip = strip
        self.add_dummy_prefix = add_dummy_prefix
        self.never_split = set(x for x in never_split)

    def split_blank(self, line):
        t = []
        for i, c in enumerate(line):
            if unicodedata.category(c)[0] == 'Z':
                if i==0 or line[i-1]!=c:
                    t.append(c)
                else:
                    t[-1] += c
                if i < len(line)-1 and line[i+1] != c:
                    t.append('')
            elif ord(c) >= self.highUnicodePoint:
                t += ['', c, '']
            else:
                if not t:
                    t.append(c)
                else:
                    t[-1] += c
        if self.strip:
            tokens = [x.strip() for x in t if x.strip()]
        else:
            tokens = [x for x in t if x]
        return tokens

    def split_category(self, line):
        if len(line) == 1:
            return [line]
        categorys = [unicodedata.category(x) for x in line]
        names = [unicodedata.name(x).split()[0] if categorys[i][0] in 'LN' else None for i, x in enumerate(line)]
        tokens = []
        for i, x in enumerate(line):
            if i == 0:
                tokens.append(x)
            elif categorys[i][0] == 'Z':
                tokens.append(x)
            elif categorys[i] == 'Mn':
                tokens[-1] +=x
            elif categorys[i][0] == categorys[i-1][0] and names[i] == names[i-1]:
                tokens[-1] += x
            else:
                tokens.append(x)

        tokens = [x for x in tokens if x]
        return tokens

    def tokenize(self, line):
        if len(line) <= 1:
            return list(line)
        if self.add_dummy_prefix and line[0] != ' ' and ord(line[0]) < self.highUnicodePoint and unicodedata.category(line[1])[0] == 'L':
            line = ' '+line
        words = self.split_blank(line)
        tokens = []
        for i, w in enumerate(words):
            if w in self.never_split:
                if tokens and tokens[-1][-1]==' ':
                    tokens[-1]=tokens[-1][:-1]
                tokens.append(w)
            else:
                u = w
                if self.do_lower_case:
                    u = unicodedata.normalize("NFD", u.lower())
                t = self.split_category(u)
                c = t[0][0]
                if tokens and tokens[-1] == ' ' and ord(c) < self.highUnicodePoint and unicodedata.category(c)[0] == 'L':
                    tokens[-1] += t[0]
                    tokens += t[1:]
                else:
                    tokens += t
        return tokens

    def detokenize(self, tokens):
        l = ''
        for i, x in enumerate(tokens):
            if i == 0 and self.add_dummy_prefix and len(x) >= 2 and x.startswith(' ') and ord(x[1]) < self.highUnicodePoint and unicodedata.category(x[1])[0] == 'L':
                x = x[1:]
            if x in self.never_split:
                l += ' '+x
            else:
                l += x
        return l


def test_UnicodeTokenizer():
    doc = ["'〇㎡[คุณจะจัดพิธีแต่งงานเมื่อไรคะัีิ์ื็ํึ]Ⅷpays-g[ran]d-blanc-élevé » (白高大夏國)😀熇'\x0000𧭏2022２０１９\U0010ffff",
           "대한민국의Ⅷ首先8.88设置 st。art_new_word=True 和 output=[açaí]，output 就是最终 no such name",
           "的输出คุณจะจัดพิธีแต่งงานเมื่อไรคะ탑승 수속해야pneumonoultramicroscopicsilicovolcanoconiosis",
           "하는데 카운터가 어디에 있어요ꆃꎭꆈꌠꊨꏦꏲꅉꆅꉚꅉꋍꂷꂶꌠلأحياء تمارين تتطلب من [MASK]   [PAD] [CLS][SEP]",
           '''est 𗴂𗹭𘜶𗴲𗂧, ou "phiow-bjij-lhjij-lhjij", ce que l'on peut traduire par « pays-grand-blanc-élevé » (白高大夏國).''',
           'วรรณพงษ์เป็นนักศึกษาชั้นปีที่หนึ่ง เรียนสาขาวิทยาการคอมพิวเตอร์และสารสนเทศคณะวิทยาศาสตร์ประยุกต์และวิศวกรรมศาสตร์อยู่ที่มหาวิทยาลัยขอนแก่นวิทยาเขตหนองคายยืมคืนทรัพยากรห้องสมุดเอกสารสัมมนาคอมพิวเตอร์ปัญญาประดิษฐ์กับการพัฒนาเกมแมวกินปลาหิวววไหมหลักสูตรใหม่สดสดทนได้',
           'ສົມເດັດພະເຈົ້າຢູ່ຫົວບໍຣົມໂກດຊົງທຳນຸບຳລຸງບ້ານເມືອງແລະພະສາດສະໜາຈົນກ່າວໄດ້ວ່າກຸງສີອະຍຸທະຢາໃນສະໄໝພະອົງນັ້ນເປັນຍຸກທີ່ບ້ານເມືອງດີ ມີຂຸນນາງຄົນສຳຄັນທີ່ເຕີບໂຕໃນເວລາຕໍ່ມາ ໃນລາຊະການຂອງພະອົງຫຼາຍຄົນ ເຊັ່ນ ສົມເດັດພະເຈົ້າກຸງທົນບຸລີ, ພະບາດສົມເດັດພະພຸດທະຍອດຟ້າຈຸລາໂລກມະຫາລາດ ເປັນຕົ້ນ ໃນທາງດ້ານວັນນະຄະດີກໍມີກະວີຄົນສຳຄັນ ເຊັ່ນ ເຈົ້າຟ້າທຳມາທິເບດໄຊຍະເຊດສຸລິຍະວົງ ກົມມະຂຸນເສນາພິທັກ ຫຼືເຈົ້າຟ້າກຸ້ງ ເຊິ່ງເປັນພະໂອລົດ ເປັນຕົ້ນ'
           ]
    # unicodeTokenizer = UnicodeTokenizer()
    unicodeTokenizer = UnicodeTokenizer(never_split=["[UNK]", "[SEP]", "[PAD]", "[CLS]", "[MASK]"])
    for line in doc:
        tokens = unicodeTokenizer.tokenize(line)
        logger.info(line)
        logger.info(unicodeTokenizer.detokenize(tokens))
        logger.info((tokens))


if __name__ == "__main__":
    from logzero import logger

    # line = "art_new_word=True"
    line = "Hello word"
    tokenizer = UnicodeTokenizer()
    logger.info((tokenizer.split_blank(line)))

    logger.info(tokenizer.tokenize("word"))
    tokens = tokenizer.tokenize(line)
    logger.info(tokens)
    logger.info(tokenizer.detokenize(tokens))

    line = "대한민국의'〇㎡[คุณจะจัดพิธีแต่งงานเมื่อไรคะัีิ์ื็ํึ]Ⅷpays-g[ran]d-blanc-élevé » (白高大夏國)😀熇'\x0000𧭏2022２０１９\U0010ffff"
    tokenizer = UnicodeTokenizer(strip=True)
    tokens = tokenizer.tokenize(line)
    logger.info(tokens)
    logger.info(tokenizer.detokenize(tokens))
    import timeit
    # re=timeit.timeit("''.join(chr(x) for x in range(int(1e6))) ")
    # logger.info(re)
    tokenizer = UnicodeTokenizer()

    # import time
    # t0 = time.time()
    # for i in range(10000):
    #     # chr(i)  # ValueError: chr() arg not in range(0x110000)
    #     tokenizer.tokenize(line)
    # t1 = time.time()
    # logger.info(t1-t0)

    test_UnicodeTokenizer()

"""
 '〇㎡[ค ณ จะจ ด พ ธ แ ต ง งานเม อ ไรคะ]ⅷpays-g[ran]d-blanc-e l eve»(白高大夏國)😀熇'00𧭏２０１９􏿿
 ▁　▁
"""
