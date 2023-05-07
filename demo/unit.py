import collections
import glob
import os
import gc
import multiprocessing

from logzero import logger

from ZiTokenizer.UnicodeTokenizer import UnicodeTokenizer
from ZiTokenizer.ZiSegmenter import ZiSegmenter
from ZiTokenizer.ZiCutter import ZiCutter
from ZiTokenizer.ZiTokenizer import ZiTokenizer
from glance import load_frequency, describe

doc = ["'〇㎡[คุณจะจัดพิธีแต่งงานเมื่อไรคะัีิ์ื็ํึ]Ⅷpays-g[ran]d-blanc-élevé » (白高大夏國)😀熇'\x0000𧭏2022２０１９\U0010ffff",
       "대한민국의Ⅷ首先8.88设置 st。art_new_word=True 和 output=[açaí]，output 就是最终 no such name",
       "的输出คุณจะจัดพิธีแต่งงานเมื่อไรคะ탑승 수속해야pneumonoultramicroscopicsilicovolcanoconiosis",
       "하는데 카운터가 어디에 있어요ꆃꎭꆈꌠꊨꏦꏲꅉꆅꉚꅉꋍꂷꂶꌠلأحياء تمارين تتطلب من [MASK] [PAD] [CLS][SEP]",
       '''est 𗴂𗹭𘜶𗴲𗂧, ou "phiow-bjij-lhjij-lhjij", ce que l'on peut traduire par « pays-grand-blanc-élevé » (白高大夏國).''',
       'วรรณพงษ์เป็นนักศึกษาชั้นปีที่หนึ่ง เรียนสาขาวิทยาการคอมพิวเตอร์และสารสนเทศคณะวิทยาศาสตร์ประยุกต์และวิศวกรรมศาสตร์อยู่ที่มหาวิทยาลัยขอนแก่นวิทยาเขตหนองคายยืมคืนทรัพยากรห้องสมุดเอกสารสัมมนาคอมพิวเตอร์ปัญญาประดิษฐ์กับการพัฒนาเกมแมวกินปลาหิวววไหมหลักสูตรใหม่สดสดทนได้',
       'ສົມເດັດພະເຈົ້າຢູ່ຫົວບໍຣົມໂກດຊົງທຳນຸບຳລຸງບ້ານເມືອງແລະພະສາດສະໜາຈົນກ່າວໄດ້ວ່າກຸງສີອະຍຸທະຢາໃນສະໄໝພະອົງນັ້ນເປັນຍຸກທີ່ບ້ານເມືອງດີ ມີຂຸນນາງຄົນສຳຄັນທີ່ເຕີບໂຕໃນເວລາຕໍ່ມາ ໃນລາຊະການຂອງພະອົງຫຼາຍຄົນ ເຊັ່ນ ສົມເດັດພະເຈົ້າກຸງທົນບຸລີ, ພະບາດສົມເດັດພະພຸດທະຍອດຟ້າຈຸລາໂລກມະຫາລາດ ເປັນຕົ້ນ ໃນທາງດ້ານວັນນະຄະດີກໍມີກະວີຄົນສຳຄັນ ເຊັ່ນ ເຈົ້າຟ້າທຳມາທິເບດໄຊຍະເຊດສຸລິຍະວົງ ກົມມະຂຸນເສນາພິທັກ ຫຼືເຈົ້າຟ້າກຸ້ງ ເຊິ່ງເປັນພະໂອລົດ ເປັນຕົ້ນ'
       ]


def test_ZiCutter(dir):
    cutter = ZiCutter(dir=dir)
    line = "'〇㎡[คุณจะจัดพิธีแต่งงานเมื่อไรคะัีิ์ื็ํึ]Ⅷpays-g[ran]d-blanc-élevé » (白高大夏國)熵😀'\x0000熇"
    tokens = cutter.tokenize(line)
    logger.info(tokens)
    a = cutter.combineHanzi(tokens)
    b = cutter.combineHanzi(''.join(tokens))
    logger.info(a)
    logger.info(b)


def test_build(freq_path, dir, alpha=1):
    if not os.path.exists(dir):
        os.makedirs(dir)
    import logzero
    logzero.logfile(os.path.join(dir, "ZiTokenizerBuild.log"), mode='w')
    tokenizer = ZiTokenizer()
    logger.warning(f" building from {freq_path}")
    word_freq, total = load_frequency(freq_path, alpha=alpha, do_lower_case=tokenizer.do_lower_case)
    assert word_freq
    P = []
    Q = []
    for x in word_freq.items():
        if x[1] >= 2:
            P.append(x)
        else:
            Q.append(x)
    del word_freq
    gc.collect()
    P.sort(key=lambda x: (-x[1], len(x[0]), x[0]))
    Q.sort(key=lambda x: (-x[1], len(x[0]), x[0]))
    word_freq = P+Q
    del P, Q
    gc.collect()
    describe(word_freq, total)
    tokenizer.build(word_freq, total, dir)

    tokenizer = ZiTokenizer(dir)
    doc = os.popen(f" tail {freq_path} -n 1000000 | shuf -n 10 ").read().splitlines()
    test_line(tokenizer, test_encode=True, doc=doc)
    # doc = [x.split('\t') for x in doc]
    # doc = [(k, float(v)) for k, v in doc]
    # for k, v in doc:
    #     tokens = tokenizer.tokenize(k)
    #     indexs = tokenizer.encode(k)
    #     words = tokenizer.decode(indexs)
    #     row = [k, v, ' '.join(tokens), tokenizer.token_word(k), ' '.join(words)]
    #     logger.info((row))
    return tokenizer


def test_line(tokenizer, test_encode=False, doc=doc):
    for line in doc:
        tokens = tokenizer.tokenize(line)
        logger.info(tokens)
        logger.info(line)

        if test_encode:
            indexs = tokenizer.encode(line)
            tokens = tokenizer.decode(indexs)

        line2 = tokenizer.detokenize(tokens)
        if line2 == line:
            logger.info(line2)
        else:
            logger.warning(line2)


def get_langs():
    freq_paths = glob.glob(rf"C:/data/word_frequency/*-word_frequency.tsv")
    langs = []
    for freq_path in freq_paths:
        name = os.path.basename(freq_path)
        lang = name.split('-')[0]
        if name.startswith('global'):
            continue
        langs.append((lang, freq_path))
    return langs


if __name__ == "__main__":
    langs = get_langs()
    tokenizer = UnicodeTokenizer()
    test_line(tokenizer)
    tokenizer = UnicodeTokenizer(never_split=["[UNK]", "[SEP]", "[PAD]", "[CLS]", "[MASK]"])
    test_line(tokenizer)
    tokenizer = UnicodeTokenizer(split_digit=True)
    test_line(tokenizer)
    tokenizer = UnicodeTokenizer(do_lower_case=True)
    test_line(tokenizer)
    tokenizer = UnicodeTokenizer(strip=True)
    test_line(tokenizer)
    tokenizer = UnicodeTokenizer(do_lower_case=True, strip=True)
    test_line(tokenizer)

    folder = "./demo"
    freq_path = f"{folder}/zh_classical-word_frequency.tsv"  # lang="zh_classical"
    test_build(freq_path, folder)
    test_ZiCutter(folder)

    tokenizer = ZiTokenizer(folder)
    test_line(tokenizer, test_encode=True)


"""

"""
